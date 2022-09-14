const Blockchain = require("./blockchain")

const bitcoin = new Blockchain();

// bitcoin.createNewBlock(2389, 'QWERTYUIOP098','POIUYTREWQ1233');

// This transaction that we created should be in the pending transactions array.
// Because we have not mined or created a new black after creating this transaction.

// bitcoin.createNewTransaction(132,'Niken123098','Ival098321');

// // So how can we get this pending transaction into our actual block chain up here?
// // Well, the way that we do that is we have to mind a new block or create a new block, so let's do that
// bitcoin.createNewBlock(111, 'asdfghjkl098','lkjhgfdsa123');
// // So now we create a block, we create a transaction and then we a block, so this transaction that we created should show up in our second block 
// // because we mine a block. After we created a transaction,

// bitcoin.createNewTransaction(150,'Ival310899','Niken051199');
// bitcoin.createNewTransaction(3000,'Ival310899','Niken051199');
// bitcoin.createNewTransaction(2150,'Ival310899','Niken051199');
// bitcoin.createNewBlock(1909, 'ZXCVBNM456','MNBVCXZ654');

// const previousBlockHash = 'QWERTYUIOP098POIUYTREWQ';
// const currentBlockData = [
//     {
//         amount: 10,
//         sender: 'NIKENasdfghjkl123',
//         recipient: 'MEKAlkjhgfdsa123'
//     },
//     {
//         amount: 4710,
//         sender: 'MELANIasdfghjkl123',
//         recipient: 'INDIRAlkjhgfdsa123'
//     },
//     {
//         amount: 99110,
//         sender: 'NINDAasdfghjkl123',
//         recipient: 'METAlkjhgfdsa123'
//     }
// ]
// const nonce = 100;

// console.log(bitcoin.hashBlock(previousBlockHash,currentBlockData,nonce))

// console.log(bitcoin.proofOfWork(previousBlockHash,currentBlockData));
// console.log(bitcoin.hashBlock(previousBlockHash,currentBlockData, 18335));
// console.log(bitcoin.chain[2]);
// console.log(bitcoin.chain[1]);

console.log(bitcoin);