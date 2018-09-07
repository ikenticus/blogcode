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
    
    // Start of function getHeight
    this.getHeight = function(root) {
        // Add your code here
        if (!root) {
            return -1;
        }
        let L = this.getHeight(root.left);
        let R = this.getHeight(root.right);
        //console.log(root.data, 'L:', L, 'R:', R);
        return 1 + ((L > R) ? L : R);

        /*
        // My original code did not work due to a few things:
        if (!root.left && !root.right) {
            return 1; // 1. upgraded from -1 to 1 and Testcase0 worked
        } else {
            // 2. similarly added 1+ to make Testcase0 work
            let L = root.left  ? 1 + this.getHeight(root.left) : 0;
            let R = root.right ? 1 + this.getHeight(root.right) : 0;
            console.log(root.data, 'L:', L, 'R:', R);
            // 3. however, the addition below is flawed without parenthesis around ternary
            return 1 + (L > R) ? L : R;
        }
        */

    }; // End of function getHeight
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

    // uncomment to dump binary tree
    //console.log(JSON.stringify(tree, null, 4));

    console.log(tree.getHeight(root));
});
