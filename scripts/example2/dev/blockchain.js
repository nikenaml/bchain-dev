function Blockchain() {
    this.chain = [];
    this.newTransactions = [];
}

// place a method on our blockchain => create new block
Blockchain.prototype.createNewBlock = function(nonce, previousBlockHash, hash) {
    // So the first thing that we want to do inside of our create new black method is create a new black object.
    
    // And this is going to be a black in our chain inside of our black chain, so all of the data that we need is going to be stored inside of this black.
    const newBlock = {
        // And this will be basically the block number, it will describe what number block this is in our chain.
        index: this.chain.length + 1, 
        // when this black was created.
        timestamp: Date.now(),

        // So basically, when we create a new block, we are going to want to put all of the new transactions or all of the pending transactions that have just been created, we are going to want to put those into this new block so that they are inside of our block chain and so that they can never be changed. So inside of this new block, we are going to say all of the transactions in this block. Should be the new transactions that are waiting to be placed into a block.
        transactions: this.newTransactions,

        // Basically, nonce comes from a proof of work and a nonce in our case is simply just a number. Could be any number could be to ten, ten thousand one hundred thousand. It doesn't really matter. But this Nonce is pretty much a proof. That we created this new black in a legitimate way by using a proof of work method.
        nonce: nonce,

        // Our next property is going to be a hash, and this hash is simply going to be equal to the hash that we pass into our function up here or into our create new block method up here. And basically, this hash will be the data. From our new block. So basically, what's going to happen is we are going to pass our transactions or our new transactions into a hashing function. Basically, what that means is all of our transactions are going to be basically compressed into a single string of code, a single string. And that is what will be our hash.
        hash: hash, 
        // So they're both hashes, this is the hash of the current block and this is the hash of the previous

        // And this is very similar to our hash except our hash right here. This is the data from our current black hacked into a string. And this previous block hash right here is the data from our previous black or the previous black to this one, hacked into a string.
        previousBlockHash: previousBlockHash
    };

    // We are putting all of the new transactions into this block, so we want to clear out this entire new transactions array so we can start over for the next block.
    this.newTransactions = [];

    // This basically simply takes this new block that we have created and pushes it into our chain and adds it to our chain.
    this.chain.push(newBlock);

    return newBlock;

    // summary: So basically, what our new create new block method does on a high level is it creates a new block.
    // And inside of this block, we have our transactions, the new transactions that have that have been created since our last block was mined.
    // And after we create a new block, we clear out the new transactions, we push the new block into our chain and we simply return our new block from this method.

}



module.exports = Blockchain;