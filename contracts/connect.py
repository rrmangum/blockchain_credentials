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

def BestowCredential(owner, token_uri):
    
    # Use the contract to send a transaction to the BestowCredential function
    tx_hash = contract.functions.BestowCredential(
        owner,
        token_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(receipt)
  

def VerifyCredential(address, token_id):
    if address == contract.functions.ownerOf(token_id).call():
        print('Individual holds selected credential')
    else:
        print('Individual does NOT hold selected credential')


""" Below are some functions I thought would be useful for later"""
# # Use the contract's `ownerOf` function to get the art token owner
# owner = contract.functions.ownerOf(token_id).call()

#  # Use the contract's `tokenURI` function to get the art token's URI
# token_uri = contract.functions.tokenURI(token_id).call()