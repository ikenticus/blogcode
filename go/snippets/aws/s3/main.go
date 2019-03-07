package main

import (
	"fmt"
	"os"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3/s3manager"
)

const (
	bucketName = "canvas-warehouse"
	fileName   = "testfile"
	regionName = "us-east-1"
)

func main() {
	// The session the S3 Uploader will use
	sess := session.Must(session.NewSession(&aws.Config{
		Region: aws.String(regionName),
	}))

	// Create an uploader with the session and default options
	uploader := s3manager.NewUploader(sess)

	f, err := os.Open(fileName)
	if err != nil {
		fmt.Printf("failed to open file %q, %v\n", fileName, err)
	}

	// Upload the file to S3.
	result, err := uploader.Upload(&s3manager.UploadInput{
		Bucket:    aws.String(bucketName),
		Key:       aws.String(fileName),
		Body:      f,
		GrantRead: aws.String("uri=http://acs.amazonaws.com/groups/global/AllUsers"),
	})
	if err != nil {
		fmt.Printf("failed to upload file, %v\n", err)
	}
	fmt.Printf("file uploaded to, %s\n", result.Location)
}
