package main

import (
    "bufio"
    "fmt"
    "io"
    "os"
    "strconv"
    "strings"
)

// Complete the hourglassSum function below.
func hourglassSum(arr [][]int32) int32 {
    //fmt.Println(arr)
    var hours [][]int32
    for r, _ := range arr[:len(arr)-2] {
        for c, _ := range arr[r][:len(arr)-2] {
            hours = append(hours, []int32{
                arr[r][c], arr[r][c+1], arr[r][c+2],
                            arr[r+1][c+1],
                arr[r+2][c], arr[r+2][c+1], arr[r+2][c+2],
            })
        }
    }
    //fmt.Println(hours)

    var max int32 = -100 // do not initialize to zero for negative cases
    var sums []int32
    for r, _ := range hours {
        //fmt.Println(sums, r)
        sums = append(sums, 0)
        for c, _ := range hours[r] {
            sums[r] += hours[r][c]
        }
        if sums[r] > max {
            max = sums[r]
        }
    }

    return max
}

func main() {
    reader := bufio.NewReaderSize(os.Stdin, 1024 * 1024)

    stdout, err := os.Create(os.Getenv("OUTPUT_PATH"))
    checkError(err)

    defer stdout.Close()

    writer := bufio.NewWriterSize(stdout, 1024 * 1024)

    var arr [][]int32
    for i := 0; i < 6; i++ {
        arrRowTemp := strings.Split(readLine(reader), " ")

        var arrRow []int32
        for _, arrRowItem := range arrRowTemp {
            arrItemTemp, err := strconv.ParseInt(arrRowItem, 10, 64)
            checkError(err)
            arrItem := int32(arrItemTemp)
            arrRow = append(arrRow, arrItem)
        }

        if len(arrRow) != int(6) {
            panic("Bad input")
        }

        arr = append(arr, arrRow)
    }

    result := hourglassSum(arr)

    fmt.Fprintf(writer, "%d\n", result)

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

