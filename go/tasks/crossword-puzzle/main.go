package main

import (
    "bufio"
    "fmt"
    "io"
    "os"
    //"strconv"
    "strings"
)

func check(crossword []string, word string) [][]int {
    var slots [][]int
    length := len(word)
    for row := 0; row < 10; row++ {
        for col := 0; col < 10; col++ {
            validH := true
            validV := true
            for w := 0; w < length; w++ {
                if col <= 10 - length {
                    c := crossword[row][col + w]
                    if c != '-' && c != word[w] {
                        validH = false                                            
                    }
                }
                if row <= 10 - length {
                    r := crossword[row + w][col]
                    if r != '-' && r != word[w] {
                        validV = false                                            
                    }
                }
            }

            if validH && col <= 10 - length {
                slots = append(slots, []int{row, col, 0})
            }
            if validV && row <= 10 - length {
                slots = append(slots, []int{row, col, 1})  
            }
        }
    }
    return slots
}

func writePuzzle(crossword []string, word string, slot []int, empty byte) {
    row, col, dir := slot[0], slot[1], slot[2]
    for w := 0; w < len(word); w++ {
        letter := empty
        if letter == 'w' {
            letter = word[w]
        }
        if dir == 0 {
            //crossword[row][col + w] = letter
            crossword[row] = crossword[row][:col+w] + string(letter) + crossword[row][col+w+1:]
        } else {
            //crossword[row + w][col] = letter
            crossword[row+w] = crossword[row+w][:col] + string(letter) + crossword[row+w][col+1:]
        }
    }
}

// Complete the crosswordPuzzle function below.
func crosswordPuzzle(crossword []string, words []string) []string {
    fmt.Println(strings.Join(crossword, "\n"))
    if len(words) == 0 {
        return crossword
    }
    word, words := words[0], words[1:]
    slots := check(crossword, string(word))
    for s := 0; s < len(slots); s++  {
        writePuzzle(crossword, string(word), slots[s], 'w')
        board := crosswordPuzzle(crossword, words)
        if len(board) > 0 {
            return board
        } else {
            writePuzzle(crossword, word, slots[s], '-')
        }
    }
    words = append(words, word)
    return []string{}
}

func main() {
    reader := bufio.NewReaderSize(os.Stdin, 1024 * 1024)

    stdout, err := os.Create(os.Getenv("OUTPUT_PATH"))
    checkError(err)

    defer stdout.Close()

    writer := bufio.NewWriterSize(stdout, 1024 * 1024)

    var crossword []string

    for i := 0; i < 10; i++ {
        crosswordItem := readLine(reader)
        crossword = append(crossword, crosswordItem)
    }

    words := strings.Split(readLine(reader), ";")

    result := crosswordPuzzle(crossword, words)

    for i, resultItem := range result {
        fmt.Fprintf(writer, "%s", resultItem)

        if i != len(result) - 1 {
            fmt.Fprintf(writer, "\n")
        }
    }

    fmt.Fprintf(writer, "\n")

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

