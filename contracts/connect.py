import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def load_contract():

    # Load the contract ABI
    with open(Path('credentials_abi.json')) as f:
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

# Mints credential
def BestowCredential(owner, token_uri):
    # Use the contract to send a transaction to the BestowCredential function
    tx_hash = contract.functions.bestowCredential(
        owner,
        token_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(receipt)
  
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

# Allows the smart contract owner (Ryan) to revoke credentials
# TODO update function in smart contract to only allow issuer to revoke credential
def RevokeCredential(token_id):
    tx_hash = contract.functions.revokeCredential(
        token_id
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(receipt)

""" Below are some functions I thought would be useful for later"""
# # Use the contract's `ownerOf` function to get the art token owner
# owner = contract.functions.ownerOf(token_id).call()

#  # Use the contract's `tokenURI` function to get the art token's URI
# token_uri = contract.functions.tokenURI(token_id).call()