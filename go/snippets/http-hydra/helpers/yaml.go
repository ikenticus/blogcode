package helpers

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"reflect"
	"strings"

	vaultApi "github.com/hashicorp/vault/api"
	strcase "github.com/stoewer/go-strcase"
	yaml "gopkg.in/yaml.v2"
)

const debug = false

type URL struct {
	Prefix  string
	Sport   string
	League  string
	Season  string
	Serial  string
	Results []int
	Teams   []int
}

type Paths struct {
	Key     string
	Type    string
	Params  []string
	Formats []string
}

type Config struct {
	Output  string  `env:"OUTPUT"`
	BaseURL string  `env:"BASE_URL"`
	APIKey  string  `env:"API_KEY"`
	URL     URL     `env:"URL"`
	Paths   []Paths `env:"PATHS"`
}

func getVaultField(vaultPath string, field string) string {
	vaultConfig := vaultApi.DefaultConfig()
	vaultClient, err := vaultApi.NewClient(vaultConfig)
	if err != nil {
		fmt.Printf("An error occurred creating vaultClient: %v\n", err)
		return ""
	}
	dbConfig, err := vaultClient.Logical().Read(vaultPath)
	if err != nil {
		fmt.Printf("An error occurred reading secret: %v\n", err)
		return ""
	}
	return dbConfig.Data[field].(string)
}

func initConfig(config Config) Config {
	k := reflect.ValueOf(&config)
	v := reflect.ValueOf(config)

	for i := 0; i < v.NumField(); i++ {
		if debug {
			fmt.Println(i, // index: 4
				k.Elem().Type().Field(i).Name,           // key: Paths
				k.Elem().Type().Field(i).Tag.Get("env"), // tag.key: PATHS
				reflect.TypeOf(v.Field(i)),              // typeof: reflect.Value
				v.Field(i).Kind(),                       // kind: slice
				v.Field(i).Type(),                       // type: []helpers.Paths
				v.Field(i),                              // value: [{Season [Sport League Season League] [%s/%s/result...
			)
		}

		// Need to figure out how to recurse
		switch v.Field(i).Kind() {
		case reflect.String:
			if strings.HasPrefix(v.Field(i).String(), "VAULT") {
				vv := getVaultField(
					strings.Split(v.Field(i).String(), ".")[1],
					strcase.LowerCamelCase(k.Elem().Type().Field(i).Tag.Get("env")),
				)
				if debug {
					fmt.Println("\t", strcase.LowerCamelCase(k.Elem().Type().Field(i).Tag.Get("env")))
					fmt.Println("\t", strings.Split(v.Field(i).String(), ".")[1])
					fmt.Println("\t", vv)
				}
				k.Elem().Field(i).SetString(vv)
			}
		case reflect.Slice:
			if debug {
				for s := 0; s < v.Field(i).Len(); s++ {
					fmt.Println("\t", s, v.Field(i).Index(s))
				}
			}
		case reflect.Struct:
			if debug {
				fmt.Println("\t", reflect.ValueOf(v.Field(i)))
			}
		}
	}
	return config
}

// readYAML will read and unmarshal YAML file
func readYAML(yamlFile string) Config {
	var config Config
	data, err := ioutil.ReadFile(yamlFile)
	if err == nil {
		err = yaml.Unmarshal(data, &config)
		if err != nil {
			log.Fatal(err)
		}
	}
	fmt.Printf("Loaded configuration from: %s\n", yamlFile)
	return config
}

func Yaml(yamlFile string) Config {
	var config Config
	yamlPath, err := filepath.Abs(yamlFile)
	if err != nil {
		fmt.Printf("Input YAML %s error: %v", yamlFile, err)
		os.Exit(2)
	}
	if _, err := os.Stat(yamlPath); err == nil {
		config = initConfig(readYAML(yamlPath))
	}
	return config
}
