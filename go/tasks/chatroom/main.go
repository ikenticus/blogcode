/*
   Task: Chatroom
*/
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"os"
	"path"
	"sort"
	"strconv"
	"strings"

	humanize "github.com/dustin/go-humanize"
)

type Info struct {
	Words []string
	Count int
}

type User struct {
	Name  string
	Count int
}

func usage() {
	fmt.Printf("Display chatroom statistics\nUsage: %s <chatfile> <n>\n", path.Base(os.Args[0]))
}

func parse(data string) (stat map[string]Info) {
	if stat == nil {
		stat = make(map[string]Info)
	}
	lines := strings.Split(data, "\n")
	for _, c := range lines {
		if len(c) > 0 {
			s := strings.Split(c, ":")
			user, chat := strings.Trim(s[0], " "), strings.Trim(strings.Join(s[1:], ":"), " ")

			t := stat[user]
			if stat[user].Words == nil {
				stat[user] = Info{}
			}
			t.Words = append(stat[user].Words, strings.Split(chat, " ")...)
			t.Count = len(t.Words)
			stat[user] = t
		}
	}
	return stat
}

func output(order string, stat map[string]Info) {
	most := true
	mostWord := "most"
	if strings.HasPrefix(order, "-") {
		most = false
		mostWord = "least"
	}

	rank, err := strconv.Atoi(order)
	if err != nil {
		log.Fatal(err)
	}
	rank = int(math.Abs(float64(rank)))

	var user []User
	for s := range stat {
		user = append(user, User{s, stat[s].Count})
	}
	if most {
		sort.Slice(user, func(a, b int) bool { return user[a].Count > user[b].Count })
	} else {
		sort.Slice(user, func(a, b int) bool { return user[a].Count < user[b].Count })
	}

	if rank == 0 {
		fmt.Printf("List of %s wordy users:\n", mostWord)
		for u := range user {
			fmt.Printf("%5d %s\n", user[u].Count, user[u].Name)
		}
	} else {
		fmt.Printf("The %s %s wordy user is (%s) with %d words\n", humanize.Ordinal(rank), mostWord, user[rank-1].Name, user[rank-1].Count)
	}
}

func main() {
	if len(os.Args) < 3 {
		usage()
		os.Exit(1)
	}

	chatfile := os.Args[1]
	chats, err := ioutil.ReadFile(chatfile)
	if err != nil {
		log.Fatal(err)
	}

	stat := parse(string(chats))
	output(os.Args[2], stat)
}
