package helpers

import (
	"encoding/json"
	"testing"
)

func TestBuildQuery(t *testing.T) {
	var query []Query
	var input = []byte(`[
		{
			"key": "hello",
			"val": "world"
		},
		{
			"key": "this",
			"val": "that"
		}
		]`)
	err := json.Unmarshal(input, &query)
	if err != nil {
		t.Errorf("Unable to test buildQuery, err: %+v", err)
	}

	want := "?hello=world&this=that"
	got := buildQuery(query)

	if got != want {
		t.Errorf("Build Query was incorrect, got: %s, want: %s", got, want)
	}

	want = ""
	got = buildQuery(nil)
	if got != want {
		t.Errorf("Empty Query was incorrect, got: %s, want: %s", got, want)
	}
}
