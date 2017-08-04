'use strict';

var _ = require('lodash');
var format = require('string-format');
var moment = require('moment');
var util = require('util');

var tools = require('./tools.js');

var nodePage = function (req, output) {
    if (req.query.node) {
        var nodes = req.query.node.split(/[|:]/);
        _.forEach(output.page, (outKey, key) => {
            if (nodes.indexOf(key) < 0) {
                delete output.page[key];
            }
        });
    }
};

var _collapseObj = function (obj, col) {
    if (util.isArray(obj)) {
        Array.prototype.push.apply(col, obj);
    } else if (typeof obj === 'object') {
        var collapseNext = true;
        _.forEach(obj, (objKey) => {
            if (typeof objKey !== 'object' && typeof objKey !== 'undefined') {
                collapseNext = false;
            }
        });
        if (collapseNext) {
            _.forEach(obj, (objKey) => {
                _collapseObj(objKey, col);
            });
        } else {
            col.push(obj);
        }
    }
    return obj;
};

var collapsePage = function (req, output) {
    if (req.query.collapse) {
        var col = [];
        _collapseObj(output.page, col);
        delete output.page;
        output.page = col;
        _.map(req.params, (key) => {
            var value = output[key];
            if (value !== undefined && value.indexOf('-') === 0 && value.lastIndexOf('-') === value.length - 1) {
                output[key] += 'collapsed-';
                req.params[key] += 'collapsed-';
            }
        });
    }
};

var _checkDate = function (value) {
    // Infostrada d_ (Hungarian notation, under_score variant)
    if (value.indexOf('d_') === 0)
        return true;

    // Generic word date/time match
    if (value.toLowerCase().indexOf('date') >= 0 || value.toLowerCase().indexOf('time') >= 0)
        return true;

    return false;
};

var _parseDate = function (value) {
    // do not process empty values
    if (value === null)
        return value;

    // UTC now
    if (value.toLowerCase() === 'now')
        return new Date();

    // epoch
    if (value.length === 13 && value.replace(/\d+/g, '').length === 0)
        return new Date(parseInt(value));

    // Infostrada .NET /Date(1343892600000+0200)/
    if (value.indexOf('/Date(') === 0) {
        var epoch = new Date(parseInt(value.substring(6, 19)));
        var tzoff = parseInt(value.substring(19, 22));
        return new Date(moment(epoch).add(tzoff, 'hour'));
    }

    try {
        return new Date(value);
    } catch (err) {
        return value;
    }
};

var _filterPurgeItem = function (kv, item) {
    if (kv[1].indexOf('|') > 0 || kv[1].indexOf(':') > 0) {
        var values = kv[1].split(/[|:]/);
        if (values.indexOf(item[kv[0]].toString()) < 0) {
            return true;
        }
    } else {
        if (Number.isInteger(item[kv[0]])) {
            if (parseInt(item[kv[0]]) !== parseInt(kv[1])) return true;
        } else {
            if (kv[1].indexOf('!') === 0 || kv[1].indexOf('-') === 0) {
                if (_.deburr(item[kv[0]].toString()).toLowerCase() ===
                    _.deburr(kv[1]).toString().substring(1).toLowerCase())
                    return true;
            } else {
                if (_.deburr(item[kv[0]].toString()).toLowerCase() !==
                    _.deburr(kv[1]).toString().toLowerCase())
                    return true;
            }
        }
    }
    return false;
};

var _filterExact = function (filter, item, purge) {
    var kv = filter.split('=');
    var childPurge = true;

    // check children nodes for matches (disable children by commenting out block)
    _.forEach(item, (itemKey) => {
        if (util.isArray(itemKey)) {
            if (itemKey.length > 0)
                if (typeof itemKey[0] === 'object' && _.keys(itemKey[0]).indexOf(kv[0]) >= 0)
                    childPurge = _filterPurgeItem(kv, itemKey[0]);
        } else if (typeof itemKey === 'object') {
            if (itemKey && _.keys(itemKey).indexOf(kv[0]) >= 0)
                childPurge = _filterPurgeItem(kv, itemKey);
        }
    });

    if ((childPurge && _.keys(item).indexOf(kv[0]) < 0) ||
        (childPurge && _.keys(item).indexOf(kv[0]) >= 0 && _filterPurgeItem(kv, item))) {
        purge.push(item);
    }
};

