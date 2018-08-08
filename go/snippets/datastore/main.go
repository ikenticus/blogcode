package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path"
	"strings"
	"time"
	"unicode/utf8"

	"cloud.google.com/go/datastore"
)

// struct for Datastore query
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
		fmt.Printf("Usage: %s key.json\n", path.Base(os.Args[0]))
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
		fmt.Errorf("Failed to connect to datastore\n")
	}

	q := datastore.NewQuery("__Stat_Kind__").Order("kind_name")

	kinds := []*DatastoreKind{}
	_, err = client.GetAll(ctx, q, &kinds)
	if err != nil {
		fmt.Errorf("Failed to run query\n")
	}

	fmt.Printf("Project: %s\n%s\n", projectID, strings.Repeat("-", utf8.RuneCountInString(projectID)+10))
	for _, k := range kinds {
		fmt.Printf("Kind: %s\n  Count: %d\n  Bytes: %d\n", k.KindName, k.Count, k.Bytes)
	}
}
