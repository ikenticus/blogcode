package jsonschema

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"path"
	"reflect"
	"testing"
)

func TestDereference(t *testing.T) {
	tests := []struct {
		description string
		schemaPath  string
	}{
		{
			description: "Self Reference",
			schemaPath:  "./test_data/reference/image-self.json",
		},
		{
			description: "File Reference",
			schemaPath:  "./test_data/reference/image-file.json",
		},/*
        // TODO: figure out mock http client to test http json references
		{
			description: "Http Reference",
			schemaPath:  "./test_data/reference/image-http.json",
		},*/
		{
			description: "List Reference",
			schemaPath:  "./test_data/reference/image-list.json",
		},
		{
			description: "Shifted List Reference",
			schemaPath:  "./test_data/reference/image-list1.json",
		},
		{
			description: "Multiple List Reference",
			schemaPath:  "./test_data/reference/image-list2.json",
		},
		{
			description: "Nested List Reference",
			schemaPath:  "./test_data/reference/image-nest.json",
		},
		{
			description: "Ingestion Example",
			schemaPath:  "./test_data/reference/asset-event-facebook.json",
		},
	}
	for _, test := range tests {

		var want interface{}
		wantPath := fmt.Sprintf("%s/deref_%s", path.Dir(test.schemaPath), path.Base(test.schemaPath))
		wantJson, err := ioutil.ReadFile(wantPath)
		if err != nil {
			t.Errorf("Test %q - failed to read json file %q: %v", test.description, wantPath, err)
		}
		json.Unmarshal(wantJson, &want)

		var got interface{}
		gotJson, err := ioutil.ReadFile(test.schemaPath)
		if err != nil {
			t.Errorf("Test %q - failed to read json file %q: %v", test.description, test.schemaPath, err)
		}
		gotJson, err = Dereference(test.schemaPath, gotJson)
		if err != nil {
			t.Errorf("Test %q - failed to dereference json file %q: %v", test.description, test.schemaPath, err)
		}
		json.Unmarshal(gotJson, &got)

		if !reflect.DeepEqual(got, want) {
			t.Errorf("Test %q - got\n%s\nwant\n%s", test.description, got, want)
		}
	}
}
