
var _scoresSetTotal = function (sport, results) {
    var score = [0, 0];
    var minSets = { BV: 21.15, TE: 6, TT: 11 };
    results.split(' ').forEach(function(period) {
        var points = period.split('-').map(function(p) { return parseInt(p); });
        //console.log('POINTS', points);

        var minSet = minSets[sport];
        if (!Number.isInteger(minSet)) {
            if (results.lastIndexOf(period) == results.length - period.length) {
                minSet = parseInt(Math.round(minSet % 1 *
                            Math.pow(10, minSet.toString().split('.')[1].length)));                
            } else {
                minSet = parseInt(minSet);              
            }
        }
        //console.log('MIN', minSet);

        if (period.indexOf('(')) {
            if (points[0] >= minSet && points[0] > points[1]) score[0] += 1;
            if (points[1] >= minSet && points[1] > points[0]) score[1] += 1;
        } else {    // almost all sports are win by 2, except tiebreaker ^above
            if (points[0] >= minSet && points[0] > points[1] + 1) score[0] += 1;
            if (points[1] >= minSet && points[1] > points[0] + 1) score[1] += 1;
        }
    });
    return score.join('-');
};

console.log('BV', _scoresSetTotal('BV', '21-14 14-21 11-15'));
console.log('TE', _scoresSetTotal('TE', '7-6(4) 7-6(3) 4-6 6-7(1) 5-7 6-1 7-6(10)'));
console.log('TT', _scoresSetTotal('TT', '5-11 9-11 3-11 11-4 11-5 11-9 7-11'));
