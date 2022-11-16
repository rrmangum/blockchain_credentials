from solcx import compile_standard, install_solc
import json

# read sol contract into file
with open("./MyContract.sol", "r") as file:
    my_contract_file = file.read()

# install_solc compiler
install_solc("0.6.0")

# compile solidity source code
compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"MyContract.sol": {"content": my_contract_file}},
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
print(compile_sol)
# read sol contract into file
with open("compiled_contract.json", "w") as file:
    json.dump(compile_sol, file)
