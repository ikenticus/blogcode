// Exploring the Golang switch/case differences
package main

import (
	"fmt"
)

type TypeA struct {
	Num  int
	Word string
}

func (this *TypeA) test() {
	fmt.Println("TestA", this)
}

type TypeB struct {
	Num  int
	Word string
}

func (this *TypeB) test() {
	fmt.Println("TestB", this)
}

type TypeC struct {
	Num  int
	Word string
}

func (this *TypeC) test() {
	fmt.Println("TestC", this)
}

var Types = map[string]interface{}{
	"a": TypeA{Num: 1, Word: "one"},
	"b": TypeB{Num: 2, Word: "two"},
	"c": TypeC{Num: 3, Word: "tre"},
}

func main() {
	words := []string{"Alpha", "beta", "Charlie", "delta", "Esso", "foxtrot", "Golf", "hotel"}

	for _, word := range words {
		fmt.Printf("First character of %s is %s (%d)\n", word, word[0:1], word[0])
		first := string([]rune(word)[0])
		switch first {
		case "A", "B", // testing fallthrough
			"C", "D", "E",
			"F", "G", "H":
			fmt.Println("Begins with UPPER:", word)
		default:
			fmt.Println("Begins with lower:", word)
		}
	}

	for key, val := range Types {
		var foo interface{}
		foo = Types[key]
		fmt.Println("LOOP", key, val, foo)

		// https://stackoverflow.com/questions/40575033/golang-multiple-case-in-type-switch
		//bar := foo.(type) // use of .(type) outside type switch
		switch bar := foo.(type) {
		//case TypeA, TypeC: //bar.test undefined (type interface {} is interface with no methods)
		case TypeA:
			bar.test()
		case TypeB:
			bar.test()
		default:
			fmt.Println("Default")
		}
	}

	/*
	   switch reflect.TypeOf(fake.) {
	       case reflect.String:
	           fmt.Println("")
	   }
	*/
}
