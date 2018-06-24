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
	///fmt.Println("REFS", refs)
	//data.(map[string]interface{})["properties"].(map[string]interface{})["URL"] = data.(map[string]interface{})["definitions"].(map[string]interface{})["imageurl"]

	for _, ref := range refs {
		top := data
		pair := strings.Split(ref, "=")
		list := strings.Split(pair[0], ".")
		for i, item := range list {
			//fmt.Println("ITEM", i, item, len(list))
			if i < len(list)-1 {
				top = top.(map[string]interface{})[item]
			} else {
				ans := buildReference(schemaPath, data, pair[1])
				//fmt.Println("TYPE", item, reflect.ValueOf(ans).MapKeys())
				if len(reflect.ValueOf(ans).MapKeys()) > 1 {
					top.(map[string]interface{})[item] = ans //buildReference(schemaPath, data, pair[1])
				} else {
					// HAve not found a way to extract single key string, so hard-coding for testing now
					//key := reflect.ValueOf(ans).MapKeys()[0]
					//fmt.Println(key)
					key := "type"
					top.(map[string]interface{})[item].(map[string]interface{})[key] = ans.(map[string]interface{})[key]
				}
				//top.(map[string]interface{})[item] = ans //buildReference(schemaPath, data, pair[1])
			}
		}
	}

	return json.Marshal(data)
}

func walkInterface(node interface{}, source []string, refs []string) []string {
	//fmt.Println("TEST1", reflect.TypeOf(node), source)
	for key, val := range node.(map[string]interface{}) {
		//fmt.Println("===", reflect.TypeOf(val).Kind())
		switch reflect.TypeOf(val).Kind() {
		case reflect.String:
			//fmt.Println(key, "is a string")
			if key == "$ref" {
				//fmt.Println("Ref -> ", val.(string), node)
				refs = append(refs, strings.Join(source, ".")+"="+val.(string))
				//fmt.Println("Refs", refs)
			}
		case reflect.Slice:
			//fmt.Println(key, "is an array", reflect.ValueOf(val))
			for i, item := range val.([]interface{}) {
				if reflect.TypeOf(item).Kind() == reflect.Map {
					refs = walkInterface(item, append(source, string(i)), refs)
				}
			}
		case reflect.Map:
			//fmt.Println(key, "is an object")
			refs = walkInterface(node.(map[string]interface{})[key], append(source, key), refs)
		}
	}
	return refs
}

func buildReference(schemaPath string, top interface{}, ref string) interface{} {
	//fmt.Println(ref)
	target := strings.Split(ref, "#")
	//fmt.Println("BUILD", target)

	var source interface{}
	switch {
	case len(target[0]) == 0:
		//fmt.Println("Source is current doc")
		source = top
	case strings.HasPrefix(target[0], "http"):
		//fmt.Println("Source is web http")
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
		//fmt.Println("Source is local file", refPath)
		data, err := ioutil.ReadFile(refPath)
		if err != nil {
			fmt.Errorf("failed to read reference file %q: %v", refPath, err)
		}
		json.Unmarshal([]byte(data), &source)
	}
	//fmt.Println(parseRefPath(source, strings.Split(target[1], "/")[1:]))
	return parseRefPath(source, strings.Split(target[1], "/")[1:])
}

func parseRefPath(source interface{}, refPaths []string) interface{} {
	//output, _ := json.MarshalIndent(source, "", "  ")
	//fmt.Println("PARSE", string(output), len(refPaths), refPaths)
	if len(refPaths) > 1 {
		//fmt.Println("NEST")
		return parseRefPath(source.(map[string]interface{})[refPaths[0]], refPaths[1:])
	} else {
		ans := source.(map[string]interface{})[refPaths[0]]
		//fmt.Println("DONE", reflect.TypeOf(ans), ans)
		return ans //source.(map[string]interface{})[refPaths[0]]
	}
}
