package helpers

import (
	"log"
	"os"
	"path/filepath"
	"sync"
	/*
	   "bytes"
	   "fmt"
	   "encoding/json"
	   "log"
	   "net/http"
	*/)

func Scan(config Config) {
	var files []string

	for _, root := range config.Read {
		err := filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
			if !info.IsDir() {
				files = append(files, path)
			}
			return nil
		})
		if err != nil {
			log.Fatal(err)
		}
	}

	var wg sync.WaitGroup
	wg.Add(len(files))
	for _, file := range files {
		go func(file string) {
			defer wg.Done()
			Post(config, file)
		}(file)
	}
	wg.Wait()
}
