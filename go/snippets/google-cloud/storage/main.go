package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"path"
	"strings"
	"time"

	"cloud.google.com/go/storage"
	"google.golang.org/api/iterator"
)

/*
const Storage = require('@google-cloud/storage');
// authenticate using ONE (not ALL) of the following methods:

// setting environment variable GOOGLE_APPLICATION_CREDENTIALS=/path/to/service_account.json
const storage = new Storage();

// explicitly specifying service_account credentials file
const storage = new Storage({
    keyFilename: '/path/to/service_account.json'
});

// passing in credentials as JSON
const storage = new Storage({
    credentials: {
        type: "service_account",
        project_id: process.env.PROJECT_ID,
        private_key_id: process.env.PRIVATE_KEY_ID,
        private_key: process.env.PRIVATE_KEY,
        client_email: "{USER}@{PROJECT}.iam.gserviceaccount.com",
        client_id: process.env.CLIENT_ID,
        auth_uri: "https://accounts.google.com/o/oauth2/auth",
        token_uri: "https://accounts.google.com/o/oauth2/token",
        auth_provider_x509_cert_url: "https://www.googleapis.com/oauth2/v1/certs",
        client_x509_cert_url: "https://www.googleapis.com/robot/v1/metadata/x509/{USER}%40{PROJECT}.iam.gserviceaccount.com"
    }
});


var bucket = storage.bucket(process.env.BUCKET_NAME);
bucket.getFiles((err, files) => {
    if (err) {
        console.log('ERROR', err);
    } else {
        files.forEach((f) => {
            var data = '';
            var remoteReadStream = bucket.file(f.name).createReadStream();
            remoteReadStream
                .on('data', function (chunk) {
                    data += chunk.toString();
                    //console.log('CHUNK:', chunk);
                })
                .on('end', function () {
                    console.log('\nFILE:', f.name)
                    console.log(data)
                });
        });
    }
});
*/

/*
ctx := context.Background()
client, err := storage.NewClient(ctx)
if err != nil {
    // TODO: Handle error.
}

client, err := storage.NewClient(ctx, option.WithoutAuthentication())

bkt := client.Bucket(bucketName)

if err := bkt.Create(ctx, projectID, nil); err != nil {
    // TODO: Handle error.
}

attrs, err := bkt.Attrs(ctx)
if err != nil {
    // TODO: Handle error.
}
fmt.Printf("bucket %s, created at %s, is located in %s with storage class %s\n",
    attrs.Name, attrs.Created, attrs.Location, attrs.StorageClass)

obj := bkt.Object("data")
// Write something to obj.
// w implements io.Writer.
w := obj.NewWriter(ctx)
// Write some text to obj. This will either create the object or overwrite whatever is there already.
if _, err := fmt.Fprintf(w, "This object contains text.\n"); err != nil {
    // TODO: Handle error.
}
// Close, just like writing a file.
if err := w.Close(); err != nil {
    // TODO: Handle error.
}

// Read it back.
r, err := obj.NewReader(ctx)
if err != nil {
    // TODO: Handle error.
}
defer r.Close()
if _, err := io.Copy(os.Stdout, r); err != nil {
    // TODO: Handle error.
}
// Prints "This object contains text."

objAttrs, err := obj.Attrs(ctx)
if err != nil {
    // TODO: Handle error.
}
fmt.Printf("object %s has size %d and can be read using %s\n",
    objAttrs.Name, objAttrs.Size, objAttrs.MediaLink)
*/
func create(ctx context.Context, client *storage.Client, projectID string, bucketName string) {
	bkt := client.Bucket(bucketName)
	if err := bkt.Create(ctx, projectID, nil); err != nil {
		fmt.Printf("\nUnable to create %s bucket: %+v\n", bucketName, err)
	} else {
		fmt.Printf("Created bucket %s\n", bucketName)
	}
}

func attr(ctx context.Context, client *storage.Client, bucketName string, objectName string) {
	bkt := client.Bucket(bucketName)
	if objectName == "" {
		attrs, err := bkt.Attrs(ctx)
		if err != nil {
			fmt.Printf("\nUnable to get %s bucket attrs: %+v\n", bucketName, err)
		}
		fmt.Printf("bucket %s, created at %s, is located in %s with storage class %s\n",
			attrs.Name, attrs.Created, attrs.Location, attrs.StorageClass)
	} else {
		obj := bkt.Object(objectName)
		objAttrs, err := obj.Attrs(ctx)
		if err != nil {
			fmt.Printf("\nUnable to get %s object attrs: %+v\n", objectName, err)
		}
		fmt.Printf("object %s has size %d and can be read using %s\n",
			objAttrs.Name, objAttrs.Size, objAttrs.MediaLink)
	}
}

