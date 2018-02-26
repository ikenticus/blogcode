package main

import (
	"fmt"
	"os"
	"sync"
	"time"

	"github.com/GannettDigital/cs-olympics-ingestor/monitor/medalCountry"
	"github.com/GannettDigital/cs-olympics-ingestor/monitor/medalTable"
	"github.com/GannettDigital/cs-olympics-ingestor/monitor/schedule"
	"github.com/GannettDigital/cs-olympics-ingestor/monitor/scheduleExtended"
)

func main() {

	ticker := time.NewTicker(60000 * time.Millisecond)
/*
	// run on the ticker schedule
	for range ticker.C {

		wg := new(sync.WaitGroup)
		mismatchErrors := make(chan error)

		// validate schedule
		wg.Add(1)
		go func() {
			defer wg.Done()

			for _, v := range schedule.Do() {
				mismatchErrors <- v
			}

		}()

		// validate schedule-extended
		wg.Add(1)
		go func() {
			defer wg.Done()

			mismatchErrors <- scheduleExtended.Do()
		}()

		// validate medaltable
		wg.Add(1)
		go func() {
			defer wg.Done()

			mismatchErrors <- medalTable.Do()
		}()

		// validate medal-country
		wg.Add(1)
		go func() {
			defer wg.Done()

			// TODO: just make medalTable.GetMedalTableNocs() return an []medalCountry.NocMatcher{}
			// so we don't have to process a new list
			nm := []medalCountry.NocMatcher{}
			for _, v := range medalTable.GetMedalTableNocs() {
				nm = append(nm, medalCountry.NocMatcher{
					ID:    v.NocID,
					Short: v.NocShort,
				})
			}

			for _, v := range medalCountry.Do(nm) {
				mismatchErrors <- v
			}

		}()

		// once everyone finished up, close our errors channel so the collector loop
		// below knows to finish up
		go func() {
			wg.Wait()
			close(mismatchErrors)
		}()

		// collect results of test
		var runErrorList []error
		for v := range mismatchErrors {
			if v != nil {
				runErrorList = append(runErrorList, v)
			}
		}

		processResults(nra, runErrorList)

		fmt.Println("------------------------------")
		*/
	}
}

// processResults - check for errors and report to newrelic if any were found
func processResults(nra newrelicAgent.Application, errorList []error) {

	if len(errorList) == 0 {
		fmt.Println("Success - no mismatches")
		return
	}

	for _, v := range errorList {
		fmt.Println(v.Error())
	}
}
