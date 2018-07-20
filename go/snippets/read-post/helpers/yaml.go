package helpers

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"

	yaml "gopkg.in/yaml.v2"
)

type Query struct {
	Key string
	Val string
}

type Request struct {
	Url   string
	Query []Query
}

type Config struct {
	Text string
	Read []string
	Post []Request
}

const (
	Seek   = "Splenda"
	ApiUrl = "https://api.domain.com/service/post/splenda/"
	ApiKey = "api_key"
	ApiVal = "1234567890abcdefedcba0987654321"
)

func (q *Query) pair() string {
	return fmt.Sprintf("%s=%s", q.Key, q.Val)
}

// use filepath.Base instead of path.Base to support Windows slashes
//path.Base(main)
func readYaml(yamlFile string) Config {
	var config Config
	data, err := ioutil.ReadFile(yamlFile)
	if err == nil {
		err = yaml.Unmarshal(data, &config)
		if err != nil {
			log.Fatal(err)
		}
	}
	fmt.Printf("Loaded configuration from: %s\n", yamlFile)
	return config
}

func setDefaults(config Config) Config {
	// default text to Seek
	if config.Text == "" {
		config.Text = Seek
	}

	// default read to current directory
	if len(config.Read) < 1 {
		read, err := filepath.Abs(".")
		if err != nil {
			log.Fatal(err)
		}
		config.Read = append(config.Read, read)
	} else {
		for idx, path := range config.Read {
			abs, err := filepath.Abs(path)
			if err != nil {
				log.Fatal(err)
			}
			config.Read[idx] = abs
		}
	}

	// default read to current directory
	if len(config.Read) < 1 {
		read, err := filepath.Abs(".")
		if err != nil {
			log.Fatal(err)
		}
		config.Read = append(config.Read, read)
	}

	// set default post to external api
	if len(config.Post) < 1 {
		var query []Query
		config.Post = append(config.Post, Request{
			Url: ApiUrl,
			Query: append(query, Query{
				Key: ApiKey,
				Val: ApiVal,
			}),
		})
	}

	return config
}

func Yaml(main string) Config {
	var config Config

	// use filepath.Base instead of path.Base to support Windows slashes
	dir := filepath.Dir(main)
	base := filepath.Base(main) + ".yaml"
	if _, err := os.Stat(base); err == nil {
		config = readYaml(base)
	} else if _, err := os.Stat(filepath.Join(dir, base)); err == nil {
		config = readYaml(filepath.Join(dir, base))
	}

	return setDefaults(config)
}
