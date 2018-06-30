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
	//fmt.Printf("%q\n", input)

	var output []byte

	output, _ = guido(input) // greedy type
	fmt.Println("\nGREEDY\n", string(output))

	output, _ = sharon(input) // sharing type
	fmt.Println("\nEXTEND\n", string(output))
}

func guido(input json.RawMessage) ([]byte, error) {
	var data merge.Guido
	json.Unmarshal(input, &data)
	return json.MarshalIndent(data, "", "    ")
}

func sharon(input json.RawMessage) ([]byte, error) {
	var data merge.Sharon
	json.Unmarshal(input, &data)
	return json.MarshalIndent(data, "", "    ")
}
