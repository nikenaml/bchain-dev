const express = require('express')
const app = express()

// We can handle different end points or different routes.
// For example, we have a get endpoint, which is just slash. And with this endpoint, we are sending back the response of Hello World and then this whole server is listening on Port 3000

app.get('/blockchain', function (req, res) {
  
});

app.post('/transaction', function (req, res) {

});

// this mine endpoint will do is it will mine a new block for us or create a new block for us,
app.get('/mine', function (req, res) {

});

app.listen(3000, function(){
    // the reason that we do this is just so that when our port is actually running, we will know that because we'll see this text.
    console.log('Listening on port 3000...');
});