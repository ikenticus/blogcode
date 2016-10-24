#!/usr/bin/env node

var amqp = require('amqplib/callback_api');
var mq = require('./rabbitcf.js');

amqp.connect('amqp://' + mq.user + ':' + mq.pass + '@' + mq.host, function(err, conn) {
  conn.createChannel(function(err, ch) {
    var q = 'puller_queue';

    ch.assertQueue(q, {durable: true});
    ch.prefetch(1);

    console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", q);
    ch.consume(q, function(msg) {
      console.log(" [x] Received %s", msg.content.toString());
      ch.ack(msg);
      console.log("     > Ack %s from Queue", msg.content.toString());
      var n = parseInt(msg.content.toString());
    
      var m = n + 1;
      if (m > 45) m = 20;  
      console.log('     Next Request is fib(%d)', m);
      ch.sendToQueue(q, new Buffer(m.toString()), {persistent: true});
      console.log("     > Added %s to Queue", m.toString());

      console.log("     Calculating fib(%d)", n);
      var r = fibonacci(n);
      console.log('     > Calculated %s', r.toString());

    }, {noAck: false});
  });
  //setTimeout(function() { conn.close(); process.exit(0) }, 500);
});

function fibonacci(n) {
  if (n == 0 || n == 1)
    return n;
  else
    return fibonacci(n - 1) + fibonacci(n - 2);
}

