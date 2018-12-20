package main

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path"

	"cloud.google.com/go/pubsub"
	"google.golang.org/api/iterator"
)

const (
	maxMessages = 10
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

func listSubscriptions(ctx context.Context, client *pubsub.Client, topic string) {
	// [START pubsub_list_topic_subscriptions]
	var subs []*pubsub.Subscription
	it := client.Topic(topic).Subscriptions(ctx)
	for {
		sub, err := it.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			log.Fatalf("Failed to list subscriptions\n")
		}
		fmt.Println(sub)
		subs = append(subs, sub)
	}
	// [END pubsub_list_topic_subscriptions]
}

func getMessage(ctx context.Context, client *pubsub.Client, sub string) {
	received := 0
	s := client.Subscription(sub)
	cctx, cancel := context.WithCancel(ctx)
	err := s.Receive(cctx, func(ctx context.Context, msg *pubsub.Message) {
		msg.Ack()
		fmt.Printf("\nMessage: %s\n   Time: %s\n   Attr: %s\n   Data: %s\n",
			msg.ID, msg.PublishTime, msg.Attributes, msg.Data)
		/*
			if readMessage(ctx, msg) {
				msg.Ack()
			} else {
				msg.Nack()
			}
		*/
		received++
		if received == maxMessages {
			cancel() // stop after receiving enough messages
		}
	})
	if err != nil {
		log.Fatalf("Failed to get %s message\n", sub)
	}
	//fmt.Println("No Error")
}

func putMessage(ctx context.Context, client *pubsub.Client, topic string, msgPath string) {
	// service account may not have permissions to create subscription
	/*
		sub, err := client.CreateSubscription(ctx, topic, pubsub.SubscriptionConfig{
			Topic:       client.Topic(topic),
			AckDeadline: 20 * time.Second,
		})
		if err != nil {
			log.Fatalf("\nfailed to create subscription for %q: %v", topic, err)
		}
		fmt.Printf("Created subscription: %v\n", sub)
	*/
	msg := fmt.Sprintf("Testing %s", topic)
	if msgPath != "" {
		tmp, err := ioutil.ReadFile(msgPath)
		if err != nil {
			log.Fatalf("Failed to read file %q: %v", msgPath, err)
		}
		msg = string(tmp)
		fmt.Println(msg)
	}
	hash := base64.StdEncoding.EncodeToString([]byte(msg))
	check, _ := base64.StdEncoding.DecodeString(hash)
	fmt.Println(hash, string(check))
	res := client.Topic(topic).Publish(ctx, &pubsub.Message{
		Data: []byte(msg),
	})
	fmt.Printf("Published %s to %q: %q\n", msgPath, topic, res)
}

func putTopic(ctx context.Context, client *pubsub.Client, topic string) {
	t := client.Topic(topic)
	// service account may not have permissions to check exists or create topic
	ok, err := t.Exists(ctx)
	if err != nil {
		log.Fatalf("Failed to check %q exists: %v", topic, err)
	}
	if ok {
		fmt.Printf("\nTopic %s already exists!\n", topic)
		return
	}

	t, err = client.CreateTopic(ctx, topic)
	if err != nil {
		log.Fatalf("\nfailed to create the topic %q: %v", topic, err)
	}
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
	client, err := pubsub.NewClient(ctx, projectID)
	if err != nil {
		log.Fatalf("Failed to connect to pubsub\n")
	}

	topic := "sports-aggregation"
	//listSubscriptions(ctx, client, topic)
	//putTopic(ctx, client, topic)

	msgPath := ""
	if len(os.Args) > 2 {
		msgPath = os.Args[2]
	}
	fmt.Println(topic, msgPath)
	putMessage(ctx, client, topic, msgPath)

	//putMessage(ctx, client, topic, "")
	sub := "sports-subscription"
	getMessage(ctx, client, sub)
}
