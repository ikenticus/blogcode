/*
   Task: Fibonacci
*/
package main

import (
	"fmt"
	"log"
	"os"
	"path"
	"strconv"
)

func usage() {
	fmt.Printf("Calculate the Nth Fibonacci number\nUsage: %s <n>\n", path.Base(os.Args[0]))
}

func main() {
	SEQ := []int{0, 1}
	if len(os.Args) < 2 {
		usage()
		os.Exit(1)
	} else if os.Args[1] <= "1" {
		fmt.Printf("F(%s) = %s\n", os.Args[1], os.Args[1])
		if os.Args[1] < "1" {
			SEQ = SEQ[:len(SEQ)-1]
		}
	} else {
		NUM, err := strconv.Atoi(os.Args[1])
		if err != nil {
			log.Fatalf("unable to convert %s to integer\n", os.Args[1])
		}
		if NUM > 1 {
			for i := 2; i < NUM+1; i++ {
				SEQ = append(SEQ, SEQ[i-1]+SEQ[i-2])
			}
		}
		SIZE := len(SEQ) - 1
		fmt.Printf("F(%d) = %d\n", NUM, SEQ[SIZE])
	}
	fmt.Println("Sequence:", SEQ)
}
