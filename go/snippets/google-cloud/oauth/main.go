package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path"

	"golang.org/x/oauth2"
	"golang.org/x/oauth2/google"
	"golang.org/x/oauth2/jwt"
)

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

func usage() {
	fmt.Printf("Usage: %s key.json\n", path.Base(os.Args[0]))
	os.Exit(1)
}

func auth(path string) {
	type basicCreds struct {
		ProjectID string `json:"project_id"`
	}

	credBytes, err := ioutil.ReadFile(path)
	if err != nil {
		log.Fatal(err)
	}

	var keyData KeyData
	err = json.Unmarshal(credBytes, &keyData)
	if err != nil {
		log.Fatal(err)
	}
	//fmt.Println(keyData)
	service(keyData)
	/*
		basic := basicCreds{}
		if err := json.Unmarshal(credBytes, &basic); err != nil {
			return nil, err
		}

		creds, err := google.CredentialsFromJSON(context.Background(), credBytes, datastore.ScopeDatastore)
		if err != nil {
			return nil, err
		}

		client, err := datastore.NewClient(context.Background(), basic.ProjectID, option.WithCredentials(creds))
		if err != nil {
			return nil, fmt.Errorf("error connecting new client: %v", err)
		}
	*/
}

func service(creds KeyData) {
	url := fmt.Sprintf("https://datastore.googleapis.com/v1/projects/%s/operations", creds.ProjectID)
	// https://github.com/golang/oauth2/blob/master/google/example_test.go
	conf := &jwt.Config{
		Email:      creds.ClientEmail,
		PrivateKey: []byte(creds.PrivateKey),
		Scopes: []string{
			"https://www.googleapis.com/auth/datastore",
			"https://www.googleapis.com/auth/devstorage.read_write",
		},
		TokenURL: google.JWTTokenURL,
	}
	client := conf.Client(oauth2.NoContext)
	res, err := client.Get(url)
	if err != nil {
		fmt.Errorf("failed get client for %q: %v", url, err)
	}
	defer res.Body.Close()
	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		fmt.Errorf("failed to decompress gzipped data: %v", err)
	}

	//fmt.Println(string(out))
	var data interface{}
	json.Unmarshal(body, &data)
	output, err := json.MarshalIndent(data, "", "    ")
	if err != nil {
		fmt.Errorf("failed to JSON unmarshal data: %v", err)
	}
	fmt.Println(string(output))
}

func main() {
	if len(os.Args) < 2 {
		usage()
		return
	}

	auth(os.Args[1])
}
