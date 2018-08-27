package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"reflect"
	"sort"
	"strconv"
	"strings"
)

func index(slice []int32, item int32) int {
    for i, _ := range slice {
        if slice[i] == item {
            return i
        }
    }
    return -1
}

// Complete the minimumSwaps function below.
func minimumSwaps(arr []int32) int32 {
    ord := make([]int32, len(arr))
    copy(ord, arr)
	sort.Slice(ord, func(i, j int) bool { return ord[i] < ord[j] })
	var swaps int32 = 0

    for !reflect.DeepEqual(arr, ord) {
        for i, a := range arr {
            if a != ord[i] {
                swaps++
                j := index(ord, a)
                arr[i] = arr[j]
                arr[j] = a
            }
        }
    }
                        
    return swaps
}

func main() {
	reader := bufio.NewReaderSize(os.Stdin, 1024*1024)

	stdout, err := os.Create(os.Getenv("OUTPUT_PATH"))
	checkError(err)

	defer stdout.Close()

	writer := bufio.NewWriterSize(stdout, 1024*1024)

	nTemp, err := strconv.ParseInt(readLine(reader), 10, 64)
	checkError(err)
	n := int32(nTemp)

	arrTemp := strings.Split(readLine(reader), " ")

	var arr []int32

	for i := 0; i < int(n); i++ {
		arrItemTemp, err := strconv.ParseInt(arrTemp[i], 10, 64)
		checkError(err)
		arrItem := int32(arrItemTemp)
		arr = append(arr, arrItem)
	}

	res := minimumSwaps(arr)

	fmt.Fprintf(writer, "%d\n", res)

	writer.Flush()
}

func readLine(reader *bufio.Reader) string {
	str, _, err := reader.ReadLine()
	if err == io.EOF {
		return ""
	}

	return strings.TrimRight(string(str), "\r\n")
}

func checkError(err error) {
	if err != nil {
		panic(err)
	}
}
