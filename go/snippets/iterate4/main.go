package main

import "fmt"

type Node struct {
    label int
    children []Node
}

func (self *Node) String() string {
    return fmt.Sprintf("<%v %v>", self.label, self.children)
}

func (self *Node) PostOrder() (<-chan int) {
    ch := make(chan int)
    go func(yield chan<- int) {
        var iter func(node *Node)
        iter = func(node *Node) {
            if node == nil {
                return
            }
            for _, child := range node.children {
                iter(&child)
            }
            yield<-node.label
        }
        iter(self)
        close(yield)
    }(ch)
    return ch
}

func main() {
    root := &Node{5, []Node{Node{3, []Node{Node{1, nil}, Node{4, nil}}}, Node{7, []Node{Node{6, nil}, Node{10, []Node{Node{8, nil}, Node{12, nil}}}}}}}
    fmt.Println(root)
    for i := range root.PostOrder() {
        fmt.Println(i)
    }
}
