// Start of function Node
function Node(data) {
    this.data = data;
    this.left = null;
    this.right = null;
}; // End of function Node

// Start of function BinarySearchTree
function BinarySearchTree() {
    this.insert = function(root, data) {
        if (root === null) {
            this.root = new Node(data);
            
            return this.root;
        }
        
        if (data <= root.data) {
            if (root.left) {
                this.insert(root.left, data);
            } else {
                root.left = new Node(data);
            }
        } else {
            if (root.right) {
                this.insert(root.right, data);
            } else {
                root.right = new Node(data);
            }
        }
        
        return this.root;
    };
    
    // Start of function levelOrder
    this.levelOrder = function(root) {

        // Add your code here
        // To print values separated by spaces use process.stdout.write(someValue + ' ')

        /*
        // prints 3 2 1 5 4 7 instead of 3 2 5 1 4 7
        // writing left branches before right regardless of level
        process.stdout.write(root.data + ' '));
        if (root.left) this.levelOrder(root.left);
        if (root.right) this.levelOrder(root.right);
        */

        let q = [root];
        while (q.length) {
            
            //let node = q.pop(); // prints 3 5 7 4 2 1 because LIFO
            let node = q.shift(); // prints 3 2 5 1 4 7 because FIFO
            process.stdout.write(node.data + ' ');
            if (node.left) q.push(node.left);
            if (node.right) q.push(node.right);
            
            /*
            // alternately, splice/pop is less efficient than push/shift?
            let node = q.pop(); // prints 3 2 5 1 4 7 because LILO
            //let node = q.shift(); // prints 3 5 7 4 2 1 because FILO
            process.stdout.write(node.data + ' ');
            if (node.left) q.splice(0, 0, node.left);
            if (node.right) q.splice(0, 0, node.right);
            */
            
        }

	}; // End of function levelOrder
}; // End of function BinarySearchTree

process.stdin.resume();
process.stdin.setEncoding('ascii');

var _input = "";

process.stdin.on('data', function (data) {
    _input += data;
});

process.stdin.on('end', function () {
    var tree = new BinarySearchTree();
    var root = null;
    
    var values = _input.split('\n').map(Number);
    
    for (var i = 1; i < values.length; i++) {
        root = tree.insert(root, values[i]);
    }
    
    tree.levelOrder(root);
});
