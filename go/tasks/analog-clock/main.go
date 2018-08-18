/*
   Task: Analog Clock
*/
package main

import (
	"fmt"
	"os"
	"path"
	"strconv"
	"strings"
)

func usage() {
	fmt.Printf("Calculate the angle betwwen hour and minute hands\nUsage: %s <HH:MM>'\n", path.Base(os.Args[0]))
}

func degree(clock string) int {
	hands := strings.Split(clock, ":")

	min, err := strconv.Atoi(hands[1])
	if err == nil {
		min = min * 6
	}

	hour, err := strconv.Atoi(hands[0])
	if err == nil {
		hour = (hour%12)*30 + (min / 12)
	}

	if hour < min {
		return hour + 360 - min
	} else {
		return hour - min
	}
}

func main() {
	if len(os.Args) < 2 {
		usage()
		os.Exit(1)
	}
	fmt.Println(degree(os.Args[1]), "degrees")
}
