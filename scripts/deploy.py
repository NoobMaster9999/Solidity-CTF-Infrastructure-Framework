from web3 import Web3
import json
import subprocess
import os
import random
import time
from hashlib import sha256
import sys
import yaml
from solcx import compile_standard,install_solc,set_solc_version
data = yaml.safe_load(open('deployment.yaml'))
contract_balance = data['contract_balance']
player_balance = data['player_balance']
solidity_version = data['solidity_version']
timeout = int(data['timeout'])
public_ip = data['public_ip']
mempool = data['mempool']
if mempool:
	mempool_time = int(data['mempool_time'])
install_solc(solidity_version)
set_solc_version(solidity_version)
# def compile(hashed):
# 	global compiled
# 	compiled = compile_standard({
#     "language": "Solidity",
#     "sources": {
#         f"Chall{hashed}.sol": {
#             "content": open(f'contracts/Chall-{hashed}.sol').read()
#         }
#     },
#     "settings": {
#         "outputSelection": {
#             "*": {
#                 "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
#             }
#         }
#     }
# })

def fix(hashed,wallet):
	global contract_name
	contract = open('Chall.sol').read()
	x=contract.index('contract')
	y=contract[x:].index('{')+x
	contract_name = contract[x:y].replace(' ','').replace('contract','')
	# contract = contract.replace("YOUR_WALLET_ADDRESS",wallet)
	#contract.close()
	contract = contract.replace(f"contract {contract_name}",f"contract {contract_name}{hashed}")
	f = open(f'./deployed_info/{hashed}/{contract_name}-{hashed}.sol','w')
	f.write(contract)
	f.close()

def make_instance():
	global ganache
	global password
	global port
	global intercept
	global hashed
	global abi
	global bytecode
	global wallet
	password = os.urandom(24).hex()
	my_private_key = "0x"+os.urandom(32).hex()
	your_private_key = "0x"+os.urandom(32).hex()
	hashed=sha256(sha256(random.randbytes(32)+os.urandom(32)).digest()).digest().hex()
	# print(port)
	port = random.randint(40001,49999)
	while True:
		if mempool:
			ganache = subprocess.Popen(["ganache","--secure","--passphrase",password,"--port",str(port+10001),"--host","127.0.0.1","-b",f'{mempool_time}',f'--account="{my_private_key},{str(int(int(contract_balance)+(0.1*10e17)))}"',f'--account="{your_private_key},{str(int(player_balance))}"',"--gasPrice","0","--gasLimit","999999"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		else:
			ganache = subprocess.Popen(["ganache","--secure","--passphrase",password,"--port",str(port+10001),"--host","127.0.0.1",f'--account="{my_private_key},{str(int(int(contract_balance)+(0.1*10e17)))}"',f'--account="{your_private_key},{str(int(player_balance))}"',"--gasPrice","0","--gasLimit","999999"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		time.sleep(3)
		if ganache.poll() is None:
			break
		else:
			port = random.randint(40001,49999)
	time.sleep(3)
	# print('ganache is running!')
	intercept = subprocess.Popen(["python3","scripts/intercept.py",str(port)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	web3 = Web3(Web3.HTTPProvider(f"http://localhost:{port}"))
	player_wallet = web3.eth.account.from_key(your_private_key)
	os.system(f"mkdir deployed_info/{hashed}")
	fix(hashed,player_wallet.address)
	# compile(hashed)
	# print("compiled, exiting...")
	# exit(0)
	# f = open(f'build/contracts/Chall{hashed}.json','r')
	# os.system(f"rm build/contracts/Chall{hashed}.json")
	# contract_json = json.load(f)
	# abi = contract_json['abi']
	# bytecode = contract_json['bytecode']
	# print(compiled['contracts'][f'Chall{hashed}.sol'])
	# contract_interface = compiled['contracts'][f'Chall{hashed}.sol'][f'Chall{hashed}']
	bytecode = open('compiled_info/bytecode','r').read()
	f=open('compiled_info/abi','r').read()
	abi=eval(f)
	shop = web3.eth.contract(abi=abi, bytecode=bytecode)
	wallet = web3.eth.account.from_key(my_private_key)
	web3.geth.personal.unlock_account(wallet.address, password, 0)
	web3.geth.personal.unlock_account(player_wallet.address, password, 0)
	tx_hash = shop.constructor().transact({'from': wallet.address})
	x = web3.eth.wait_for_transaction_receipt(tx_hash)
	contract_address = x.contractAddress
	gas_price = web3.to_wei('3', 'gwei')
	shop = web3.eth.contract(address=contract_address,abi=abi)
	gas_limit = shop.functions.getMoney().estimate_gas({'from': wallet.address})
	# gas_limit = 999999
	total_gas_cost = gas_price * gas_limit
	intial_deposit = shop.functions.getMoney().build_transaction({'from':wallet.address,'value':int(100e18)-total_gas_cost,'gas':gas_limit,'gasPrice':gas_price})
	tx_hash = web3.eth.send_transaction(intial_deposit)
	tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
	#web3.geth.personal.lock_account(wallet.address)
	rpc_url = "http://"+public_ip+":"+str(port)
	f = open(f'deployed_info/{hashed}/{hashed}.txt','w')
	f.write(contract_address+"_"+rpc_url+"_"+your_private_key+"_"+player_wallet.address)
	f.close()
	return str(contract_address),str(rpc_url),str(your_private_key),str(player_wallet.address),str(hashed)

info = make_instance()
print("contract address: " + info[0] + "\n" + "rpc-url: " + info[1] + "\n" + "Wallet private-key: " + info[2] + "\n" + "Wallet address: " + info[3] + "\n" + "Secret: " + info[4] + "\n" + "Please save the provided secret, it will be needed to get the flag")
# time.sleep(timeout)
for i in range(20):
	time.sleep(15)
	web3 = Web3(Web3.HTTPProvider(info[1]))
	shop = web3.eth.contract(address=info[0],abi=abi)
	if i % 2 == 0:
		deposit = shop.functions.buy(10).build_transaction({'from':wallet.address,'value':int(13e18)})
		web3.eth.send_transaction(deposit)
	else:
		deposit = shop.functions.sell(10).build_transaction({'from':wallet.address})
		web3.eth.send_transaction(deposit)
		print('price reset?')
		time.sleep(60)
os.system(f"rm -rf ./{info[4]}/")
try:
	os.remove(f"./deployed_info/{info[4]}/{contract_name}-{info[4]}.sol")
	# os.remove(f"./build/contracts/Chall{info[4]}.json")
	# abcd
except:
	pass
	# print("Something 	failed!")
finally:
	ganache.terminate()	
	intercept.terminate()