var _ = require('lodash');

var mappings = [
    {
        "sdi": "COFC",
        "usat": "CHAR"
    },
    {
        "subsport": ["NCAAB"],
        "sdi": "CONN",
        "usat": "UCON"
    },
    {
        "subsport": ["NCAAF", "NCAAW"],
        "sdi": "UCONN",
        "usat": "UCON"
    }
];

//console.log(_.find(mappings, {usat: 'UCON'}));
console.log(_.find(mappings, (m) => {
    return m.usat === 'UCON' && (!m.subsport || m.subsport.indexOf('NCAAB') > -1);
}));
console.log(_.find(mappings, (m) => {
    return m.usat === 'UCON' && (!m.subsport || m.subsport.indexOf('NCAAF') > -1);
}));
console.log(_.find(mappings, (m) => {
    return m.usat === 'CHAR' && (!m.subsport || m.subsport.indexOf('NCAAF') > -1);
}));
