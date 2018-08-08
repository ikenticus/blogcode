package main

import (
	"fmt"
	"reflect"
)

const debug = false

type URL struct {
	API     string
	DiagAPI string
	GraphQL string
	PresAPI string
}

type Config struct {
	Uno   string `env:"ENV_ONE"`
	Zwei  string `env:"ENV_TWO" json:"JSON2"`
	Trois string `env:"ENV_TRE" json:"JSON3" yaml:"YAML_ABC"`
}

func main() {
	var config Config
	k := reflect.ValueOf(&config)
	v := reflect.ValueOf(config)

	for _, e := range []string{"env", "json", "yaml"} {
		fmt.Println("\n---", e, "---")
		for i := 0; i < v.NumField(); i++ {
			fmt.Println(i, k.Elem().Type().Field(i).Name, k.Elem().Type().Field(i).Tag.Get(e))
		}
	}
}
