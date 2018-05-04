package http

import (
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
)

func getRoutes() *mux.Router {
	router := mux.NewRouter()
	router.HandleFunc("/status", getStatus).Methods("GET")
	router.HandleFunc("/get", getParams).Methods("GET")
	router.HandleFunc("/post", postBody).Methods("POST")
	return router
}

// mux method of handling requests
func multi() (err error) {
	if err := http.ListenAndServe(httpPort, getRoutes()); err != nil {
		fmt.Errorf("error with net/http listen/server: %v", err)
	}
	return nil
}
