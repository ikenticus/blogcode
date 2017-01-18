var test = [];

test.push(1);
test.push(3);
test.push(5);
console.log(test);

test.splice(2, 0, 4);
test.splice(1, 0, 2);
console.log(test);

var empty = {};
var node = 'old';
[1, 2, 3].forEach((c) => {
    if (!empty[node]) {
        empty[node] = [c];
    } else {
        empty[node].push(c);
    }
});
console.log(empty);

node = 'new';
[4, 5, 6].forEach((c) => {
    (empty[node] || (empty[node] = [])).push(c);
});
console.log(empty);
