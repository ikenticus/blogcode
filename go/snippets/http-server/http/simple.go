package http

import (
	"fmt"
	"net/http"
)

// simple method of using just net/http to handle requests
func simple() (err error) {
	http.HandleFunc("/status", getStatus)
	http.HandleFunc("/get", getParams)
	http.HandleFunc("/post", postBody)
	if err := http.ListenAndServe(httpPort, nil); err != nil {
		fmt.Errorf("error with net/http listen/server: %v", err)
	}
	return nil
}
