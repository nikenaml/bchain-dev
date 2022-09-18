const express = require('express')
const app = express()
const bodyParser = require('body-parser');
const Blockchain = require('./blockchain');

// this library does for us is it creates a unique string, a unique random string for us. And we're going to use that string as this network nodes address.
const uuid = require('uuid');
// const { json } = require('body-parser');
const nodeAddress = uuid.v1().split('-').join('');

// So in order to get access to this variable in our network, a node file, we are using this process,
const port = process.argv[2];

const rp = require('request-promise');

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
    const lastBlock = bitcoin.getLastBlock();
	const previousBlockHash = lastBlock['hash'];
	const currentBlockData = {
		transactions: bitcoin.pendingTransactions,
		index: lastBlock['index'] + 1
	};
	const nonce = bitcoin.proofOfWork(previousBlockHash, currentBlockData);
	const blockHash = bitcoin.hashBlock(previousBlockHash, currentBlockData, nonce);
	
    bitcoin.createNewTransaction(12.5,"00",nodeAddress);
    
    const newBlock = bitcoin.createNewBlock(nonce, previousBlockHash, blockHash);

    res.json ({
        note:"New block mined successfully",
        block:newBlock
    });

});

// So now in our block chain, we want to be able to create a network and we want to have a way of registering all these different nodes with our network.
// So right now, we're going to make a couple more end points that will make registering nodes with our network possible.
// register a node and broadcast it the network
app.post('/register-and-broadcast-node', function(req,res) {
    const newNodeUrl = req.body.newNodeUrl;
	if (bitcoin.networkNodes.indexOf(newNodeUrl) == -1) bitcoin.networkNodes.push(newNodeUrl);

	const regNodesPromises = [];
	bitcoin.networkNodes.forEach(networkNodeUrl => {
		const requestOptions = {
			uri: networkNodeUrl + '/register-node',
			method: 'POST',
			body: { newNodeUrl: newNodeUrl },
			json: true
		};

		regNodesPromises.push(rp(requestOptions));
	});

	Promise.all(regNodesPromises)
	.then(data => {
		const bulkRegisterOptions = {
			uri: newNodeUrl + '/register-nodes-bulk',
			method: 'POST',
			body: { allNetworkNodes: [ ...bitcoin.networkNodes, bitcoin.currentNodeUrl ] },
			json: true
		};

		return rp(bulkRegisterOptions);
	})
	.then(data => {
		res.json({ note: 'New node registered with network successfully.' });
	});
});

// register a node with the network
app.post('/register-node', function(req,res) {
    const newNodeUrl = req.body.newNodeUrl;
	const nodeNotAlreadyPresent = bitcoin.networkNodes.indexOf(newNodeUrl) == -1;
	const notCurrentNode = bitcoin.currentNodeUrl !== newNodeUrl;
	if (nodeNotAlreadyPresent && notCurrentNode) bitcoin.networkNodes.push(newNodeUrl);
	res.json({ note: 'New node registered successfully with node.' });
});

// register multiple nodes at once
app.post('/register-nodes-bulk', function(req, res) {
	const allNetworkNodes = req.body.allNetworkNodes;
	allNetworkNodes.forEach(networkNodeUrl => {
		const nodeNotAlreadyPresent = bitcoin.networkNodes.indexOf(networkNodeUrl) == -1;
		const notCurrentNode = bitcoin.currentNodeUrl !== networkNodeUrl;
		if (nodeNotAlreadyPresent && notCurrentNode) bitcoin.networkNodes.push(networkNodeUrl);
	});

	res.json({ note: 'Bulk registration successful.' });
});

app.listen(port, function(){
    // the reason that we do this is just so that when our port is actually running, we will know that because we'll see this text.
    console.log(`Listening on port ${port}...`);
});