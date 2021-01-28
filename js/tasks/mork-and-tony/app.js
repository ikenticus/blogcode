const express = require('express');
const request = require('request');

const app = express();

app.get('/ping', (req, res) => {
    res.status(200).send(`${process.env.PING}`);
});

app.get('/mork', (req, res) => {
    request('http://mork:9090/ping', (err, resp, body) => {
        res.status(200).send(body);
    });
});

app.get('/tony', (req, res) => {
    request('http://tony:8008/ping', (err, resp, body) => {
        res.status(200).send(body);
    });
});

app.listen(process.env.PORT, () => {
    console.log(`Listening @ http://localhost:${process.env.PORT}/`);
});
