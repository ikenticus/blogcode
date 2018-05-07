package main

import (
	"fmt"
	"reflect"
	"strings"
)

type Types struct {
	a int
	b string
	c bool
	d []int
	e []string
	f []interface{}
	g interface{}
	h map[string]int
}

func main() {
	a := 1
	b := "one"
	c := true
	d := []int{1, 2, 3, 4}
	e := []string{"one", "two", "three"}
	f := make([]interface{}, len(e))
	g := Types{a: 9, b: "nine"}

	fmt.Println(strings.Repeat("-", 99), "\nTypeOf(x):")
	fmt.Println(reflect.TypeOf(a)) // int
	fmt.Println(reflect.TypeOf(b)) // string
	fmt.Println(reflect.TypeOf(c)) // bool
	fmt.Println(reflect.TypeOf(d)) // []int
	fmt.Println(reflect.TypeOf(e)) // []string
	fmt.Println(reflect.TypeOf(f)) // []interface {}
	fmt.Println(reflect.TypeOf(g)) // main.Types

	fmt.Println(strings.Repeat("-", 99), "\nValueOf(x):")
	fmt.Println(reflect.ValueOf(a)) // 1
	fmt.Println(reflect.ValueOf(b)) // one
	fmt.Println(reflect.ValueOf(c)) // true
	fmt.Println(reflect.ValueOf(d)) // [1, 2, 3, 4]
	fmt.Println(reflect.ValueOf(e)) // [one two three]
	fmt.Println(reflect.ValueOf(f)) // [<nil> <nil> <nil>]
	fmt.Println(reflect.ValueOf(g)) // {9 nine false [] [] [] <nil> map[]}

	fmt.Println(strings.Repeat("-", 99), "\nValueOf(x).Kind():")
	fmt.Println(reflect.ValueOf(a).Kind()) // int
	fmt.Println(reflect.ValueOf(b).Kind()) // string
	fmt.Println(reflect.ValueOf(c).Kind()) // bool
	fmt.Println(reflect.ValueOf(d).Kind()) // slice
	fmt.Println(reflect.ValueOf(e).Kind()) // slice
	fmt.Println(reflect.ValueOf(f).Kind()) // slice
	fmt.Println(reflect.ValueOf(g).Kind()) // struct

	fmt.Println(strings.Repeat("-", 99), "\nValueOf(x).Type():") // same as TypeOf(x)
	fmt.Println(reflect.ValueOf(a).Type())                       // int
	fmt.Println(reflect.ValueOf(b).Type())                       // string
	fmt.Println(reflect.ValueOf(c).Type())                       // bool
	fmt.Println(reflect.ValueOf(d).Type())                       // []int
	fmt.Println(reflect.ValueOf(e).Type())                       // []string
	fmt.Println(reflect.ValueOf(f).Type())                       // []interface {}
	fmt.Println(reflect.ValueOf(g).Type())                       // main.Types

	fmt.Println(strings.Repeat("-", 99), "\nValueOf(&x):")
	fmt.Println(reflect.ValueOf(&a)) // 0xc4200140a8
	fmt.Println(reflect.ValueOf(&b)) // 0xc42000e1d0
	fmt.Println(reflect.ValueOf(&c)) // 0xc4200140b0
	fmt.Println(reflect.ValueOf(&d)) // &[1, 2, 3, 4]
	fmt.Println(reflect.ValueOf(&e)) // &[one two three]
	fmt.Println(reflect.ValueOf(&f)) // &[<nil> <nil> <nil>]
	fmt.Println(reflect.ValueOf(&g)) // &{9 nine false [] [] [] <nil> map[]}

	fmt.Println(strings.Repeat("-", 99))
}
