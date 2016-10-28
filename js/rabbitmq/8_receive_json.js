#!/usr/bin/env node

var amqp = require('amqplib/callback_api');
var mq = require('./rabbitcf.js');

amqp.connect('amqp://' + mq.user + ':' + mq.pass + '@' + mq.host, function(err, conn) {
  conn.createChannel(function(err, ch) {
    var q = 'json_queue';

    ch.assertQueue(q, {durable: false});
    console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", q);
    ch.consume(q, function(msg) {
        console.log(" [x] Received %s", msg.content.toString());
        var run = JSON.parse(msg.content.toString());
        console.log('Checking: %s %s (%s)', run.feed, run.subset, run.last_access);
    }, {noAck: true});
  });
  setTimeout(function() { conn.close(); process.exit(0) }, 500);
});
