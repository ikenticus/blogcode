#!/usr/bin/env node

var amqp = require('amqplib/callback_api');
var mq = require('./rabbitcf.js');

var args = process.argv.slice(2);

if (args.length == 0) {
  console.log("Usage: init_send.js num");
  process.exit(1);
}

amqp.connect('amqp://' + mq.user + ':' + mq.pass + '@' + mq.host, function(err, conn) {
  conn.createChannel(function(err, ch) {
    var q = 'puller_queue';
    var num = parseInt(args[0]);

    ch.assertQueue(q, {durable: true});
    ch.sendToQueue(q, new Buffer(num.toString()), {persistent: true});
    console.log(" [x] Sent '%s'", num.toString());
  });
  setTimeout(function() { conn.close(); process.exit(0) }, 500);
});