var _filterBefore = function (filter, item, purge) {
    var kv = filter.split('<');
    if (_checkDate(kv[0]) === true) {
        if (_parseDate(item[kv[0]]) > _parseDate(kv[1])) purge.push(item);
    } else {
        if (item[kv[0]] > kv[1]) purge.push(item);
    }
};

var _filterAfter = function (filter, item, purge) {
    var kv = filter.split('>');
    if (_checkDate(kv[0]) === true) {
        if (_parseDate(item[kv[0]]) < _parseDate(kv[1])) purge.push(item);
    } else {
        if (item[kv[0]] < kv[1]) purge.push(item);
    }
};

var _filterLike = function (filter, item, purge) {
    var kv = filter.split('~');
    if (item[kv[0]]) {
        if (_.deburr(item[kv[0]].toString()).toLowerCase().indexOf(_.deburr(kv[1]).toString().toLowerCase()) < 0)
            purge.push(item);
    } else {
        purge.push(item);
    }
};

var _filterBoolean = function (filter, item, purge) {
    if (filter.indexOf('!') === 0 || filter.indexOf('-') === 0) {
        if (item[filter.substring(1)] || item[filter.substring(1)] === true) purge.push(item);
    } else {
        if (!item[filter] || item[filter] === false) purge.push(item);
    }
};

var _filterCollection = function (col, filterQuery) {
    var keep = [];
    var purge = [];
    var filters = filterQuery.split(',');
    // build list of items to purge
    col.forEach(function(item) {
        filters.forEach(function(filter) {
            if (filter.indexOf('=') > 0) {
                _filterExact(filter, item, purge);
            } else if (filter.indexOf('<') > 0) {
                _filterBefore(filter, item, purge);
            } else if (filter.indexOf('>') > 0) {
                _filterAfter(filter, item, purge);
            } else if (filter.indexOf('~') > 0) {
                _filterLike(filter, item, purge);
            } else {
                _filterBoolean(filter, item, purge);
            }
        });
    });
    // build new list of items to keep
    col.forEach(function(item) {
        if (purge.indexOf(item) < 0) keep.push(item);
    });
    // reset the page to the kept items
    col = keep;

    return col;
};

var _filterObj = function (obj, filter) {
    if (util.isArray(obj)) {
        obj = _filterCollection(obj, filter);
    } else if (typeof obj === 'object') {
        _.forEach(obj, (objKey, key) => {
            obj[key] = _filterObj(objKey, filter);
        });
    }
    return obj;
};

var filterPage = function (req, output) {
    if (req.query.filter) {
        output.page = _filterObj(output.page, req.query.filter);
    }
};

var _sortObj = function (obj, sortKeys, sortOrder) {
    if (util.isArray(obj)) {
        obj = _.sortBy(obj, sortKeys);
        if (sortOrder && sortOrder === 'desc') {
            obj = obj.reverse();
        }
    } else if (typeof obj === 'object') {
        _.forEach(obj, (objKey, key) => {
            obj[key] = _sortObj(objKey, sortKeys, sortOrder);
        });
    }
    return obj;
};

var sortPage = function (req, output) {
    if (req.query.sortby) {
        output.page = _sortObj(output.page, req.query.sortby.split(','), req.query.order);
    }
};

var _markIndex = function (value) {
    if (value.indexOf('=') > 0) {
        var kv = value.split('=');
        return { value: kv[0], count: parseInt(kv[1]) };
    } else {
        return { value: value, count: 1 };
    }
};

var _markRange = function (range) {
    var begin;
    var end = _markIndex(range[0]);
    if (range.length > 1) {
        begin = _markIndex(range[1]);
    } else {
        begin = { value: range[0].split('=')[0], count: 0 };
    }
    return { begin: begin, end: end };
};

