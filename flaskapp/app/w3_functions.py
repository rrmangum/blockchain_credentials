from web3 import Web3
from pathlib import Path
import json
import os

# Mints the token into a specified address
def mint_token(address, artwork_uri):
    with open(Path('../contracts/credentials_abi.json')) as f:
        artwork_abi = json.load(f)

    w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    address = Web3.toChecksumAddress(address)

    tx_hash = contract.functions.BestowCredential(
        address,
        artwork_uri
    ).transact({ 'from': address, 'gas': 1000000 })

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return receipt

   
# Function to show token from token address 
def show_token(contract, token_id):
    owner = contract.functions.ownerOf(token_id).call()

    token_uri = contract.functions.tokenURI(token_id).call()

    return token_uri