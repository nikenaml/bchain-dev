from flask import Flask,request, jsonify,render_template
from blockchain import Blockchain
import json
import requests
import argparse

parser = argparse.ArgumentParser(description='Run flask program')
parser.add_argument(
    '--port',
    action='store',
    dest='port',
    type=int,
    default=8888,
    metavar='PORTNUM',
    help='set port number')
args = parser.parse_args()
app = Flask(__name__,template_folder='templates')
bc = Blockchain(args.port)

@app.route('/blockchain',methods=['GET'])
def blockchain():
    # print(bc.__dict__)
    return json.dumps(bc.__dict__)

@app.route("/transaction",methods=['POST'])
def transaction():
    newTransaction = request.json
    # print(request.data)
    blockIndex = bc.addTransactionToPendingTransaction(newTransaction)
    return {"note":f"Transaction will be added in block {blockIndex}"}

@app.route("/transaction/broadcast",methods=['POST'])
def transactionBroadcast():
    data = request.json
    # newTransaction = bc.createNewTransaction(data['amount'],data['sender'],data['recipient'])
    newTransaction = bc.createNewTransaction(**data)
    bc.addTransactionToPendingTransaction(newTransaction)
    responseAll = []
    for networkNodeURL in bc.networkNodes:
        responseAll.append(requests.post(f"{networkNodeURL}/transaction",json=newTransaction).status_code)
    if responseAll.count(200) == len(responseAll):
        return {"note":"Transaction created and broadcast successfully. "}
    else:
        return{"note":"Errorr"}

@app.route('/mine',methods=['GET'])
def mine():
    lastBlock = bc.getLastBlock()
    previousBlockHash = lastBlock['hash']
    currentBlockData = {
        "transactions":bc.pendingTransactions,
        "index":lastBlock['index']+1
    }
    nonce = bc.prooOfWork(previousBlockHash,currentBlockData)
    blockHash = bc.hashBlock(previousBlockHash,currentBlockData,nonce)
    newBlock = bc.createNewBlock(nonce,previousBlockHash,blockHash)
    responseAll = []
    for networkNodeURL in bc.networkNodes:
        res = requests.post(f"{networkNodeURL}/receive-new-block",json={"newBlock":newBlock})
        responseAll.append(res.status_code)
    # for networkNodeURL in bc.networkNodes:
    #     responseAll.append(request.post(f"{networkNodeURL}/transaction/broadcast",json={"newBlock":newBlock}).status_code)
    if responseAll.count(200) == len(responseAll):
        return {
            "note":"Transaction created and broadcast successfully. ",
            "block":newBlock
        }
    else:
        return{"note":"Errorr"}

@app.route("/receive-new-block",methods=['POST'])
def receive_block():
    newBlock = request.json['newBlock']
    lastBlock = bc.getLastBlock()
    correctHash = lastBlock['hash'] == newBlock['previousBlockHash']
    correctIndex = lastBlock['index']+1 == newBlock['index']
    if correctHash and correctIndex:
        bc.chain.append(newBlock)
        bc.pendingTransactions = []
        return {
            "note":"Transaction created and broadcast successfully. ",
            "newBlock":newBlock
        }
    else:
        return {
            "note":"New Block rejected",
            "newBlock":newBlock
        }


@app.route("/register-and-broadcast-node",methods=['POST'])
def register_and_broadcast_node():
    newNodeURL = request.json['newNodeURL']
    try:
        bc.networkNodes.index(newNodeURL)
    except:
        bc.networkNodes.append(newNodeURL)
    responseAll = []
    for networkNodeURL in bc.networkNodes:
        responseAll.append(requests.post(f"{networkNodeURL}/register-node",json={"newNodeURL":newNodeURL}).status_code)
    if responseAll.count(200) == len(responseAll):
        requests.post(f"{networkNodeURL}/register-nodes-bulk",json={"allNetworkNodes":bc.networkNodes + [bc.currentNodeURL]})
        return {"note":"New node registered with network successfully. "}
    else:
        return {"note":"New node registered with network rejected. "}

@app.route("/register-node",methods=['POST'])
def register_node():
    newNodeURL = request.json['newNodeURL']
    try:
        bc.networkNodes.index(newNodeURL)
    except:
        nodeNotAlreadyPresent = True
    notCurrentNode = bc.currentNodeURL != newNodeURL
    if nodeNotAlreadyPresent and notCurrentNode:
        bc.networkNodes.append(newNodeURL)
    return {"note":"New node registered successfully with node. "}
    # return "Register Node"

@app.route("/register-nodes-bulk",methods=['POST'])
def register_nodes_bulk():
    allNetworkNodes = request.json['allNetworkNodes']
    for networkNodeURL in allNetworkNodes:
        try:
            bc.networkNodes.index(networkNodeURL)
        except:
            nodeNotAlreadyPresent = True
        notCurrentNode = bc.currentNodeURL != networkNodeURL
        if nodeNotAlreadyPresent and notCurrentNode:
            bc.networkNodes.append(networkNodeURL)
    return {'note':'Bulk registration successful. '}

@app.route("/consensus",methods=['POST'])
def consensus():
    newLongestChain = []            
    newPendingTransactions = None
    for networkNodeURL in bc.networkNodes:
        # responseAll.append(request.get(f"{networkNodeURL}/blockchain").status_code)
        res = requests.get(f"{networkNodeURL}/blockchain")
        blockchain = res.json()
        if res.status_code == 200:    
            currentChainLength = len(bc.chain)
            maxChainLength = currentChainLength
            if len(blockchain["chain"]) > maxChainLength:
                maxChainLength = len(blockchain["chain"])
                newLongestChain = blockchain["chain"]   
                newPendingTransactions = blockchain["pendingTransactions"]         
    if newLongestChain == [] or (newLongestChain and not bc.chainIsValid(newLongestChain)):
        return {"note":"Current chain has not been replaced. ","chain":bc.chain}
    elif newLongestChain and bc.chainIsValid(newLongestChain):
        bc.chain = newLongestChain
        bc.pendingTransactions = newPendingTransactions
        return {
            "note":"This chain has been replaced. ",
            "chain":bc.chain
        }


@app.route("/block/<string:blockHash>",methods=['GET'])
def block_hash(blockHash):
    blockHash = request.json()['blockHash']
    correctBlock = bc.getBlock(blockHash)
    return {
        "block":correctBlock
    }
@app.route("/transaction/<int:transactionId>",methods=['GET'])
def getTransactionId(transactionId):
    transactionData = bc.getTransaction(transactionId)
    return {
        "transaction":transactionData['transaction'],
        "block":transactionData["block"]
    }

@app.route("/address/<string:address>",methods=['GET'])
def getAddress(address):
    addressData = bc.getAddressData(address)
    return {
        "addressData":addressData
    }

@app.route("/block-explorer",methods=['GET'])
def blockExplorer():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True,port=args.port)