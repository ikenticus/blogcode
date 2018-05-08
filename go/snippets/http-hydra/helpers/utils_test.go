package helpers

import (
	"reflect"
	"testing"
)

var testPath = Paths{
	Key:     "competition",
	Type:    "Results",
	Params:  []string{"Sport", "League", "Season", "League"},
	Formats: []string{"%s/%s/teams/%s/teams_%s.xml", "%s/%s/team-stats/%s/team_stats_%s.xml"},
}

var testTeam = Paths{
	Key:     "team",
	Type:    "Teams",
	Params:  []string{"Sport", "League", "Season", "Teams", "League"},
	Formats: []string{"%s/%s/players/%s/players_%s_%s.xml"},
}

var testConfig = Config{
	Output: "_test",
	URL: URL{
		Prefix: "sport/v2",
		Sport:  "baseball",
		League: "MLB",
		Season: "2018",
		Teams:  []int{1, 2, 3},
	},
	Paths: []Paths{testPath},
}

func TestBuildFiles(t *testing.T) {
	tests := []struct {
		description string
		config      Config
		path        Paths
		output      []string
	}{
		{
			description: "successful string build",
			config:      testConfig,
			path:        testPath,
			output:      []string{"baseball/MLB/teams/2018/teams_MLB.xml", "baseball/MLB/team-stats/2018/team_stats_MLB.xml"},
		},
		{
			description: "successful slice build",
			config:      testConfig,
			path:        testTeam,
			output: []string{
				"baseball/MLB/players/2018/players_1_MLB.xml",
				"baseball/MLB/players/2018/players_2_MLB.xml",
				"baseball/MLB/players/2018/players_3_MLB.xml",
			},
		},
	}

	for _, test := range tests {
		if got, want := buildFiles(test.config, test.path), test.output; !reflect.DeepEqual(got, want) {
			t.Errorf("Test %q - got %v, want %v", test.description, got, want)
		}
	}
}

func TestSetFieldSlice(t *testing.T) {
	tests := []struct {
		description string
		config      Config
		key         string
		values      []int
		output      Config
	}{
		{
			description: "successful set field slice",
			config:      testConfig,
			key:         "URL.Teams",
			values:      []int{7, 8, 9},
			output: Config{
				Output: "_test",
				URL: URL{
					Prefix: "sport/v2",
					Sport:  "baseball",
					League: "MLB",
					Season: "2018",
					Teams:  []int{1, 2, 3, 7, 8, 9},
				},
				Paths: []Paths{testPath},
			},
		},
	}

	for _, test := range tests {
		if got, want := setFieldSlice(test.config, test.key, test.values), test.output; !reflect.DeepEqual(got, want) {
			t.Errorf("Test %q - got %v, want %v", test.description, got, want)
		}
	}
}