var _shiftRange = function (range, indexes) {
    if (range.end.count > indexes.end.length) {
        range.begin.count += (range.end.count - indexes.end.length);
        range.end.count = indexes.end.length;
    }
    if (range.begin.count > indexes.begin.length) {
        if (indexes.end.length > (range.end.count + range.begin.count - indexes.begin.length)) {
            range.end.count += (range.begin.count - indexes.begin.length);
        } else if (indexes.end.length > range.end.count) {
            range.end.count = indexes.end.length;
        }
        range.begin.count = indexes.begin.length;
    }
};

var _smartMatch = function (left, right) {
    if (Number.isInteger(left)) {
        if (parseInt(left) === parseInt(right)) return true;
    } else {
        if (left === right) return true;
    }
    return false;
};

var _markListEnd = function (node, range, item, indexes, index) {
    if (range.end.value.indexOf('!') === 0 || range.end.value.indexOf('-') === 0) {
        if (!_smartMatch(item[node], range.end.value.substring(1)))
            indexes.end.push(index);
    } else {
        if (_smartMatch(item[node], range.end.value))
            indexes.end.push(index);
    }
};

var _markListBegin = function (node, range, item, indexes, index) {
    if (range.begin.value.indexOf('!') === 0 || range.begin.value.indexOf('-') === 0) {
        if (!_smartMatch(item[node], range.begin.value.substring(1)))
            if (indexes.end.length === 0 || index < indexes.end[0])
                indexes.begin.push(index);
    } else {
        if (_smartMatch(item[node], range.begin.value))
            if (indexes.end.length === 0 || index < indexes.end[0])
                indexes.begin.push(index);
    }
};

var _markLists = function (req, obj, node, range) {
    var index = 0;
    var indexes = { begin: [], end: [] };
    obj.forEach(function(item) {
        _markListEnd(node, range, item, indexes, index);
        _markListBegin(node, range, item, indexes, index);
        index++;
    });
    _shiftRange(range, indexes);
    return indexes;
};

var _sliceObj = function (req, obj, node, range) {
    if (util.isArray(obj)) {
        var subrange = _.cloneDeep(range);
        var indexes = _markLists(req, obj, node, subrange);
        var endIndex = indexes.end[subrange.end.count - 1] + 1;
        var beginIndex = indexes.end[0];
        if (subrange.begin.count > 0) {
            beginIndex = indexes.begin[indexes.begin.length - subrange.begin.count];
        }
        obj = obj.slice(beginIndex, endIndex);
    } else if (typeof obj === 'object') {
        _.forEach(obj, (objKey, key) => {
            obj[key] = _sliceObj(req, objKey, node, range);
        });
    }
    return obj;
};

var slicePage = function (req, output) {
    if (req.query.slice) {
        if (req.query.slice.indexOf(':') > 0) {
            var slice = req.query.slice.split(':');
            output.page = _sliceObj(req, output.page, slice[0], _markRange(slice[1].split(',')));
        }
    }
};

var _markNodeListEnd = function (node, range, item, indexes, index, level) {
    if (range.end.value.indexOf('!') === 0 || range.end.value.indexOf('-') === 0) {
        if (!_smartMatch(item[node], range.end.value.substring(1)))
            indexes.end.push({index: index, level: level});
    } else {
        if (_smartMatch(item[node], range.end.value))
            indexes.end.push({index: index, level: level});
    }
};

var _markNodeListBegin = function (node, range, item, indexes, index, level) {
    if (range.begin.value.indexOf('!') === 0 || range.begin.value.indexOf('-') === 0) {
        if (!_smartMatch(item[node], range.begin.value.substring(1)))
            if (indexes.end.length < range.end.count)
                if (indexes.end.length === 0)
                    indexes.begin.push({index: index, level: level});
    } else {
        if (_smartMatch(item[node], range.begin.value))
            if (indexes.end.length < range.end.count)
                if (indexes.end.length === 0)
                    indexes.begin.push({index: index, level: level});
    }
};

var _markNodeLists = function (req, obj, level, node, range, indexes) {
    var index = 0;
    obj.forEach(function(item) {
        _markNodeListEnd(node, range, item, indexes, index, level);
        _markNodeListBegin(node, range, item, indexes, index, level);
        index++;
    });
};

