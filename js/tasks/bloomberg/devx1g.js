
// Attempting to build a working flat linked list

const LinkedListNode = class {
    constructor(x) {
        this.id = x;
        this.next = null;
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

function printList(head) {
    while (head.id) {
        console.log(head.id);
        head.id = head.next ? head.next.id : null;
        head.next = head.next ? head.next.next : null;
    }
}

function main() {
    let nodes = new LinkedList();
    for (let i = 1; i<= 10; i++) {
        nodes.addNode(i);
    }

    console.log(JSON.stringify(nodes, null, 4));
    console.log(nodes);
    printList(nodes.head);
}

main();
