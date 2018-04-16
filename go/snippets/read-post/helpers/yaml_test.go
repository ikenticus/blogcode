package helpers

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"path/filepath"
	"reflect"
	"testing"
)

func TestSetDefaults(t *testing.T) {
	var empty Config
	got := setDefaults(empty)

	cwd, err := filepath.Abs(".")
	if err != nil {
		t.Errorf("Unable to determine current path, err: %+v", err)
	}

	var want Config
	var input = []byte(fmt.Sprintf(`{
		"text": "%s",
		"read": ["%s"],
		"post": [
			{
				"url": "%s",
				"query": [
					{
						"key": "%s",
						"val": "%s"
					}
				]
			}
		]
		}`, Seek, cwd, ApiUrl, ApiKey, ApiVal))
	err = json.Unmarshal(input, &want)
	if err != nil {
		t.Errorf("Unable to test setDefaults, err: %+v", err)
	}

	if got.Text != want.Text {
		t.Errorf("Default Text was incorrect, got: %s, want: %s", got.Text, want.Text)
	}

	if !reflect.DeepEqual(got.Read, want.Read) {
		t.Errorf("Default Read was incorrect, got:\n%+v\nwant:\n%+v", got.Read, want.Read)
	}

	if !reflect.DeepEqual(got.Post, want.Post) {
		t.Errorf("Default Post was incorrect, got:\n%+v\nwant:\n%+v", got.Post, want.Post)
	}
}

func TestQueryPair(t *testing.T) {
	want := "hello=world"

	var got Query
	var input = []byte(`{
			"key": "hello",
			"val": "world"
		}`)
	err := json.Unmarshal(input, &got)
	if err != nil {
		t.Errorf("Unable to test Query.pair(), err: %+v", err)
	}

	if got.pair() != want {
		t.Errorf("Query pair was incorrect, got: %s, want: %s", got.pair(), want)
	}
}

func TestReadYaml(t *testing.T) {
	sample := "./test_data/sample"
	got := readYaml(sample + ".yaml")

	input, err := ioutil.ReadFile(sample + ".json")
	if err != nil {
		t.Errorf("Unable to read sample: %s.json, err: %+v", sample, err)
	}

	var want Config
	err = json.Unmarshal(input, &want)
	if err != nil {
		t.Errorf("Unable to test readYaml, err: %+v", err)
	}

	if !reflect.DeepEqual(got, want) {
		t.Errorf("Read YAML was incorrect, got:\n%+v\nwant:\n%+v", got, want)
	}
}

func TestYaml(t *testing.T) {
	sample := "./test_data/sample"
	got := Yaml(sample)

	input, err := ioutil.ReadFile(sample + ".json")
	if err != nil {
		t.Errorf("Unable to read sample: %s.json, err: %+v", sample, err)
	}

	var want Config
	err = json.Unmarshal(input, &want)
	if err != nil {
		t.Errorf("Unable to test readYaml, err: %+v", err)
	}

	for idx, path := range want.Read {
		abs, err := filepath.Abs(path)
		if err != nil {
			t.Errorf("Unable to Abs filepath for %s, err: %+v", path, err)
		}
		want.Read[idx] = abs
	}

	if !reflect.DeepEqual(got, want) {
		t.Errorf("YAML was incorrect, got:\n%+v\nwant:\n%+v", got, want)
	}
}
