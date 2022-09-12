const Blockchain = require("./blockchain")

const bitcoin = new Blockchain();

bitcoin.createNewBlock(2389, 'QWERTYUIOP098','POIUYTREWQ1233');

// This transaction that we created should be in the pending transactions array.
// Because we have not mined or created a new black after creating this transaction.

bitcoin.createNewTransaction(132,'Niken123098','Ival098321');

// bitcoin.createNewBlock(111, 'asdfghjkl098','lkjhgfdsa123');
// bitcoin.createNewBlock(1909, 'ZXCVBNM456','MNBVCXZ654');

console.log(bitcoin);
// console.log(bitcoin.chain[1]);