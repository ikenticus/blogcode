
// Modifying JKL function to handle dict

function loop(nodes, x, queue) {
    if (nodes[x].child) {
        if (nodes[x].next) { 
            loop(nodes, nodes[x].child, nodes[x].next);
        } else {
            loop(nodes, nodes[x].child, queue);
        }
        nodes[x].next = nodes[x].child;
    } else if (nodes[x].next) { 
        loop(nodes, nodes[x].next, queue);
    } else if (queue) {
        loop(nodes, queue);
        if (nodes[x].next != queue)
            nodes[x].next = queue;
    }
    delete nodes[x].child;
    return nodes;
}

// Using dict map to represent the linked lists for testing:

let nodes = {
    1: { next: 2 },
    2: { next: 3 },
    3: { next: 8, child: 4 },
    4: { next: 5 },
    5: { next: 6 },
    6: { child: 7 },
    7: {},
    8: { next: 10, child: 9 },
    9: {},
   10: {},
}       

console.log('OLD:');
console.log(nodes);
let lines = loop(nodes, 1);
console.log('NEW:');
console.log(lines);

