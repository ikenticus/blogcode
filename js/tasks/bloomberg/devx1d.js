
// Modifying to handle more complex dict
/*

  [1] -> [2] -> [8] -> [10]
          |      |
          |     [9]
          |
         [3] -> [4] -> [7]
                 |
                [5] -> [6]

*/


function loop(x, queue=[]) {
    if (x.child) {
        if (x.next) queue.push(x.next);
        loop(nodes[x.child], queue);
        x.next = x.child;
        delete x.child;
    } else if (x.next) { 
        loop(nodes[x.next], queue);
    } else if (queue) {
        x.next = queue.pop();
        if (x.next) loop(nodes[x.next], queue);
    }
    return nodes;
}

// Using dict map to represent the linked lists for testing:

let nodes = {
    1: { next: 2 },
    2: { next: 8, child: 3 },
    3: { next: 4 },
    4: { next: 7, child: 5 },
    5: { next: 6 },
    6: {},
    7: {},
    8: { next: 10, child: 9 },
    9: {},
    10: {}
}       

console.log('OLD:');
console.log(nodes);
let lines = loop(nodes[1]);
console.log('NEW:');
console.log(lines);

