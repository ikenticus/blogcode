package helpers

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"path/filepath"
	"strings"
)

func buildQuery(query []Query) string {
	if query != nil {
		var pairs []string
		for _, kv := range query {
			pairs = append(pairs, kv.pair())
		}
		return "?" + strings.Join(pairs, "&")
	}
	return ""
}

func Post(config Config, file string) {
	// use filepath.Base instead of path.Base to support Windows slashes
	base := filepath.Base(file)

	for _, api := range config.Post {
		data, err := ioutil.ReadFile(file)
		if err != nil {
			log.Fatal(err)
		}

		if strings.Contains(string(data), config.Text) {
			url := api.Url + base + buildQuery(api.Query)
			fmt.Printf("Uploading %s file: %s to %s\n", config.Text, base, url)
			req, err := http.NewRequest("POST", url, bytes.NewReader(data))
			if err != nil {
				log.Fatal(err)
			}

			req.Header.Add("Content-Type", "text/plain")

			resp, err := http.DefaultClient.Do(req)
			if err != nil {
				log.Fatal(err)
			}

			if resp.StatusCode == 200 {
				fmt.Printf("Successfully uploaded file: %s\n", base)
			} else {
				fmt.Printf("Error uploading file: %s\n%+v\n", base, resp)
			}
		} else {
			fmt.Printf("Skipping non-%s file: %s\n", config.Text, base)
		}
	}

	/*
		for _,

		   req, err := http.NewRequest("POST", graphQLURL, textAssetQuery)
		   if err != nil {
		       log.Fatal(err)
		   }

		   req.Header.Add("content-type", "application/graphql")
		   req.Header.Add("x-sitecode", "USAT")
		   req.Header.Add("x-api-key", "blah")

		   resp, err := http.DefaultClient.Do(req)
		   if err != nil {
		       log.Fatal(err)
		   }

		   var content textAsset
		   dec := json.NewDecoder(resp.Body)
		   if err := dec.Decode(&content); err != nil {
		       log.Fatal(err)
		   }

		   fmt.Printf("Section: %q", content.SSTS.Section)
	*/
}
