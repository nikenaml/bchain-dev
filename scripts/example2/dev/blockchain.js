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
        nonce: nonce
    };
}