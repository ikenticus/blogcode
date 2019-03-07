package main

import (
	"database/sql"
	"fmt"
	"io/ioutil"

	"github.com/joho/sqltocsv"
	_ "github.com/lib/pq"
)

func main() {
	connStr := `port=5439 dbname=db user=user password=pass host=postgresql`
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	}

	rows, err := db.Query("SELECT TOP 10 * FROM pages")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	}
	defer rows.Close()

	err = sqltocsv.WriteFile("testquery.csv", rows)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	}

	rows, err = db.Query("SELECT TOP 1 id FROM pages")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	}
	defer rows.Close()

	var value string
	for rows.Next() {
		if err = rows.Scan(&value); err != nil {
			fmt.Printf("Error: %v\n", err)
		}
		//fmt.Println(value)
		err = ioutil.WriteFile("testvalue.csv", []byte(value), 0644)
		if err != nil {
			fmt.Printf("Error: %v\n", err)
		}
	}
}
