package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/ikenticus/blogcode/go/snippets/json-struct/merge"
)

func main() {
	source := os.Args[1]
	//fmt.Println("source", source)
	input, err := ioutil.ReadFile(source)
	if err != nil {
		fmt.Errorf("failed to read json file %q: %v", source, err)
		os.Exit(10)
	}
	fmt.Printf("%q\n", input)

	var output []byte
	var data merge.Child
	json.Unmarshal(input, &data)
	fmt.Printf("%q\n", data)

	output, err = json.MarshalIndent(data, "", "    ")
	if err != nil {
		fmt.Errorf("failed to marshal indent json: %v", err)
		os.Exit(30)
	}

	fmt.Println(string(output))
}
