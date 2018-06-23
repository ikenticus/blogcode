package jsonschema

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"path"
	"path/filepath"
	"reflect"
	"strings"

	"github.com/franela/goreq"
)

// Dereference parse JSON string and replaces all $ref with the referenced data.
func Dereference(schemaPath string, input []byte) ([]byte, error) {
	if !strings.Contains(string(input), "$ref") {
		return input, nil
	}
	var data interface{}
	json.Unmarshal([]byte(input), &data)
	walkInterface(path.Dir(schemaPath), data, data)
	//data.(map[string]interface{})["properties"].(map[string]interface{})["URL"] = data.(map[string]interface{})["definitions"].(map[string]interface{})["imageurl"]
	return json.Marshal(data)
}

func walkInterface(schemaPath string, top interface{}, node interface{}) {
	//fmt.Println("TEST1", reflect.TypeOf(node))
	for key, val := range node.(map[string]interface{}) {
		//fmt.Println("===", reflect.TypeOf(val).Kind())
		switch reflect.TypeOf(val).Kind() {
		case reflect.String:
			fmt.Println(key, "is a string")
			if key == "$ref" {
				//fmt.Println("Ref -> ", val.(string), node)
				node = buildReference(schemaPath, top, val.(string))
			}
		case reflect.Slice:
			fmt.Println(key, "is an array", reflect.ValueOf(val))
			for _, item := range val.([]interface{}) {
				if reflect.TypeOf(item).Kind() == reflect.Map {
					walkInterface(schemaPath, top, item)
				}
			}
		case reflect.Map:
			fmt.Println(key, "is an object")
			walkInterface(schemaPath, top, node.(map[string]interface{})[key])
		}
	}
}

func buildReference(schemaPath string, top interface{}, ref string) interface{} {
	//fmt.Println(ref)
	target := strings.Split(ref, "#")
	fmt.Println(target)

	var source interface{}
	switch {
	case len(target[0]) == 0:
		source = top
	case strings.HasPrefix(target[0], "http"):
		res, err := goreq.Request{
			Uri: target[0],
		}.Do()
		if err != nil {
			fmt.Errorf("unable to get reference from %s: %v", target[0], err)
			os.Exit(1)
		}
		res.Body.FromJsonTo(&source)
	default:
		refPath, err := filepath.Abs(schemaPath + "/" + target[0])
		if err != nil {
			fmt.Errorf("unable to expand reference filepath %s: %v", target[0], err)
			os.Exit(1)
		}
		data, err := ioutil.ReadFile(refPath)
		if err != nil {
			fmt.Errorf("failed to read reference file %q: %v", refPath, err)
		}
		json.Unmarshal([]byte(data), &source)
	}
	fmt.Println(parseRefPath(source, strings.Split(target[1], "/")[1:]))
	return parseRefPath(source, strings.Split(target[1], "/")[1:])
}

func parseRefPath(source interface{}, refPaths []string) interface{} {
	if len(refPaths) > 1 {
		return parseRefPath(source.(map[string]interface{})[refPaths[0]], refPaths[1:])
	} else {
		return source.(map[string]interface{})[refPaths[0]]
	}
}
