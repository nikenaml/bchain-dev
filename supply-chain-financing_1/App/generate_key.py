from ellipticcurve.privateKey import PrivateKey, PublicKey

privateKey = PrivateKey()
publicKey = privateKey.publicKey()
# print(privateKey)
print(privateKey.toPem())
print(publicKey.toPem())
# publicKey = privateKey.publicKey()
