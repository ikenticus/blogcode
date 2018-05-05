package helpers

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
)

// downloadFile will download a url to a local file. It's efficient because it will
// write as it downloads and not load the whole file into memory.
func downloadFile(filePath string, url string) error {
	if skipExist {
		if _, err := os.Stat(filePath); err == nil {
			fmt.Println("SKIPPING existing file:", filePath)
			return nil
		}
	}

	folderPath := filepath.Dir(filePath)
	os.MkdirAll(folderPath, os.ModePerm)

	// Create the file
	out, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer out.Close()

	// Get the data via http
	resp, err := http.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Write the body to file
	_, err = io.Copy(out, resp.Body)
	if err != nil {
		return err
	}

	return nil
}
