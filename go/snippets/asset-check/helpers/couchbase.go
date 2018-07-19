package helpers

import (
	"fmt"

	"github.com/couchbase/gocb"
)

type BucketSpec struct {
	Name     string
	Password string
	Server   string
}
type Connection struct {
	ClusterConnection *gocb.Cluster
	SourceBucketSpec  BucketSpec
	SourceBucket      *gocb.Bucket
}

func (c *Connection) connectDB() (err error) {
	c.ClusterConnection, err = gocb.Connect(c.SourceBucketSpec.Server)
	if err != nil {
		return err
	}

	c.SourceBucket, err = c.ClusterConnection.OpenBucket(
		c.SourceBucketSpec.Name,
		c.SourceBucketSpec.Password,
	)
	if err != nil {
		return err
	}

	return nil
}

func (c *Connection) queryDB(config Config) (results []string, err error) {
	myQuery := gocb.NewN1qlQuery(config.Query)
	rows, err := c.SourceBucket.ExecuteN1qlQuery(myQuery, nil)
	if err != nil {
		return nil, fmt.Errorf("could not execute N1QL: %s\n", err)
	}
	var row interface{}
	for rows.Next(&row) {
		results = append(results, row.(map[string]interface{})["id"].(string))
	}
	if err = rows.Close(); err != nil {
		return nil, fmt.Errorf("could not get all the rows: %s\n", err)
	}
	return results, nil
}

func runQuery(config Config) ([]string, error) {
	sourceBucketSpec := BucketSpec{
		Name:     config.Bucket,
		Password: config.SASL,
		Server:   config.Couchbase,
	}
	c := &Connection{
		SourceBucketSpec: sourceBucketSpec,
	}
	c.connectDB()
	return c.queryDB(config)
}
