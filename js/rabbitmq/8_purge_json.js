#!/usr/bin/env node

var amqp = require('amqplib/callback_api');
var mq = require('./rabbitcf.js');

amqp.connect('amqp://' + mq.user + ':' + mq.pass + '@' + mq.host, function(err, conn) {
  conn.createChannel(function(err, ch) {
    var q = 'json_queue';

    ch.purgeQueue(q);
    console.log(" [x] Purged %s", q);
  });
  setTimeout(function() { conn.close(); process.exit(0) }, 500);
});
