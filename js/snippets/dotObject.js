/*
    Really useful getattr/setattr for use with dot-notation
    especially since pure dot-notation does not allow numbers
*/

var output = {
    page: {
        20120727: [ 1, 2, 3, 4 ]
    }
}

var dotObject = function (obj, dot, value) {
    if (typeof dot == 'string') {
        return dotObject(obj, dot.split('.'), value);
    } else if (dot.length == 1 && value !== undefined) {
        return obj[dot[0]] = value;
    } else if (dot.length == 0) {
        return obj;
    } else {
        return dotObject(obj[dot[0]], dot.slice(1), value);
    }
}

console.log(output);
console.log('output -> page.20120727.1 =', dotObject(output, 'page.20120727.1'));
console.log('output.page-> 20120727.2 =', dotObject(output.page, '20120727.2'));
console.log('output.page-> 20120727.7 =', dotObject(output.page, '20120727.7'));
console.log('output.page-> 20120728 =', dotObject(output.page, '20120728'));

dotObject(output, 'page.20120727.6', 6);
console.log('setting output -> page.20120727.6 to 6:\n', output);

dotObject(output, 'page.20120727.3', []);
console.log('setting output -> page.20120727.3 to []:\n', output);

dotObject(output.page, '20120727.4', {});
console.log('setting output.page -> 20120727.4 to {}:\n', output);

dotObject(output.page, '20120728', [4, 5, 6]);
console.log('setting output.page -> 20120728 to [list]:\n', output);

