var _ = require('lodash');
var num = 3;
var lists = {};
var data = ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10", "a11", "a12", "a13"];
_.forEach(data, (item, key) => {
    if (!lists[key % num]) lists[key % num] = [];
    lists[key % num].push(item);
});
console.log(lists);
