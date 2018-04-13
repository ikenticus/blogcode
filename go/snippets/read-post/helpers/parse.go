// Package helpers contains the parse and upload tools
package helpers

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"sync"
)

func Scan(config Config) {
	var files []string

	for _, root := range config.Read {
		fmt.Printf("Scanning directory: %s\n", root)
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
