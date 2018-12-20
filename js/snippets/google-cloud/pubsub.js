// npm install --save @google-cloud/pubsub
const {PubSub} = require('@google-cloud/pubsub');

let _ = require('lodash'),
    format = require('string-format'),
    path = require('path');

async function getMessage(ps, subscriptionName) {
    const timeout = 60;
    const subscription = ps.subscription(subscriptionName);
    let messageCount = 0;
    const messageHandler = message => {
        console.log(`Received message ${message.id}:`);
        console.log(`\tData: ${message.data}`);
        console.log(`\tAttributes: ${message.attributes}`);
        messageCount += 1;
        message.ack();
    };
    subscription.on(`message`, messageHandler);
    setTimeout(() => {
        subscription.removeListener('message', messageHandler);
        console.log(`${messageCount} message(s) received.`);
    }, timeout * 1000);
}

async function putMessage(ps, topicName) {
    const data = JSON.stringify({ foo: 'bar' });
    const dataBuffer = Buffer.from(data);
    const messageId = await ps
        .topic(topicName)
        .publisher()
        .publish(dataBuffer);
    console.log(`Message ${messageId} published.`);
}

// MAIN
//console.log(process.argv.length)
if (process.argv.length < 4) {
    console.log('\nUsage: %s key.json <action> <queue> <params>', path.basename(process.argv[0]));
    console.log(`
        get <subscription>
        put <topic>
    `)
    process.exit(1);
}
// explicitly specifying service_account credentials file
let keyFile = process.argv[2];
process.env['GOOGLE_APPLICATION_CREDENTIALS'] = keyFile;
let keyData = require(keyFile);
let projectID = keyData.project_id;
let ps = new PubSub();

switch (process.argv[3]) {
    case "get":
        getMessage(ps, process.argv[4]);
        break;
    case "put":
        putMessage(ps, process.argv[4]);
        break;
}
