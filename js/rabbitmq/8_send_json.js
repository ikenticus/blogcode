#!/usr/bin/env node

var amqp = require('amqplib/callback_api');
var mq = require('./rabbitcf.js');

amqp.connect('amqp://' + mq.user + ':' + mq.pass + '@' + mq.host, function(err, conn) {
  conn.createChannel(function(err, ch) {
    var q = 'json_queue';
    ch.assertQueue(q, {durable: true});

    var msg = {
        feed: 'sdi',
        last_access: new Date()
    };

    var sports = ['baseball', 'basketball', 'football'];
    sports.forEach((sport) => {
        msg.subset = sport;
        ch.sendToQueue(q, new Buffer(JSON.stringify(msg)));
        console.log(" [x] Sent %s", msg);
    });
  });
  setTimeout(function() { conn.close(); process.exit(0) }, 500);
});
