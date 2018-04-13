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

const Seek = "Sagarin"

func (q *Query) pair() string {
	return fmt.Sprintf("%s=%s", q.Key, q.Val)
}

// use filepath.Base instead of path.Base to support Windows slashes
//path.Base(main)
func read(cfgfile string) Config {
	var config Config
	data, err := ioutil.ReadFile(cfgfile)
	if err == nil {
		err = yaml.Unmarshal(data, &config)
		if err != nil {
			log.Fatal(err)
		}
	}
	fmt.Printf("Loaded configuration from: %s\n", cfgfile)
	return config
}

func Yaml(main string) Config {
	var config Config

	// use filepath.Base instead of path.Base to support Windows slashes
	dir := filepath.Dir(main)
	base := filepath.Base(main) + ".yaml"
	if _, err := os.Stat(base); err == nil {
		config = read(base)
	} else if _, err := os.Stat(filepath.Join(dir, base)); err == nil {
		config = read(filepath.Join(dir, base))
	}

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
			Url: "https://api.gannett-cdn.com/sportssvc/post/sagarin/",
			Query: append(query, Query{
				Key: "api_key",
				Val: "57646bc6bca4811fea000001d1227c937acd4a17696f2718976d19a5",
			}),
		})
	}

	return config
}