// https://github.com/googleapis/google-cloud-go/blob/master/storage/acl.go#L53
type ACLRule struct {
	Entity string
	Owner  string
}

// https://github.com/googleapis/google-cloud-go/blob/master/storage/storage.go#L650
type ObjectAttrs struct {
	Bucket                  string
	Name                    string
	ContentType             string
	ContentLanguage         string
	CacheControl            string
	EventBasedHold          bool
	TemporaryHold           bool
	RetentionExpirationTime time.Time
	ACL                     []ACLRule
	PredefinedACL           string
	Owner                   string
	Size                    int64
	ContentEncoding         string
	ContentDisposition      string
	MD5                     []byte
	CRC32C                  uint32
	MediaLink               string
	Metadata                map[string]string
	Generation              int64
	Metageneration          int64
	StorageClass            string
	Created                 time.Time
	Deleted                 time.Time
	Updated                 time.Time
	CustomerKeySHA256       string
	KMSKeyName              string
	Prefix                  string
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

func list(ctx context.Context, client *storage.Client, bucketName string) {
	it := client.Bucket(bucketName).Objects(ctx, nil)
	for {
		batchErr := BatchError{Errors: make(map[string]error)}
		id, err := it.Next()
		if err != nil {
			if err == iterator.Done {
				break
			}
			batchErr.Errors[id.Name] = fmt.Errorf("Error fetching next entity: %v", err)
			continue
		}
		fmt.Printf("\nBucket: %s\nName: %s\nContent-Type: %s\nOwner: %s\nSize: %v\nStorageClass: %s\nCreated: %q\n",
			id.Bucket, id.Name, id.ContentType, id.Owner, id.Size, id.StorageClass, id.Created)
		fmt.Printf("MD5: %v\nCRC32C: %v\nMediaLink: %s\nACL: %+v\n",
			id.MD5, id.CRC32C, id.MediaLink, id.ACL)
	}
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

func read(ctx context.Context, client *storage.Client, bucketName string, objectName string) {
	bkt := client.Bucket(bucketName)
	obj := bkt.Object(objectName)
	r, err := obj.NewReader(ctx)
	if err != nil {
		fmt.Printf("\nUnable to initiate reader: %+v\n", err)
	}
	defer r.Close()
	if _, err := io.Copy(os.Stdout, r); err != nil {
		fmt.Printf("\nUnable to read %s: %+v\n", objectName, err)
	}
}

func write(ctx context.Context, client *storage.Client, bucketName string, objectName string) {
	bkt := client.Bucket(bucketName)
	obj := bkt.Object(objectName)
	w := obj.NewWriter(ctx)
	fmt.Println("Type in some text, EOF (^D) when finished:")
	if _, err := io.Copy(w, os.Stdin); err != nil {
		fmt.Printf("\nUnable to write to %s: %+v\n", objectName, err)
	}
	if err := w.Close(); err != nil {
		fmt.Printf("\nUnable to close %s: %+v\n", objectName, err)
	}
}

func delete(ctx context.Context, client *storage.Client, bucketName string, objectName string) {
	bkt := client.Bucket(bucketName)
	if err := bkt.Object(objectName).Delete(ctx); err != nil {
		fmt.Printf("\nUnable to delete %s: %+v\n", objectName, err)
	}
	fmt.Printf("\nDeleted object %s successfully\n", objectName)
}

func main() {
	if len(os.Args) < 2 {
		fmt.Printf("\nUsage:\n\t%s key.json [limit]\n\t%s key.json <action> <object...>\n\n",
			path.Base(os.Args[0]), path.Base(os.Args[0]))
		fmt.Println(`Actions:
	create <bucket>
	list <bucket>
	attr <bucket> [<object>]
	read <bucket> <object>
	write <bucket> <object>
	delete <bucket> <object>
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
	//client, err := storage.NewClient(ctx, option.WithoutAuthentication())
	client, err := storage.NewClient(ctx) // aobve ^ for public data
	if err != nil {
		fmt.Errorf("\nFailed to connect to storage\n")
	}

	if len(os.Args) > 3 {
		switch os.Args[2] {
		case "attr":
			if len(os.Args) > 4 {
				attr(ctx, client, os.Args[3], os.Args[4])
			} else {
				attr(ctx, client, os.Args[3], "")
			}
		case "create":
			create(ctx, client, projectID, os.Args[3])
		case "list":
			list(ctx, client, os.Args[3])
		case "read":
			read(ctx, client, os.Args[3], os.Args[4])
		case "write":
			write(ctx, client, os.Args[3], os.Args[4])
		case "delete":
			delete(ctx, client, os.Args[3], os.Args[4])
		}
	}
}
