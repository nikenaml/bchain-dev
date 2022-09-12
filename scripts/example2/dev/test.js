const Blockchain = require("./blockchain")

const bitcoin = new Blockchain();

bitcoin.createNewBlock(2389, 'QWERTYUIOP098','POIUYTREWQ1233');
bitcoin.createNewBlock(111, 'asdfghjkl098','lkjhgfdsa123');
bitcoin.createNewBlock(1909, 'ZXCVBNM456','MNBVCXZ654');


console.log(bitcoin);