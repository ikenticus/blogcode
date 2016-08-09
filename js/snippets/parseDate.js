var _parseDate = function (value) {
    // do not process empty values
    if (value == null)
        return value;

    // UTC now
    if (value.toLowerCase() == 'now')
        return new Date();

    // epoch
    if (value.length = 13 && value.replace(/\d+/g, '').length == 0)
        return new Date(parseInt(value));

    // Infostrada .NET /Date(1343892600000+0200)/
    if (value.indexOf('/Date(') == 0) {
        var epoch = new Date(parseInt(value.substring(6, 19)));
        var tzoff = parseInt(value.substring(19, 22));
        return new Date(moment(epoch).add(tzoff, 'hour'));
    }

    try {
        return new Date(value);
    } catch (err) {
        return value;
    };
};

console.log(_parseDate(process.argv[2]));
