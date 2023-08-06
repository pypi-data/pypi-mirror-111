from web3 import Account, Web3, exceptions, types

NETWORK_IDS = {
    'mainnet': 1,
    'kovan': 42,
    'rinkeby': 4,
    'goerli': 5,
    'ropsten': 3,
    'polygon-mainnet': 137
}

"""
Main exposed function that prepares the transaction and sends it to infura
to - account to sent to
message - data to append to tx
project_id - infura project id
network - eth network (mainnet, polygon, kovan, etc.)
value - amount to send (defaults to 0)
gas - gas to spend (defaults to 90000)
"""
def send_tx(to, message, project_id, private_key, network, value=0, gas=90000):
    w3 = __setup(network, project_id)
    tx = {
        "to": to,
        "value": value,
        "data": "0x{}".format(message.encode().hex()),
        "gasPrice": w3.eth.gas_price,
        "gas": gas,
    }

    try:
        sender = Account.from_key(private_key)
        tx['nonce'] = w3.eth.get_transaction_count(sender.address)
        tx['chainId'] = NETWORK_IDS[network]
        signed_tx = sender.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction, sender)
        return tx_hash.hex()
    except ValueError:
        raise ValueError("Incorrect tx details: check private key and network")
    except TypeError:
        raise TypeError("Incorrect account bytes: make sure they are 20 bytes")
    except:
        print("Unexpected error occured")
        raise

"""
Get tx details by its transaction hash
return "Transaction not mined yet for invalid tx_hash"
"""
def get_tx_details(tx_hash, network, project_id):
    w3 = __setup(network, project_id)
    try:
        return w3.eth.get_transaction(tx_hash)
    except exceptions.TransactionNotFound:
        raise RuntimeError("Transaction has not been mined yet: {}".format(tx_hash))

"""
Sets up the network provider (eth, polygon, kovan, etc)
network - 
project_id - 
"""
def __setup(network, project_id):
    url = "https://{}.infura.io/v3/{}".format(network, project_id)
    w3 = Web3(Web3.HTTPProvider(url))
    if(not w3.isConnected()):
        raise RuntimeError('Incorrect project Id or network name')
    return w3
