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

const bc1 = {
    "chain": [
    {
    "index": 1,
    "timestamp": 1664783853063,
    "transactions": [],
    "nonce": 100,
    "hash": "0",
    "previousBlockHash": "0"
    },
    {
    "index": 2,
    "timestamp": 1664783859766,
    "transactions": [],
    "nonce": 18140,
    "hash": "0000b9135b054d1131392c9eb9d03b0111d4b516824a03c35639e12858912100",
    "previousBlockHash": "0"
    },
    {
    "index": 3,
    "timestamp": 1664784830123,
    "transactions": [
    {
    "amount": 12.5,
    "sender": "00",
    "recipient": "0943c02042f111edafcce17066091d28",
    "transactionId": "0d6b22b042f111edafcce17066091d28"
    },
    {
    "amount": 1100,
    "sender": "niken",
    "recipient": "mama",
    "transactionId": "4d876b4042f311edafcce17066091d28"
    }
    ],
    "nonce": 32325,
    "hash": "0000f4f14e5c0062402eb59ddb2d7068855776dc62a06665def1def2d0cd8ab9",
    "previousBlockHash": "0000b9135b054d1131392c9eb9d03b0111d4b516824a03c35639e12858912100"
    },
    {
    "index": 4,
    "timestamp": 1664784862928,
    "transactions": [
    {
    "amount": 12.5,
    "sender": "00",
    "recipient": "0943c02042f111edafcce17066091d28",
    "transactionId": "4fc6d3f042f311edafcce17066091d28"
    },
    {
    "amount": 1500,
    "sender": "niken",
    "recipient": "mama",
    "transactionId": "5cd8032042f311edafcce17066091d28"
    },
    {
    "amount": 2900,
    "sender": "niken",
    "recipient": "mama",
    "transactionId": "60d6cf1042f311edafcce17066091d28"
    }
    ],
    "nonce": 119658,
    "hash": "00001edd5591adcf50903f12de7493b0c37ddc64ed1e0143c7cf43252a8240e6",
    "previousBlockHash": "0000f4f14e5c0062402eb59ddb2d7068855776dc62a06665def1def2d0cd8ab9"
    },
    {
    "index": 5,
    "timestamp": 1664784874638,
    "transactions": [
    {
    "amount": 12.5,
    "sender": "00",
    "recipient": "0943c02042f111edafcce17066091d28",
    "transactionId": "6354523042f311edafcce17066091d28"
    }
    ],
    "nonce": 53531,
    "hash": "00001872b0b765235c13a6daa923b7b565ec57659beed2f8047917d673006127",
    "previousBlockHash": "00001edd5591adcf50903f12de7493b0c37ddc64ed1e0143c7cf43252a8240e6"
    }
    ],
    "pendingTransactions": [
    {
    "amount": 12.5,
    "sender": "00",
    "recipient": "0943c02042f111edafcce17066091d28",
    "transactionId": "6a4f201042f311edafcce17066091d28"
    }
    ],
    "currentNodeUrl": "http://localhost:3001",
    "networkNodes": []
    };

// console.log(bitcoin.hashBlock(previousBlockHash,currentBlockData,nonce))

// console.log(bitcoin.proofOfWork(previousBlockHash,currentBlockData));
// console.log(bitcoin.hashBlock(previousBlockHash,currentBlockData, 18335));
// console.log(bitcoin.chain[2]);
// console.log(bitcoin.chain[1]);

// console.log(bitcoin);
console.log('VALID:', bitcoin.chainIsValid(bc1.chain));
