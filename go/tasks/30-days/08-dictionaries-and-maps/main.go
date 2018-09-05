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
    scanner.Scan()
    n, err := strconv.Atoi(scanner.Text())
    checkError(err)
    
    entry := make(map[string]string)
    for i := 0; i < n; i++ {
        scanner.Scan()
        e := strings.Split(scanner.Text(), " ");
        entry[e[0]] = e[1];
    }
    
    for scanner.Scan() {
        q := scanner.Text()
        phone, ok := entry[q]
        if ok {
            fmt.Printf("%s=%s\n", q, phone)
        } else {
            fmt.Println("Not found")
        }
    }
}

func checkError(err error) {
    if err != nil {
        panic(err)
    }
}
