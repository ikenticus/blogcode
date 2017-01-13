var _ = require('lodash');

var origin = {
    x1: {
        a1: {
            name: 'a1',
            stats: [ 1, 2, 3 ]
        },
        a2: {
            name: 'a2',
            stats: [ 4, 5, 6 ]
        }
    },
    x2: {
        b1: {
            name: 'b1',
            stats: { j: 1, k: 2, l: 3 }
        },
        b2: {
            name: 'b2',
            stats: { j: 7, k: 8, l: 9 }
        }
    }
};

var append = {
    x3: {
        c1: {
            name: 'c1',
            stats: 'one'
        },
        c2: {
            name: 'c2',
            stats: 'two'
        }
    }
};

var alter = {
    x1: {
        a2: {
            name: 'a2',
            stats: [ 7, 8, 9 ]
        }
    },
    x2: {
        b1: {
            name: 'B1',
            stats: 'uno'
        },
        b3: {
            name: 'B3',
            stats: 'tres'
        }
    },
    x3: 'destroy'
};

var new1 = _.cloneDeep(origin);
_.merge(new1, append);
console.log('\nAPPEND', JSON.stringify(new1, null, 4));
_.merge(new1, alter);
console.log('\nUPDATGE', JSON.stringify(new1, null, 4));
