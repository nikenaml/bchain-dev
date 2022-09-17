const sha256 = require('sha256');
const currentNodeUrl = process.argv[3];

function Blockchain() {
    this.chain = [];

    // But all of the transactions in here in this area are not really set in stone, they're not really recorded into our block chain yet.
    // They get recorded into our block chain when a new block is mined, which is when a new block is created.
    
    // So all of these new transactions are pretty much just pending transactions and they have not been validated yet.
    // They get validated and they get pretty much set in stone and recorded an our block chain when we create a new black.
    
    this.pendingTransactions = [];

    this.currentNodeUrl = currentNodeUrl;
    this.networkNodes = [];


    // a genesis block is quite simply the first block in a block chain, every block chain needs to start off with one block, and that's called the Genesis block. And we want this to happen right when the block chain is created.
    // So in order to create our Genesis Block, we are going to use our create new block method right inside of our block chain constructor function. So let's do that now. So we will say this does create New Block. 
    // And we can see that this method takes in a notes, a previous block hash and a hash as parameters. Now, since this is the Genesis block, we are not going to have a previous block hash.
    // And since we are not doing a proof of work to create this block, we are also not going to have a notice and we're not going to have a hash for this block as well. So inside of our create new block method, we're simply going to pass in some arbitrary parameters,
    // we will pass on a notice of one hundred, a previous block hash of the string zero.And a hash that is also of the string zero. And you can really make these parameters, whatever you want to make there, kind of just arbitrary for creating our Genesis block.
    this.createNewBlock(100,'0','0');

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
        transactions: this.pendingTransactions,

        // Basically, nonce comes from a proof of work and a nonce in our case is simply just a number. Could be any number could be to ten, ten thousand one hundred thousand. It doesn't really matter. But this Nonce is pretty much a proof. That we created this new black in a legitimate way by using a proof of work method.
        nonce: nonce,

        // Our next property is going to be a hash, and this hash is simply going to be equal to the hash that we pass into our function up here or into our create new block method up here. And basically, this hash will be the data. From our new block. So basically, what's going to happen is we are going to pass our transactions or our new transactions into a hashing function. Basically, what that means is all of our transactions are going to be basically compressed into a single string of code, a single string. And that is what will be our hash.
        hash: hash, 
        // So they're both hashes, this is the hash of the current block and this is the hash of the previous

        // And this is very similar to our hash except our hash right here. This is the data from our current black hacked into a string. And this previous block hash right here is the data from our previous black or the previous black to this one, hacked into a string.
        previousBlockHash: previousBlockHash
    };

    // We are putting all of the new transactions into this block, so we want to clear out this entire new transactions array so we can start over for the next block.
    this.pendingTransactions = [];

    // This basically simply takes this new block that we have created and pushes it into our chain and adds it to our chain.
    this.chain.push(newBlock);

    return newBlock;

    // summary: So basically, what our new create new block method does on a high level is it creates a new block.
    // And inside of this block, we have our transactions, the new transactions that have that have been created since our last block was mined.
    // And after we create a new block, we clear out the new transactions, we push the new block into our chain and we simply return our new block from this method.

}

// block chain constructor function will be called the last block and it will simply return to us the last block in our block chain.
Blockchain.prototype.getLastBlock = function(){
    return this.chain[this.chain.length - 1];
}

// block chain constructor function is called create new transaction and it will create a new transaction for us.
Blockchain.prototype.createNewTransaction = function(amount, sender, recipient) {
    // So the first thing that we want to do inside of our create new transaction method is we want to create a transaction object.
    const newTransaction = {
        amount : amount,
        sender: sender,
        recipient : recipient
    };

    // Every time that a new transaction is created, it's going to be pushed into our new transactions array.
    this.pendingTransactions.push(newTransaction)

    // So overall, when a new transaction is created, it is pushed into our pending transactions.
    // Then when a new block is mined or when a new block is created, that's when all of our pending transactions become recorded on our block chain and they are set in stone and they can never be changed

    return this.getLastBlock()['index'] + 1;

    // so from top to bottom now, the create new transaction method simply creates a new transaction object and then we push that new transaction into our pending transactions.
    // And finally we return the number of the block that this transaction will be added to.


}

