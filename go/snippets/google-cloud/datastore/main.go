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
	"regexp"
	"strconv"
	"strings"
	"time"
	"unicode/utf8"

	"cloud.google.com/go/datastore"
	"github.com/golang/snappy"
	"google.golang.org/api/iterator"
)

const datastoreMaxPropertyBytes = 1048487

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
		//fmt.Printf("RAW: %+v\n", k)
		listKeys(ctx, client, k.KindName, limit)
	}
}

func filter(ctx context.Context, client *datastore.Client, key string, filter string) {
	//query := datastore.NewQuery(key).Filter("DataType =", "teams").Order("-DataType")
	query := datastore.NewQuery(key)
    //regex := *regexp.MustCompile(`^(\w+\W+)(\w+)$`)
    regex := *regexp.MustCompile(`^(.+[<=>]+)(.+)$`)
    for _, pair := range strings.Split(filter, ",") {
        //fmt.Printf("Pair: %s\n", pair)
        res := regex.FindAllStringSubmatch(pair, 2)
        for i := range res {
            //fmt.Printf("Filter: %s -> %s\n", res[i][1], res[i][2])
            query = query.Filter(res[i][1], res[i][2])
        }
    }
	//query := datastore.NewQuery(key).Filter("DataType=", "teams")
    it := client.Run(ctx, query)
    for {
	    var entity DatastoreEntity
        id, err := it.Next(&entity)
        if err == iterator.Done {
            break
        }
        if err != nil {
            log.Fatalf("Error fetching next entity: %v", err)
        }
        fmt.Printf("Entity %s: %s %s/%s (%s) %s\n", entity.DataType, entity.Season, entity.Sport, entity.League, entity.LastModified, id)
        //fmt.Printf("Value %+v\n", string(entity.Value))
    }
}

func findKeys(ctx context.Context, client *datastore.Client, key string, filter string) {
	query := datastore.NewQuery(key).KeysOnly()
	keys, err := client.GetAll(ctx, query, nil)
	if err != nil {
		fmt.Errorf("\nFailed to run Keys query\n")
	}
	if len(keys) == 0 {
		fmt.Printf("\nNo Keys found for %s!", key)
	}
	fmt.Printf("\n%s:\n", key)
	for _, k := range keys {
		// loop through and match until better Query.Filter found
		matched, err := regexp.MatchString(filter, k.Name)
		if err != nil {
			fmt.Errorf("\nSyntax error with regexp\n")
		}
		if matched {
			//if strings.Contains(k.Name, filter) {
			fmt.Printf("  %s\n", k.Name)
		}
	}
}

func listKeys(ctx context.Context, client *datastore.Client, key string, limit int) {
	query := datastore.NewQuery(key).KeysOnly().Limit(limit)
	if limit < 0 {
		query = datastore.NewQuery(key).KeysOnly()
	}

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
	if limit < 0 {
		fmt.Printf("\n%s contains %d items\n", key, len(keys))
	}
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
	Value         []byte `datastore:",noindex"`

    // sportEntity
	Sport         string
	League        string
	Season        string
	DataType      string
	SchemaVersion string
	LastModified  string
}

type BatchError struct {
	Errors map[string]error
}

func (b BatchError) Error() string {
	errList := []string{}
	for id, err := range b.Errors {
		errList = append(errList, fmt.Sprintf("ID %q: %v", id, err))
	}

	return strings.Join(errList, ",")
}

func readMultiKey(ctx context.Context, client *datastore.Client, kind string, ids []string) {
	var keys []*datastore.Key
	for _, id := range ids {
		keys = append(keys, datastore.NameKey(kind, id, nil))
	}

	entities := make([]*DatastoreEntity, len(ids))
	if err := client.GetMulti(ctx, keys, entities); err != nil {
		if ctx.Err() != nil {
			fmt.Errorf("context cancelled")
		}
		if !strings.HasPrefix(err.Error(), datastore.ErrNoSuchEntity.Error()) {
			fmt.Errorf("Entities not found %s: %v\n", ids, err)
		}
	}

	outputs := make([]string, len(ids))
	batchErr := BatchError{Errors: make(map[string]error)}
	for i, entity := range entities {
		if entity == nil {
			outputs[i] = ""
			continue
		}

		zip, err := gzip.NewReader(bytes.NewBuffer(entity.Value))
		if err != nil {
			fmt.Errorf("failed to initialize gzip Reader for ids %q: %v", ids[i], err)
			snap, err := snappy.Decode(nil, entity.Value)
			if err != nil {
				fmt.Errorf("error with snappy decoding: %v", err)
			} else {
				fmt.Printf("SNAP: %+v\n", string(snap))
				return
			}
		}

		out, err := ioutil.ReadAll(zip)
		if err != nil {
			batchErr.Errors[ids[i]] = fmt.Errorf("failed to decompress gzipped data for id %q: %v", ids[i], err)
			continue
		}

		var data interface{}
		json.Unmarshal(out, &data)
		output, err := json.MarshalIndent(data, "", "    ")
		if err != nil {
			fmt.Errorf("failed to JSON unmarshal data for id %q: %v", ids[i], err)
			outputs[i] = string(out)
		} else {
			outputs[i] = string(output)
		}
	}

	if len(batchErr.Errors) == 0 {
		fmt.Println(strings.Join(outputs, "\n=====\n"))
	} else {
		fmt.Println(batchErr.Errors)
	}
}

