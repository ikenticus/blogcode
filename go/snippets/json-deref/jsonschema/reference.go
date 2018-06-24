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
	refs := walkInterface(data, []string{}, []string{})

	for _, ref := range refs {
		top := data
		pair := strings.Split(ref, "=")
		list := strings.Split(pair[0], ".")
		for i, item := range list {
			if i < len(list)-1 {
				top = top.(map[string]interface{})[item]
			} else {
				targetRef := buildReference(schemaPath, data, pair[1])
				targetKeys := reflect.ValueOf(targetRef).MapKeys()
				if len(targetKeys) > 1 {
					top.(map[string]interface{})[item] = targetRef
				} else {
					key := targetKeys[0].Interface().(string)
					top.(map[string]interface{})[item].(map[string]interface{})[key] = targetRef.(map[string]interface{})[key]
					delete(top.(map[string]interface{})[item].(map[string]interface{}), "$ref")
				}
			}
		}
	}

	return json.Marshal(data)
}

// walkInterface traverses the map[string]interface{} to located json references
func walkInterface(node interface{}, source []string, refs []string) []string {
	for key, val := range node.(map[string]interface{}) {
		switch reflect.TypeOf(val).Kind() {
		case reflect.String:
			if key == "$ref" {
				refs = append(refs, strings.Join(source, ".")+"="+val.(string))
			}
		case reflect.Slice:
			for i, item := range val.([]interface{}) {
				if reflect.TypeOf(item).Kind() == reflect.Map {
					refs = walkInterface(item, append(source, string(i)), refs)
				}
			}
		case reflect.Map:
			refs = walkInterface(node.(map[string]interface{})[key], append(source, key), refs)
		}
	}
	return refs
}

// buildReference constructs the json reference: internal, file or http
func buildReference(schemaPath string, top interface{}, ref string) interface{} {
	target := strings.Split(ref, "#")
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
		refPath, err := filepath.Abs(path.Dir(schemaPath) + "/" + target[0])
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

	return parseReference(source, strings.Split(target[1], "/")[1:])
}

// parseReference recursively parses the given reference path
func parseReference(source interface{}, refPaths []string) interface{} {
	if len(refPaths) > 1 {
		return parseReference(source.(map[string]interface{})[refPaths[0]], refPaths[1:])
	} else {
		return source.(map[string]interface{})[refPaths[0]]
	}
}
