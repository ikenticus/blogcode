
// Attempting to build a linked list using HackerRank example, but failing to do so in the allocated timeframe:

const LinkedListNode = class {
    constructor(x) {
        this.id = x;
        this.next = null;
        this.child = null;
    }
}

const LinkedList = class {
    constructor() {
        this.head = null;
        this.tail = null;
    }
    addNode(x) {
        const node = new LinkedListNode(x);
        if (this.head == null) {
            this.head = node;
        } else {
            this.tail.next = node;
        }
        this.tail = node;
    }
}

function node(x) {
    if (!x.child && !x.next) { // base case
        return x;
    } else { // recurse case
        if (x.child) {
            x.next = node(x.child);
        } else if (x.next) { 
            x.next = node(x.next);
        }
    }
}

function printList(head) {
    while (head.id) {
        console.log(head.id);
        head.id = head.next.id;
        head.next = head.next.next;
    }
}

function main() {
    let linked_list = new LinkedList();
    for (let i = 1; i<= 10; i++) {
        linked_list.addNode(i);
    }
    printList(linked_list.head);
}

// Coicidence?  But after running it once and discovering that it printed nothing,
// Kunal suggested that we end the interview but I could attempt to solve it in my own time

