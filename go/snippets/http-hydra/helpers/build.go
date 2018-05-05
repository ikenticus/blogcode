package helpers

import (
	"fmt"
	"reflect"
	"strings"
)

const skipExist = true

// funcMap maps path types to functions
var funcMap = map[string]interface{}{
	"results": resultsFiles,
	"season":  seasonFiles,
	"teams":   teamsFiles,
}

// resultsFiles is used to acquire files looping through results slice
func resultsFiles(c Config, p Paths) {
	fmt.Println("Processing results", c, "\n", p.Params, "\n")
}

// seasonFiles is used to acquire files for the season
func seasonFiles(c Config, p Paths) {
	fmt.Println("Processing season", c, "\n", p.Params, "\n")
	files := buildFiles(c, p)
	fmt.Println(files, "\n")
}

// teamsFiles is used to acquire files looping through teams slice
func teamsFiles(c Config, p Paths) {
	fmt.Println("Processing teams", c, "\n", p.Params, "\n")
}

// getFiles is used to acquire files regardless of path type
func getFiles(c Config, p Paths) Config {
	files := buildFiles(c, p)
	for _, f := range files {
		fmt.Println("Downloading", p.Type, "file", f)
		file := fmt.Sprintf("%s/%s", c.Output, f)
		url := fmt.Sprintf("%s/%s/%s?apiKey=%s", c.BaseURL, c.URL.Prefix, f, c.APIKey)
		err := downloadFile(file, url)
		if err != nil {
			fmt.Printf("FAILED to download %s due to %v\n", f, err)
		} else {
			for _, t := range c.Paths {
				if strings.Contains(f, "/"+strings.ToLower(t.Type)+"/") {
					fmt.Println("Building", t.Type)
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
	//reflect.ValueOf(&r).Elem().Field(i).SetInt( i64 )
	//config.URL.Teams = append(config.URL.Teams, 1, 2, 3)
	//config.URL.Results = append(config.URL.Results, 7, 8, 9)
	for _, p := range config.Paths {
		if debug {
			fmt.Println("Calling", p.Type)
		}

		// leaving below to demonstrate dynamic function call
		// if different parameters, then use a switch(p.Type)
		//funcMap[strings.ToLower(p.Type)].(func(Config, Paths))(config, p)

		config = getFiles(config, p)
	}
}
