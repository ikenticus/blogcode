package helpers

import (
	"fmt"
	"reflect"
	"strings"
)

const skipExist = true
const useMulti = true

// getFiles is used to acquire files regardless of path type
func getFiles(c Config, p Paths) Config {
	files := buildFiles(c, p)
	switch getField(c, "URL."+p.Type).Kind() {
	case reflect.Slice:
		channelFiles(c, files)
		//syncFiles(c, files)
	case reflect.String:
		//default:
		for _, f := range files {
			fmt.Println("Downloading file", f)
			file := fmt.Sprintf("%s/%s", c.Output, f)
			url := fmt.Sprintf("%s/%s/%s?apiKey=%s", c.BaseURL, c.URL.Prefix, f, c.APIKey)
			err := downloadFile(file, url, true)
			if err != nil {
				fmt.Printf("-Failed to download %s due to %v\n", f, err)
			} else {
				for _, t := range c.Paths {
					if strings.Contains(f, "/"+strings.ToLower(t.Type)+"/") {
						fmt.Println("+Building list for", t.Type)
						values := parseXML(file, t.Type, t.Key)
						c = setFieldSlice(c, "URL."+t.Type, values)
					}
				}
			}
		}
	}
	return c
}

func Build(config Config) {
	if debug {
		fmt.Println(config.BaseURL, config.APIKey, reflect.ValueOf(config).FieldByName("URL").FieldByName("Prefix"))
		fmt.Println(getField(config, "URL.Prefix"))
	}
	for _, p := range config.Paths {
		if debug {
			fmt.Println("Calling", p.Type)
		}
		config = getFiles(config, p)
	}
}
