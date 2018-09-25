package main

import (
	"bytes"
	"compress/gzip"
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path"
	"strconv"
	"strings"
	"time"
	"unicode/utf8"

	"cloud.google.com/go/datastore"
)

// struct for Datastore Kind
type DatastoreKind struct {
	KindName            string    `datastore:"kind_name"`
	EntityBytes         int       `datastore:"entity_bytes"`
	BuiltinIndexBytes   int       `datastore:"builtin_index_bytes"`
	BuiltinIndexCount   int       `datastore:"builtin_index_count"`
	CompositeIndexBytes int       `datastore:"composite_index_bytes"`
	CompositeIndexCount int       `datastore:"composite_index_count"`
	Timestamp           time.Time `datastore:"timestamp"`
	Count               int       `datastore:"count"`
	Bytes               int       `datastore:"bytes"`
}

func listKinds(ctx context.Context, client *datastore.Client, limit int) {
	query := datastore.NewQuery("__Stat_Kind__").Order("kind_name")

	kinds := []*DatastoreKind{}
	_, err := client.GetAll(ctx, query, &kinds)

	if err != nil {
		fmt.Errorf("Failed to run Kinds query\n")
	}
	if len(kinds) == 0 {
		fmt.Println("\nNo Kinds found!")
	}

	for _, k := range kinds {
		fmt.Printf("\nKind: %s\n  Count: %d\n  Bytes: %d\n", k.KindName, k.Count, k.Bytes)
		listKeys(ctx, client, k.KindName, limit)
	}
}

func listKeys(ctx context.Context, client *datastore.Client, key string, limit int) {
	query := datastore.NewQuery(key).KeysOnly().Limit(limit)

	keys, err := client.GetAll(ctx, query, nil)
	if err != nil {
		fmt.Errorf("\nFailed to run Keys query\n")
	}
	if len(keys) == 0 {
		fmt.Printf("\nNo Keys found for %s!", key)
	}

	fmt.Printf("\n%s:\n", key)
	/*
		if len(keys) > 10 {
			keys = keys[:10]
		} // same as .Limit(#) above
	*/
	//var last string
	for _, k := range keys {
		fmt.Printf("  %s\n", k.Name)
		//last = k.Name
	}

	/*
		if !strings.HasPrefix(key, "__") {
			//fmt.Printf("\nLast: %q, %q\n", last, key)
			readKey(ctx, client, key, last)
		}
	*/
}

// struct for Datastore Kind
type DatastoreTask struct {
	Category        string
	Done            bool
	Priority        float64
	Description     string `datastore:",noindex"`
	PercentComplete float64
	Created         time.Time
}

func listTasks(ctx context.Context, client *datastore.Client) {
	query := datastore.NewQuery("Task")

	tasks := []*DatastoreTask{}
	_, err := client.GetAll(ctx, query, &tasks)
	if err != nil {
		fmt.Errorf("\nFailed to run Tasks query\n")
	}
	if len(tasks) == 0 {
		fmt.Println("\nNo Tasks found!")
	}

	for _, t := range tasks {
		fmt.Printf("\nTask: %s\n", t.Description)
	}
}

type DatastoreEntity struct {
	Value []byte `datastore:",noindex"`
}

func readKey(ctx context.Context, client *datastore.Client, kind string, id string) {
	key := datastore.NameKey(kind, id, nil)

	var entity DatastoreEntity
	if err := client.Get(ctx, key, &entity); err != nil {
		if err == datastore.ErrNoSuchEntity {
			fmt.Errorf("\nEntity not found: %s\n", id)
		}
	}

	zip, err := gzip.NewReader(bytes.NewBuffer(entity.Value))
	if err != nil {
		fmt.Errorf("failed to initialize gzip Reader for id %q: %v", id, err)
	}

	out, err := ioutil.ReadAll(zip)
	if err != nil {
		fmt.Errorf("failed to decompress gzipped data for id %q: %v", id, err)
	}

	//fmt.Println(string(out))
	var data interface{}
	json.Unmarshal(out, &data)
	output, err := json.MarshalIndent(data, "", "    ")
	if err != nil {
		fmt.Errorf("failed to JSON unmarshal data for id %q: %v", id, err)
	}
	fmt.Println(string(output))
}

// struct for Google key.json data
type KeyData struct {
	AuthProviderX509CertURL string  `json:"auth_provider_x509_cert_url"`
	AuthURI                 string  `json:"auth_uri"`
	ClientEmail             string  `json:"client_email"`
	ClientID                float64 `json:"client_id,string"`
	ClientX509CertURL       string  `json:"client_x509_cert_url"`
	PrivateKey              string  `json:"private_key"`
	PrivateKeyID            string  `json:"private_key_id"`
	ProjectID               string  `json:"project_id"`
	TokenURI                string  `json:"token_uri"`
	Type                    string  `json:"type"`
}

func main() {
	if len(os.Args) < 2 {
		fmt.Printf("Usage: %s key.json [limit] [kind] [id]\n", path.Base(os.Args[0]))
		os.Exit(1)
	}
	keyPath := os.Args[1]
	os.Setenv("GOOGLE_APPLICATION_CREDENTIALS", keyPath)

	keyFile, err := ioutil.ReadFile(keyPath)
	if err != nil {
		log.Fatal(err)
	}

	var keyData KeyData
	err = json.Unmarshal(keyFile, &keyData)
	if err != nil {
		log.Fatal(err)
	}

	ctx := context.Background()
	projectID := keyData.ProjectID
	client, err := datastore.NewClient(ctx, projectID)
	if err != nil {
		fmt.Errorf("\nFailed to connect to datastore\n")
	}

	if len(os.Args) > 3 {
		readKey(ctx, client, os.Args[2], os.Args[3])
	} else {
		limit := 10
		if len(os.Args) > 2 {
			limit, err = strconv.Atoi(os.Args[2])
			if err != nil {
				fmt.Errorf("\nFailed to convert limit parameter\n")
			}
		}
		fmt.Printf("\nProject: %s\n%s\n", projectID, strings.Repeat("-", utf8.RuneCountInString(projectID)+10))
		listKeys(ctx, client, "__kind__", limit)
		listKinds(ctx, client, limit)
		listTasks(ctx, client)
	}
}
