package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"github.com/ikenticus/blogcode/go/snippets/json-deref/jsonschema"
)

func main() {
	source := os.Args[1]
	//fmt.Println("source", source)
	input, err := ioutil.ReadFile(source)
	if err != nil {
		fmt.Errorf("failed to read json file %q: %v", source, err)
		os.Exit(10)
	}

	input, err = jsonschema.Dereference(source, input)
	if err != nil {
		fmt.Errorf("failed to Dereference json: %v", err)
		os.Exit(20)
	}

	var data interface{}
	json.Unmarshal(input, &data)

	output, err := json.MarshalIndent(data, "", "    ")
	if err != nil {
		fmt.Errorf("failed to marshal indent json: %v", err)
		os.Exit(30)
	}

	fmt.Println(string(output))
}
