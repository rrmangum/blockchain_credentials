# Vitae Blockchain Identity  Application
___

## Technology
____
* Python 3.7.7 
* Anaconda Virtual Environment
* Flask 2.2.2
* SQL ALchemy 1.4.42
* PG Admin (Optional)
* Truffle Suite for Blockchain Prototyping
* Goerli Ethereum Testnet
* Infura
* Metamask
* Oppen Zeppelin ERC-721 standard (v4.7.0)
* Solidity pragma 0.8.4
* Reference the requirements.txt for a list of application dependencies

## Application Best Usage
___

The main directory for this application is stored in the /flaskapp directory. The application is being deployed through the application.py file. To run the application ensure that you have an environment set up with all of the necessary dependencies installed. To install these dependencies in your terminal run:

```
pip install -r requirements.txt
```
The /flaskapp/app directory contains the source code for the application including each of the routes and the utility functions used by them. Additionally the schema for the database is designed in the models.py file. The application is built using flask and uses standard conventions to render the HTML stored in the templates directories within each route. 
The application is compiled using blueprints which are created in each routes __init__.py file and are referenced via the /app directory's __init__.py file. 

Before starting the application, create a .env file in your root directory and insert the following controls:
```
FLASK_ENV = development
debug = true
```

This will allow the application to recompile on changes and return important information for error troubleshooting.
To start the application, navigate to the /flaskapp directory and, after making sure that you are using the correct environment, set the flask app in the terminal using:
```
FLASK_APP=application.py flask run
```

This will set the application.py file as the site of deployment for the application and going forward to start the application simply return to the same directory and run:
```
flask run
```
This will deploy the application locally and allow the user to interact with, and create and deploy their own certificates following proper setup of a Pinata IPFS image hosting account, and a valid blockchain connection. 

## Smart Contract Details
___

The smart contract is based on Oppen Zeppelin's ERC-721 standards (v 4.7.0) with some added functionality. An override had been added to the _beforeTokenTransfer function to prevent any of our credentials from being transferred.

The largest addition to the smart contract is the bestowCredential function. This function requires the address you are issueing the credential to and the uri that hosts said credential. It uses a modified version of the _mint function.

RevokeCredential and deleteCredential can both be used to call the burn function from the owner and issuer of the credential respectively.