// What this hash block method will do is it will take in a block from our block chain and hash that block into some fixed length string that to us will appear pretty much random.
// So in essence, we're going to pass some block or some block data into our method and in return or. In return.
Blockchain.prototype.hashBlock = function(previousBlockHash, currentBlockData, nonce) {
    const dataAsString = previousBlockHash + nonce.toString() + JSON.stringify(currentBlockData);
    const hash = sha256(dataAsString);
    return hash;

}

// A proof of work is very essential to block chain technology, and it is one of the reasons that Bitcoin and many other black chains are so very secure.
// So what is a proof of work?
// Well, if we take a look at our black chain, every black chain is pretty much a list of blocks, right?
// Every single block has to be created and added to the chain. But we don't want just any block being created and added to the chain.
// We want to make sure that every block that is added to the chain is legitimate and it has the correct transactions and the correct data inside of it, because if it doesn't have the correct transactions
// and the correct data, then people could fake how much bitcoin they have and essentially cause fraud and steal money from other people.
// So every time that we create a new block, we first have to make sure that it is a legitimate block by mining it through proof of work.
// So what does a proof of work method actually do? A proof of work method will take in the current Block's data and the previous block hash.
// And from this data that we supply it, it is going to try to generate a specific hash.
// This specific hash in our case is going to be a hash that starts with four zeros. So given the current block data and the previous black hash.
// Somehow we have to generate a resulting hash that begins with four zeros.

Blockchain.prototype.proofOfWork = function(previousBlockHash, currentBlockData) {
    // The reason that this proof of work method will secure our block chain is because in order to generate the correct hash, we are going to have to run our hash black method many, many times, tens of thousands of times or hundreds of thousands of times, and is going to use a lot of computing power and a lot of energy.
    // So if somebody wanted to go back into the black chain and try and change a block or try to change some data in that block, perhaps to give themselves more bitcoin, they would have to do a ton of calculations and use a lot of energy to create the correct hash.
    // So in most cases, going back and trying to recreate an already existing block or trying to remain an already existing block with your own fake data is not feasible.
    // On top of that, not only does our hash block method take in the current black data, but it also takes in the previous Black's hash, this means that all of the blacks in the block chain are linked together by their data.
    // So if somebody was to try and go back and remind or recreate a block that already exists, they would also have to remind and recreate every single block that comes after the first one they recreated.
    // This would take an incredible amount of calculations and energy and is just not feasible for a well developed block chain.
    // A person would have to go in, recreate a block by using a proof of work. And then recreate every block after that by doing a new proof of work for each block.
    // This is just not feasible for any well produced block chain, and this is why block chain technology is so secure
    // basically what our proof of work method will do is it will repeatedly hash our previous block hash and our current block of data and announce. Until we get an acceptable hash generated, that starts with four zeros.

    let nonce = 0;
    let hash = this.hashBlock(previousBlockHash,currentBlockData, nonce);
    // Our proof of work method generates a bunch of different hashes. By incrementing our note's value. Then at the end of the method, we simply return the notes value that gives us a valid hash in which the first four characters are zero zero zero zero.
    // So after this whole proof of work method runs, we will get the correct notes value that we need return from our proof of work.
    
    while (hash.substring(0,4) !== '0000'){
        nonce++;
        hash = this.hashBlock(previousBlockHash,currentBlockData, nonce);
    }
    return nonce;

    // So a proof of work should take a lot of energy and a lot of calculations, and it should be very difficult to calculate. But once we have the correct proof or the correct announce, it should be very easy to verify that we have the correct announced value.
    // We can verify that we have the correct notes or the correct proof by simply passing it into our hash black method, by running our hash black method, one time we can verify that we have the correct notes because the generated hash starts with four zeros. So that's very important to block chain technology.
    // It takes a lot of work to generate a proof of work, but it is very easy to verify that that proof of work is correct. So if we ever want to go back into our block chain and check to make sure that a block is valid, all we have to do is hash that blacks data with the previous black's hash. 
    // And the notes that was generated from the proof of work when that block was mined, if this returns to us a valid hash that starts with four zeros, then we already know that the black is valid. Easy is that it just takes one calculation to prove that the black is valid.
    // So this is pretty cool stuff, this is a very important part of block chain technology, if you are having a little bit of trouble understanding just exactly how this proof of work is working or how it's securing the black chain.

}

module.exports = Blockchain;