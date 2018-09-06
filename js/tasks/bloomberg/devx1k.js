
// Modified version from JKL

let linkedlist = {
    '1': { next: '2' },
    '2': { next: '3' },
    '3': { next: '8', child: '4' },
    '4': { next: '5' },
    '5': { next: '6' },
    '6': { child: '7' },
    '7': {},
    '8': { next: '10', child: '9' },
    '9': {},
    '10': {}
}; 

function node(x, placeholder) {
    if (x.child) {
        if (x.next) {
            node(linkedlist[x.child], x.next);
        } else {
            node(linkedlist[x.child], placeholder);
        }
        x.next = x.child;
        x.child = undefined;
    } else if (x.next) { 
        node(linkedlist[x.next], placeholder);
    } else {
        x.next = placeholder;
        if(x.next)
            node(linkedlist[x.next]);
    }
}

console.log('before', JSON.stringify(linkedlist, null, 4));
node(linkedlist['1']);
console.log('after', JSON.stringify(linkedlist, null, 4));

