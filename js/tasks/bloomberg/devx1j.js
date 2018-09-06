
// Presented problem to JKL and he suggested something like this:

function node(x, placeholder) {
    if (x.child) {
        console.log('child', x, x.child);
        if (x.next) { 
            node(x.child, x.next);
        } else {
            node(x.child, placeholder);
        }
        x.next = x.child;
    } else if (x.next) { 
        console.log('next', x, x.next);
        node(x.next, placeholder);
    } else {
        x.next = placeholder;
        if (x.next) node(x.next);
    }
}

// Using dict map to represent the linked lists for testing:

let nodes = {
    1: { next: 2 },
    2: { next: 3 },
    3: { next: 8, child: 4 },
    4: { next: 5 },
    5: { next: 6 },
    6: { child: 7 },
    8: { next: 10, child: 9 },
    9: { next: 10 },
   10: {},
}       

let line = node(nodes[1]);
//console.log(nodes);

 // But the dict is insufficient to test the method as is --- the method needs to be modified to handle
