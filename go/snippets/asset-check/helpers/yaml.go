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
	API     string
	GraphQL string
}

type Config struct {
	APIKey    string `env:"apigeeconsumerkey"`
	Bucket    string
	Couchbase string `env:"couchbaseurl"`
	Front     string
	Query     string
	SASL      string `env:"couchbasebucketpassword"`
	SiteCode  string
	URL       URL
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