var _extractCollection = function (req, obj, level, node, range, indexes) {
    if (util.isArray(obj)) {
        _markNodeLists(req, obj, level, node, range, indexes);
    } else if (typeof obj === 'object') {
        _.forEach(obj, (objKey, key) => {
            _extractCollection(req, objKey, format('{}.{}', level, key), node, range, indexes);
        });
    }
    return obj;
};

var _extractObj = function (req, obj, level, node, range) {
    var indexes;
    if (util.isArray(obj)) {
        var subrange = _.cloneDeep(range);
            indexes = _markLists(req, obj, node, subrange);
        var endSlice = indexes.end.slice(0, subrange.end.count);
        var beginSlice = [];
        if (subrange.begin.count > 0) {
            beginSlice = indexes.begin.slice(indexes.begin.length - subrange.begin.count);
        }
        return _.pullAt(obj, beginSlice, endSlice);
    } else if (typeof obj === 'object') {
        indexes = { begin: [], end: [] };
        _extractCollection(req, obj, level, node, range, indexes);
        _shiftRange(range, indexes);
        var slices = [];
        if (range.begin.count > 0) {
            slices = indexes.begin.slice(indexes.begin.length - range.begin.count);
        }
        indexes.end.slice(0, range.end.count).forEach(function(item) {
            slices.push(item);
        });

        var newObj = {};
        slices.forEach(function(item) {
            var sublevel = item.level.slice(level.length + 1);
            if (tools.dotObject(newObj, sublevel) === undefined)
                tools.dotObject(newObj, sublevel, []);
            tools.dotObject(newObj, sublevel).push(
                tools.dotObject(obj, format('{}.{}', sublevel, item.index))
            );
        });
        return newObj;
    }
};

var extractPage = function (req, output) {
    if (req.query.extract) {
        if (req.query.extract.indexOf(':') > 0) {
            var extract = req.query.extract.split(':');
            output.page = _extractObj(req, output.page, 'page', extract[0], _markRange(extract[1].split(',')));
        }
    }
};

var _rankObj = function (obj, index, dense, order, rankas) {
    if (util.isArray(obj)) {
        var list = [];
        obj.forEach(function(item) {
            if (dense) {
                if (list.indexOf(item[index]) < 0) {
                    list.push(item[index]);
                }
            } else {
                list.push(item[index]);
            }
        });
        obj.forEach(function(item) {
            if ((order || 'asc') === (rankas || 'desc')) {
                item.rank = list.indexOf(item[index]) + 1;
            } else {
                item.rank = list.length - list.indexOf(item[index]);
            }
        });
    } else if (typeof obj === 'object') {
        _.forEach(obj, (objKey, key) => {
            obj[key] = _rankObj(objKey, index, dense, order, rankas);
        });
    }
    return obj;
};

var rankPage = function (req, output) {
    if (req.query.rankby) {
        output.page = _rankObj(output.page, req.query.rankby, req.query.dense, req.query.order, req.query.rankas);
    }
};

var _centerObj = function (req, obj, node, value, before, after) {
    if (util.isArray(obj)) {
        var index = 0;
        obj.forEach(function(item) {
            if (item[node] && item[node].toString() === value.toString())
                index = obj.indexOf(item);
        });
        var beginIndex = index - before;
        var endIndex = index + after;
        if (beginIndex < 0) {
            endIndex += 0 - beginIndex;
            beginIndex = 0;
        }
        if (endIndex >= obj.length) {
            if (beginIndex > 0) beginIndex -= endIndex - obj.length + 1;
            endIndex = obj.length - 1;
            if (beginIndex < 0) beginIndex = 0;
        }
        obj = obj.slice(beginIndex, endIndex + 1);
    } else if (typeof obj === 'object') {
        _.forEach(obj, (objKey, key) => {
            obj[key] = _centerObj(req, objKey, node, value, before, after);
        });
    }
    return obj;
};

