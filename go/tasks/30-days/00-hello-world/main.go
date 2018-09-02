package main
import (
    "bufio"
    "fmt"
    "os"
)

func main() {
    //Enter your code here. Read input from STDIN. Print output to STDOUT
    reader := bufio.NewReader(os.Stdin)
    inputString, _ := reader.ReadString('\n')
    fmt.Println("Hello, World.\n" + inputString)
}
