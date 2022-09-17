const express = require('express')
const app = express()
const bodyParser = require('body-parser');
const Blockchain = require('./blockchain');

// we want to make an instance of our block chain so we will say consed bitcoin equals a new block
const bitcoin = new Blockchain();

// So basically, all these two lines are doing is they're saying if a request comes in with JSON data or with form data, we simply want to pass that data so that we can access it in any of these routes.
// So any route we hit our data is first going to go through the body parser so we can access the data and then we can use the data in whichever endpoint we'll be receiving it.
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// We can handle different end points or different routes.
// For example, we have a get endpoint, which is just slash. And with this endpoint, we are sending back the response of Hello World and then this whole server is listening on Port 3000

// we can test to make sure that this end point worked correctly, as we can check out our entire block chain by hitting our block chain and point
app.get('/blockchain', function (req, res) {
  res.send(bitcoin);
});

app.post('/transaction', function (req, res) {
    // console.log(req.body);
    // res.send(`The amount of the transaction is ${req.body.amount} bitcoin.`);
    const blockIndex = bitcoin.createNewTransaction(req.body.amount, req.body.sender, req.body.recipient);
    res.json({ note: `Transaction will be added in block ${blockIndex}.`});
});

// this mine endpoint will do is it will mine a new block for us or create a new block for us,
app.get('/mine', function (req, res) {

});



app.listen(3000, function(){
    // the reason that we do this is just so that when our port is actually running, we will know that because we'll see this text.
    console.log('Listening on port 3000...');
});