var centerPage = function (req, output) {
    if (req.query.center) { // center=node=value,before:after
        var center = req.query.center;
        var before = 1;
        var after = 1;
        if (req.query.center.indexOf(',') > 0) {
            var offset = req.query.center.split(',')[1];
            center = req.query.center.split(',')[0];
            before = parseInt(offset.split(':')[0]);
            after = parseInt(offset.split(':')[1]) || before;
        }
        var node = center.split('=')[0];
        var value = center.split('=')[1] || true;
        output.page = _centerObj(req, output.page, node, value, before, after);
    }
};

var _countObj = function (obj, count) {
    if (util.isArray(obj)) {
        obj = obj.slice(0, count);
    } else if (typeof obj === 'object') {
        _.forEach(obj, (objKey, key) => {
            obj[key] = _countObj(objKey, count);
        });
    }
    return obj;
};

var countPage = function (req, output) {
    if (req.query.count) {
        output.page = _countObj(output.page, req.query.count);
    }
};

var count;
var _maxObj = function (obj, max) {
    if (util.isArray(obj)) {
        obj = obj.slice(0, max - count);
        count += obj.length;
    } else if (typeof obj === 'object') {
        _.forEach(obj, (objKey, key) => {
            if (count >= max) {
                delete obj[key];
            } else {
                obj[key] = _maxObj(objKey, max);
            }
        });
    }
    return obj;
};

var maxPage = function (req, output) {
    count = 0;
    if (req.query.max) {
        output.page = _maxObj(output.page, req.query.max);
    }
};

var _safeSum = function (obj, key, val) {
    if (!obj[key]) {
        if (Number.isInteger(val)) {
            obj[key] = val;
        } else {
            obj[key] = 1;
        }
    } else {
        if (Number.isInteger(val)) {
            obj[key] += val;
        } else {
            obj[key] += 1;
        }
    }
    return obj;
};

var totalPage = function (req, output) {
    var sum = {};
    if (req.query.total) {
        var totals = req.query.total.split(',');
        output.page.forEach(function(item) {
            totals.forEach(function(total) {
                if (total.indexOf('=') > 0) {
                    var kv = total.split('=');
                    if (_smartMatch(item[kv[0]], kv[1])) {
                        sum = _safeSum(sum, kv.join(''), 1);
                    }
                } else {
                    if (item[total]) {
                        sum = _safeSum(sum, total, item[total]);
                    }
                }
            });
        });
        output.total = sum;
    }
};

var _emptyObj = function (obj) {
    if (typeof obj === 'object') {
        _.forEach(obj, (objKey, key) => {
            if (util.isArray(objKey)) {
                if (objKey.length === 0) {
                    delete obj[key];
                }
            } else if (typeof objKey === 'undefined') {
                delete obj[key];
            } else if (typeof objKey === 'object') {
                if (objKey) {
                    if (_.keys(objKey).length === 0) {
                        delete obj[key];
                    } else {
                        _.forEach(obj, (objKey) => {
                            if (typeof objKey !== 'undefined') {
                                _emptyObj(objKey);
                            }
                        });
                    }
                }
            }
        });
    }
};

var emptyPage = function (req, output) {
    if (req.query.empty === null && !util.isArray(output.page)) {
        _emptyObj(output.page);
        // iterate again to catch the empty objects left behind by the first pass
        _emptyObj(output.page);
    }
};

var manipulatePage = function (req, output) {
    if (output !== null) {
        nodePage(req, output);
        collapsePage(req, output);
        filterPage(req, output);
        sortPage(req, output);
        slicePage(req, output);
        extractPage(req, output);
        rankPage(req, output);
        centerPage(req, output);
        countPage(req, output);
        maxPage(req, output);
        totalPage(req, output);
        emptyPage(req, output);
    }
    return output;
};

module.exports = {
    centerPage: centerPage,
    collapsePage: collapsePage,
    countPage: countPage,
    emptyPage: emptyPage,
    extractPage: extractPage,
    filterPage: filterPage,
    manipulatePage: manipulatePage,
    maxPage: maxPage,
    nodePage: nodePage,
    rankPage: rankPage,
    slicePage: slicePage,
    sortPage: sortPage,
    totalPage: totalPage
};
