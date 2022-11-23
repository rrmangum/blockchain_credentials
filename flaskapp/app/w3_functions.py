from flask import flash
from web3 import Web3, Account
from pathlib import Path
import json
import os
from dotenv import load_dotenv


load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
ethereum_private_key = os.getenv("ETHEREUM_PRIVATE_KEY")
account = Account.privateKeyToAccount(ethereum_private_key)

# Mints the token into a specified address
def BestowCredential(address, artwork_uri):
    with open(Path('../contracts/credentials_abi.json')) as f:
        artwork_abi = json.load(f)

    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    address = Web3.toChecksumAddress(address)
    nonce = w3.eth.get_transaction_count(address)

    txn = contract.functions.bestowCredential(
        address,
        artwork_uri
    ).build_transaction({ 'from': address, 'gas': w3.eth.gas_price, 'nonce': nonce })

    signed_txn =  w3.eth.account.signTransaction(txn, private_key=ethereum_private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)  

    receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    # receipt = w3.toHex(w3.keccak(signed_txn.rawTransaction))
    
    return receipt

   
# Function to show token from token address 
def show_token(contract, token_id):
    owner = contract.functions.ownerOf(token_id).call()

    token_uri = contract.functions.tokenURI(token_id).call()

    return token_uri


def load_contract():

    # Load the contract ABI
    with open(Path('../contracts/credentials_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

# Load the contract
contract = load_contract()

# Set the gas price strategy
# w3.eth.setGasPriceStrategy(fast_gas_price_strategy)

# Calculate the gas estimate
# gasEstimate = w3.eth.estimateGas(
#     "to": receiver,
#     "from": account_address,
#     "value": value
# )
  
# Allows a verifier to supply a wallet address and a token ID to verify that address 
# actually owns that specific token and the token was issued from our smart contract 
def VerifyCredential(address, token_id):
    if address == contract.functions.ownerOf(token_id).call():
        print('Individual holds selected credential')
    else:
        print('Individual does NOT hold selected credential')

# Allows a receiver to delete(burn) a credential
def DeleteCredential(token_id):
    tx_hash = contract.functions.deleteCredential(
        token_id
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(receipt)

# # Allows the smart contract owner (Ryan) to revoke credentials
# # TODO update function in smart contract to only allow issuer to revoke credential
# def RevokeCredential(token_id):
#     tx_hash = contract.functions.revokeCredential(
#         token_id
#     ).transact({'from': address, 'gas': 1000000})
#     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     print(receipt)