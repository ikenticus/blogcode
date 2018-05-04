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

type URL struct {
	Prefix string
	Sport  string
	League string
	Season string
}

type Path struct {
	Type    string
	Params  []string
	Formats []string
}

type Config struct {
	Output  string `env:"OUTPUT"`
	BaseURL string `env:"BASE_URL"`
	APIKey  string `env:"API_KEY"`
	URL     URL    `env:"URL"`
	Paths   []Path `env:PATHS"`
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
		fmt.Println(i,
			k.Elem().Type().Field(i).Name,
			k.Elem().Type().Field(i).Tag.Get("env"),
			reflect.TypeOf(v.Field(i)),
			v.Field(i).Kind(),
			v.Field(i).Type(),
			v.Field(i),
		)

		// Need to figure out how to recurse
		switch v.Field(i).Kind() {
		case reflect.String:
			if strings.HasPrefix(v.Field(i).String(), "VAULT") {
				fmt.Println("\t", strcase.LowerCamelCase(k.Elem().Type().Field(i).Tag.Get("env")))
				fmt.Println("\t", strings.Split(v.Field(i).String(), ".")[1])
				vv := getVaultField(
					strings.Split(v.Field(i).String(), ".")[1],
					strcase.LowerCamelCase(k.Elem().Type().Field(i).Tag.Get("env")),
				)
				fmt.Println("\t", vv)
				k.Elem().Field(i).SetString(vv)
			}
		case reflect.Slice:
			for s := 0; s < v.Field(i).Len(); s++ {
				fmt.Println("\t", s, v.Field(i).Index(s))
			}
		case reflect.Struct:
			sv := reflect.ValueOf(v.Field(i))
			fmt.Println("\t", sv)
		}
	}
	return config
}

func readYaml(yamlFile string) Config {
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
		config = initConfig(readYaml(yamlPath))
	}
	return config
}
