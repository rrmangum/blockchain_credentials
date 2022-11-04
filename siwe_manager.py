from siwe import SiweMessage
from ethers import providers

domain = "Url"
statement = "Create statement"
origin = "Uri"
provider = providers.Web3Provider()
signer = provider.getSigner()

def createSiweMessageToken(address, message):
    message = SiweMessage({
        "domain": domain,
        "address": address,
        "statement": statement,
        "uri": origin,
        "version": '1',
        "chainId": '1'
    })

    return message.prepareMessage()

def connectWallet():
    try:
        provider.send('eth_requestAccounts', [])
    except:
        print("User rejected the request")

def signInWithEthereum():
    message = createSiweMessageToken(
        signer.getAddress(),
        'Sign in with Ethereum to the app'
    )

def verifyMessage():
    try:
        message: SiweMessage = SiweMessage(message=eip_4361_string)
        message.verify(signature, nonce="abcdef", domain="example.com")
    except siwe.ValueError:
        # Invalid message
        print("Authentication attempt rejected.")
    except siwe.ExpiredMessage:
        print("Authentication attempt rejected.")
    except siwe.DomainMismatch:
        print("Authentication attempt rejected.")
    except siwe.NonceMismatch:
        print("Authentication attempt rejected.")
    except siwe.MalformedSession as e:
        # e.missing_fields contains the missing information needed for validation
        print("Authentication attempt rejected.")
    except siwe.InvalidSignature:
        print("Authentication attempt rejected.")