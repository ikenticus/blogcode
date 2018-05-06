package helpers

import (
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
	"sync"
)

// http comparison for NHL results (box/ss):
//	real	11m53.835s	downloadFile (1445/1445) w/o pretty
//	real	11m52.862s	channelFiles 10 (1445/1445)
//	real	11m10.620s	channelFiles 25 (1445/1445)
//	real	11m10.620s	channelFiles 100 (1445/1445)
const maxBuffer = 25

// downloadFile will download a url to a local file. It's efficient because it will
// write as it downloads and not load the whole file into memory.
func downloadFile(filePath string, url string, pretty bool) error {
	if skipExist {
		if _, err := os.Stat(filePath); err == nil {
			fmt.Println("SKIPPING existing file:", filePath)
			return nil
		}
	}

	folderPath := filepath.Dir(filePath)
	os.MkdirAll(folderPath, os.ModePerm)

	// Get the data via http
	resp, err := http.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	//if strings.HasSuffix(filePath, ".xml") {
	if pretty {
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			fmt.Errorf("Unable to read data from", url)
			return err
		}
		data := cleanXML(string(body))
		err = ioutil.WriteFile(filePath, []byte(data), 0644)
		if err != nil {
			return err
		}
	} else {
		// Create the file
		out, err := os.Create(filePath)
		if err != nil {
			return err
		}
		defer out.Close()

		// Write the body to file
		_, err = io.Copy(out, resp.Body)
		if err != nil {
			return err
		}
	}

	return nil
}

// channelFiles downloads files via channels
// => currently fails to complete with no errors
func channelFiles(c Config, files []string) error {
	var errStr string

	ch := make(chan error, maxBuffer)
	go func(ch chan error) {
		for _, f := range files {
			fmt.Println("Downloading file", f)
			file := fmt.Sprintf("%s/%s", c.Output, f)
			url := fmt.Sprintf("%s/%s/%s?apiKey=%s", c.BaseURL, c.URL.Prefix, f, c.APIKey)
			err := downloadFile(file, url, false)
			ch <- err
		}
		close(ch)
	}(ch)

	for e := range ch {
		errStr = fmt.Sprintf("%s\n%v", errStr, e)
	}

	var err error
	if errStr != "" {
		err = errors.New(errStr)
	}
	return err
}

// syncFiles downloads files via WaitGroup
func syncFiles(c Config, files []string) error {
	filesLen := len(files)
	var errStr string
	var wg sync.WaitGroup
	wg.Add(filesLen)
	for i := 0; i < filesLen; i++ {
		go func(i int) {
			defer wg.Done()
			f := files[i]

			fmt.Println("Downloading file", f)
			file := fmt.Sprintf("%s/%s", c.Output, f)
			url := fmt.Sprintf("%s/%s/%s?apiKey=%s", c.BaseURL, c.URL.Prefix, f, c.APIKey)
			err := downloadFile(file, url, false)
			if err != nil {
				errStr = errStr + "\n" + err.Error()
			}
		}(i)
	}
	wg.Wait()

	var err error
	if errStr != "" {
		err = errors.New(errStr)
	}
	return err
}
