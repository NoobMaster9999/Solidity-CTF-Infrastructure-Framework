import yaml
from solcx import compile_standard,install_solc,set_solc_version
data = yaml.safe_load(open('deployment.yaml'))
solidity_version = data['solidity_version']
install_solc(solidity_version)
set_solc_version(solidity_version)
def compile():
	global compiled
	compiled = compile_standard({
    "language": "Solidity",
    "sources": {
        f"Chall.sol": {
            "content": open(f'Chall.sol').read()
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
})

compile()
contract = open('Chall.sol').read()
x=contract.index('contract')
y=contract[x:].index('{')+x
contract_name = contract[x:y].replace(' ','').replace('contract','')
contract_interface = compiled['contracts'][f'Chall.sol'][f'{contract_name}']
bytecode = contract_interface['evm']['bytecode']['object']
abi = contract_interface['abi']
f = open('abi','w')
f.write(str(abi))
b = open('bytecode','w')
b.write(str(bytecode))
