/*

// Given a linked lists with next ahd child nodes:

[1] -> [2] -> [3] -> [8] -> [10]
               |      |
               |     [9]
               |
              [4] -> [5] -> [6]
                             |
                            [7]
                            
                            
// Write a method that would restructure it into the following:
                            
[1] -> [2] -> [3] -> [4] -> [5] -> [6] -> [7] -> [8] -> [9] -> [10]

*/

// Attempting to solve theoretically:

function node(x) {
    if (!x.child && !x.next) { // base case
        return x.id; // or return x ?
    } else { // recurse case
        if (x.child) {
            x.next = node(x.child);
        } else if (x.next) { 
            x.next = node(x.next);
        }
    }
}

const linked_list = {};
function main() {
    let flat_list = node(1);
}

// Kunal indicated that the node function looked like it would work properly, verify what the base case is returning
// At 2pm, he told me that we can go overtime, if needed, and suggested building a linked list to verify the method

