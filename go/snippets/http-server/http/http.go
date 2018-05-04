// Package http just creates the server to listen to requests
package http

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"sort"
	"strings"
)

const httpPort = ":8080"

func getStatus(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Server is running")
}

func getParams(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	for k, v := range r.Form {
		vlist := strings.Split(strings.Join(v, ""), ",")
		sort.Strings(vlist)
		fmt.Fprintf(w, "Sorted (%s): %s\n", k, vlist)
	}
}

func postBody(w http.ResponseWriter, r *http.Request) {
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "unable to read body", http.StatusBadRequest)
	}
	fmt.Printf("%v\n", string(body))
	vlist := strings.Split(string(body), "\n")
	sort.Strings(vlist)
	fmt.Fprintf(w, "Sorted body:\n%s\n", strings.Join(vlist, "\n"))
}

func Server() (err error) {
	fmt.Println("HTTP Server starting on port", httpPort)
	//return simple()
	return multi()
}
