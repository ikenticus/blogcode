package helpers

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"path"
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
	for _, api := range config.Post {
		data, err := ioutil.ReadFile(file)
		if err != nil {
			log.Fatal(err)
		}

		if strings.Contains(string(data), config.Text) {
			fmt.Printf("Uploading %s file: %s\n", config.Text, path.Base(file))
			url := api.Url + path.Base(file) + buildQuery(api.Query)
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
				fmt.Printf("Successfully uploaded file: %s\n", path.Base(file))
			} else {
				fmt.Printf("%+v", resp)
			}
		} else {
			fmt.Printf("Skipping non-%s file: %s\n", config.Text, path.Base(file))
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
