package main
import (
    "bufio"
    "fmt"
    "os"
    "strconv"
    "strings"
)

func main() {
    //Enter your code here. Read input from STDIN. Print output to STDOUT
    scanner := bufio.NewScanner(os.Stdin)
    var T int
    scanner.Scan()
    T, _ = strconv.Atoi(scanner.Text())
    for i := 0; i < T; i++ {
        output := []string{"", ""}
        scanner.Scan()
        S := scanner.Text()
        for c := 0; c < len(S); c++ {
            if c % 2 == 0 {
                output[0] += string(S[c])
            } else {
                output[1] += string(S[c])
            }
        }
        fmt.Println(strings.Join(output, " "))
    }
}
