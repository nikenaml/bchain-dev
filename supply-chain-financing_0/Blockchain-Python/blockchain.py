from datetime import datetime
import json
import hashlib 
import uuid

# port = 5000
class Blockchain():
    def __init__(self,port):
        self.chain = []
        self.pendingTransactions = []
        self.networkNodes = []
        self.currentNodeURL = f"http://localhost:{port}"
        self.createNewBlock(100,'0','0')
    
    def createNewBlock(self,nonce,previousBlockHash,hash):
        newBlock = {
            "index":len(self.chain),
            "timestamp":datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
            "transactions":self.pendingTransactions,
            "nonce":nonce,
            "hash":hash,
            "previousBlockHash":previousBlockHash,
        }
        self.pendingTransactions = []
        self.chain.append(newBlock)
        return newBlock
    
    def getLastBlock(self):
        return self.chain[-1]
    
    # def createNewTransaction(self,amount,sender,recipient):
    #     newTransaction = {
    #         "amount":amount,
    #         "sender":sender,
    #         "recipient":recipient,
    #         "transactionId":str(uuid.uuid4())
    #     }
    #     return newTransaction
    def createNewTransaction(self,**kwargs):
        newTransaction = kwargs
        return newTransaction
    
    def addTransactionToPendingTransaction(self,transactionObj):
        self.pendingTransactions.append(transactionObj)
        return self.getLastBlock()['index']+1

    def hashBlock(self,previousBlockHash, currentBlockData, nonce):
        dataAsString = previousBlockHash + str(nonce) + json.dumps(currentBlockData)
        hash = hashlib.sha256(dataAsString.encode()).hexdigest()
        return hash

    def prooOfWork(self,previousBlockHash,currentBlockData):
        nonce = 0
        hash = self.hashBlock(previousBlockHash,currentBlockData,nonce)
        while hash.startswith('0000') == False:
            nonce+=1
            hash = self.hashBlock(previousBlockHash,currentBlockData,nonce)
        return nonce
    
    def chainIsValid(self,blockchain):
        validChain = True
        for i in range(1,len(blockchain)):
            currentBlock = blockchain[i]
            prevBlock = blockchain[i-1]
            blockHash = self.hashBlock(prevBlock['hash'],{"transactions":currentBlock['transactions'],"index":currentBlock['index']},currentBlock['nonce'])
            if blockHash.startswith('0000') is False or currentBlock['previousBlockHash'] != prevBlock['hash']:
                validChain = False 
        genesisBlock = blockchain[0]
        correctNonce = genesisBlock['nonce'] == 100
        correctPreviousBlockHash = genesisBlock['previousBlockHash'] == '0'
        correctHash = genesisBlock['hash'] == '0'
        correctTransactions = len(genesisBlock['transactions'])== 0
        if correctNonce is False or correctPreviousBlockHash is False or correctHash is False or correctTransactions is False:
            validChain=False
        return validChain
    
    def getBlock(self,blockHash):
        for block in self.chain:
            if block.hash == blockHash:
                correctBlock = block
        
    def getBlock(self,blockHash):

        for block in self.chain:
            for transaction in block.transactions:
                correctBlock = block
                correctTransactions = transaction
        return {
            "transaction":correctTransactions,
            "block":correctBlock    
        }

    def getAddressData(self,address):
        addressTransactions = []
        for block in self.chain:
            for transaction in block:
                addressTransactions.append(transaction)
        
        balance = 0
        for transaction in addressTransactions:
            if transaction.recipient == address:
                balance += transaction.amount
            elif transaction.sender == address:
                balance -= transaction.amount
        return {
            "addressTransactions":addressTransactions,
            "addressBalance":balance
        }
    
    def getTransaction(self,transactionId):
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction.transactionId == transactionId:
                    correctTransactions = transaction
                    correctBlock = block
        return{
            "transaction":correctTransactions,
            "block":correctBlock
        }