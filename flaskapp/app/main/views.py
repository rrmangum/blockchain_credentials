from . import main_blueprint
import os
from flask import render_template, request, redirect, url_for

@main_blueprint.route('/')
def index():
    return render_template('main/index.html')

@main_blueprint.route('/wallet')
def wallet():
    #  return render_tempalte('main/wallet.html')
    private_key = os.environ.get("MY_WALLET_PRIVATE_KEY")
    from zksync_sdk import HttpJsonRPCTransport, ZkSyncProviderV01, network
    from zksync_sdk import EthereumSignerWeb3
    from web3 import Account

    provider = ZkSyncProviderV01(provider=HttpJsonRPCTransport(network=network.rinkeby))
    account = Account.from_key(str(private_key))

    return render_template('main/wallet.html', account=account)
