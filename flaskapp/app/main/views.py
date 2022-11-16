from . import main_blueprint
from .forms import DeploySmartContractForm
import os
from flask import render_template, request, redirect, url_for, flash
from ..extensions import db
from ..models import Wallet
import json
from web3 import Web3
from solcx import compile_standard, install_solc

@main_blueprint.route("/")
def index():
    return render_template("main/index.html")

@main_blueprint.route("/deploy_smart_contract", methods=["GET", "POST"])
def deploy_smart_contract():
    if request.method == "GET":
        form = DeploySmartContractForm(csrf_enabled=False)
        return render_template("main/deploy_smart_contract.html", form=form)

    elif request.method == "POST":
        form = DeploySmartContractForm(csrf_enabled=False)

        if form.validate_on_submit():

            # Read in the smart contract file uploaded from the form
            smart_contract_file = request.files["file"].read().decode("utf-8")

            # Store variables from the form
            http_provider_url = form.http_provider_url.data
            chain_id = form.chain_id.data
            wallet_address = form.wallet_address.data
            private_key = form.private_key.data

            # Compile the contract
            install_solc("0.6.0")
            compiled_sol = compile_standard(
                {
                    "language": "Solidity",
                    "sources": {"MyContract.sol": {"content": smart_contract_file}},
                    "settings": {
                        "outputSelection": {
                            "*": {
                                "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                            }
                        }
                    },
                },
                solc_version="0.6.0",
            )

            # Write the compiled contract data to file
            with open("compiled_sol.json", "w") as compiled_file:
                json.dump(compiled_sol, compiled_file)

            # Write the bytcode to file
            bytecode = compiled_sol["contracts"]["MyContract.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
            with open("bytecode.json", "w") as bytecode_file:
                json.dump(bytecode, bytecode_file)

            # Write the ABI to file
            abi = compiled_sol["contracts"]["MyContract.sol"]["SimpleStorage"]["abi"]
            with open("abi.json", "w") as abi_file:
                json.dump(abi, abi_file)

            # Connect to the network using the HTTPProvider from the form
            w3 = Web3(Web3.HTTPProvider(http_provider_url))
            
            # Create the Contract object using our ABI and bytecode
            Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
            
            # Get the nonce for the wallet address
            nonce = w3.eth.getTransactionCount(wallet_address)
            
            print(private_key, chain_id, w3.eth.gas_price, wallet_address, nonce)
            
            # Create our transaction
            transaction = Contract.constructor().buildTransaction(
                {
                    "chainId": chain_id,
                    "gasPrice": w3.eth.gas_price,
                    "from": wallet_address,
                    "nonce": nonce
                }
            )
            
            # Sign the transaction
            signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
            print(signed_txn)
            
            # Send our transaction
            tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            
            # Wait for the transaction to be mined
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
               
        # Queue a flash message to the user and redirect to the index page    
        flash(f"Contract deployed successfully with tx_hash: {tx_hash}")
        return redirect(url_for("main.index"))


# @main_blueprint.route('/wallet')
# def wallet():
#     #  return render_tempalte('main/wallet.html')
#     private_key = os.environ.get("MY_WALLET_PRIVATE_KEY")
#     from zksync_sdk import HttpJsonRPCTransport, ZkSyncProviderV01, network
#     from zksync_sdk import EthereumSignerWeb3
#     from web3 import Account
#     provider = ZkSyncProviderV01(provider=HttpJsonRPCTransport(network=network.rinkeby))
#     account = Account.from_key(str(private_key))
#     return render_template('main/wallet.html', account=account)

# @main_blueprint.route('/connect_wallet', methods=['POST'])
# def connect_wallet(wallet_address):
#     wallet_address = wallet_address
#     wallet_record = Wallet(address=wallet_address)
#     db.session.add(wallet_record)
#     db.session.commit()
#     return "Hello"
