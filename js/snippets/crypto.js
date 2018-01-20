var crypto = require('crypto');

var secret = "hidden";
var phrase = "This old man";

console.log('V1-HMAC-SHA256', crypto.createHmac('sha256', secret).update(phrase).digest('base64'));