/*
	//fmt.Println(string(out))
*/

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
		snap, err := snappy.Decode(nil, entity.Value)
		if err != nil {
			fmt.Errorf("error with snappy decoding: %v", err)
		} else {
			fmt.Printf("SNAP: %+v\n", string(snap))
			return
		}
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
		fmt.Println(string(out))
	} else {
		fmt.Println(string(output))
	}
}

func deleteKey(ctx context.Context, client *datastore.Client, kind string, id string) {
	key := datastore.NameKey(kind, id, nil)
	if err := client.Delete(ctx, key); err != nil {
		if err == datastore.ErrNoSuchEntity {
			fmt.Errorf("\nEntity not found: %s\n", id)
		}
	}
	fmt.Printf("Deleted id %s from %s\n", id, kind)
}

func writeKey(ctx context.Context, client *datastore.Client, kind string, id string, dataPath string) {
	key := datastore.NameKey(kind, id, nil)
	data, err := ioutil.ReadFile(dataPath)
	if err != nil {
		fmt.Errorf("Unable to read file: %s\n%q\n", dataPath, err)
	}
	//fmt.Println(key)
	//fmt.Println(string(data))
	//entity := &DatastoreEntity{Value: data}

	var buf bytes.Buffer
	zip := gzip.NewWriter(&buf)
	if _, err := zip.Write(data); err != nil {
		fmt.Errorf("failed gzip for id %q: %v", id, err)
	}
	zip.Close()
	if buf.Len() > datastoreMaxPropertyBytes {
		fmt.Errorf("compressed size %d bytes excedes datastore max %d bytes", buf.Len(), datastoreMaxPropertyBytes)
	}

	doc, err := ioutil.ReadAll(&buf)
	if err != nil {
		fmt.Errorf("failed reading compressed data for id %q: %v", id, err)
	}
	entity := &DatastoreEntity{Value: doc}

	wrote, err := client.Put(ctx, key, entity)
	if err != nil {
		fmt.Errorf("failed put for id %q: %v", id, err)
	}
	if ctx.Err() != nil {
		fmt.Errorf("context cancelled")
	}
	if !wrote.Equal(key) {
		fmt.Errorf("put for ID %q, returned key %q which doesn't match the request key", id, wrote)
	}
	fmt.Printf("Wrote id %s into %s as %s\n", id, kind, wrote)
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
		fmt.Printf("\nUsage:\n\t%s key.json [limit]\n\t%s key.json <action> <kind> <id>\n\n",
			path.Base(os.Args[0]), path.Base(os.Args[0]))
		fmt.Println(`Actions:
	delete <kind> <id>
	find <kind> <pattern>
	list <kind> <count>
	read <kind> <id | id1,..,idN>
	write <kind> <id> <filepath>
	`)
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

	if len(os.Args) > 4 {
		switch os.Args[2] {
		case "delete":
			deleteKey(ctx, client, os.Args[3], os.Args[4])
		case "filter":
			filter(ctx, client, os.Args[3], os.Args[4])
		case "find":
			findKeys(ctx, client, os.Args[3], os.Args[4])
		case "list":
			size, err := strconv.Atoi(os.Args[4])
			if err != nil {
				fmt.Errorf("\nFailed to convert size parameter\n")
			}
			listKeys(ctx, client, os.Args[3], size)
		case "read":
			if strings.Contains(os.Args[4], ",") {
				readMultiKey(ctx, client, os.Args[3], strings.Split(os.Args[4], ","))
			} else {
				readKey(ctx, client, os.Args[3], os.Args[4])
			}
		case "write":
			writeKey(ctx, client, os.Args[3], os.Args[4], os.Args[5])
		}
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
