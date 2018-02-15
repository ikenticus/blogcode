var _ = require('lodash');
var amqp = require('amqplib/callback_api');
var config = require('config');
var format = require('string-format');

var QUEUE;
var name = 'async_local';

if (!QUEUE) {
    var mq = {
        user: 'user',
        pass: 'pass',
        host: 'www.host.com'
    };
    amqp.connect(format('amqp://{}:{}@{}', mq.user, mq.pass, mq.host), function(err, conn) {
        QUEUE = conn;

        conn.createChannel(function(err, ch) {
            ch.assertQueue(name, {durable: false, maxPriority: 10});

            _.range(1, 11).forEach((num) => {
                ch.sendToQueue(name, new Buffer(JSON.stringify({
                    key: 'event', num: num
                })), {priority: 5});
            });
            ch.sendToQueue(name, new Buffer(JSON.stringify({
                key: 'old', num: 100
            })));
            ch.sendToQueue(name, new Buffer(JSON.stringify({
                key: 'schedule', num: 1000
            })), {priority: 10});
            ch.sendToQueue(name, new Buffer(JSON.stringify({
                key: 'results', num: 777
            })), {priority: 7});

            setInterval(() => {
                ch.assertQueue(name, {durable: false, maxPriority: 10}, (err, count) => {
                    if (!err) {
                        console.log('Current count:', count.messageCount, count.consumerCount);
                        if (count.messageCount === 0 && count.consumerCount <= 1)
                            process.exit(0);
                    }
                });
            }, 30);

            ch.consume(name, function(msg) {
                ch.ack(msg);
                console.log('MSG', JSON.parse(msg.content.toString()));
            }, {noAck: false});
        });
    });
} else {
    return QUEUE;
}

