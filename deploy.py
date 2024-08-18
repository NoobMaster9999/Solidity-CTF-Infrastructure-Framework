from web3 import Web3
import json
import subprocess
import os
import random
import time
from hashlib import sha256
import sys
contract_balance = int(int(sys.argv[1]))
player_balance = int(int(sys.argv[2]))

def compile():
	try:
		subprocess.run(["truffle","compile"],capture_output=True)
		return 1
	except:
		return 0


public_ip = "127.0.0.1"

def fix(hashed,wallet):
	contract = """
	pragma solidity ^0.6.0;
contract Chall {
    uint[4] cost = [5 ether,11 ether,23 ether,1337 ether];
   uint[4] bought = [0,0,0,0];
    function reset() public payable {
        bought[0] = 0;
        bought[1] = 0;
        bought[2] = 0;
        bought[3] = 0;
    }
    constructor() public {
        reset();
    }
    function getMoney() public payable {
    // This is used for deployment, can be safely ignored
    }
 
    function buy(uint item, uint quantity) public payable {
    	//require(msg.sender==YOUR_WALLET_ADDRESS); // This is for security purposes
        require(0 <= item && item<= 3, "Item does not exist!");
        require(0 < quantity && quantity <= 10, "Cannot buy more than 10 at once!");
        require(msg.value == (cost[item] * quantity), "Payment error!");
        bought[item] = quantity;
    }

    function refund(uint item, uint quantity) public payable {
    	//require(msg.sender==YOUR_WALLET_ADDRESS); // This is for security purposes
        require(0 <= item && item <= 3, "Item does not exist!");
        require(0 < quantity && quantity <= 10, "Cannot refund more than 10 at once!");
        require(bought[item] > 0, "You do not have that item!");
        require(bought[item] >= quantity, "Quantity is greater than amount!");
        msg.sender.call.value((cost[item] * quantity))("");
        bought[item] -= quantity;
    }

    function isChallSolved() public view returns (bool solved) {
        if (bought[3] > 0) {
            return true;
        }
        else {
            return false;
        }
    }

}
	"""
	contract = contract.replace("YOUR_WALLET_ADDRESS",wallet)
	contract = contract.replace("contract Chall",f"contract Chall{hashed}")
	f = open(f'contracts/Chall-{hashed}.sol','w')
	f.write(contract)
	f.close()

def make_instance():
	global ganache
	global password
	global port
	global intercept
	password = os.urandom(24).hex()
	my_private_key = "0x"+os.urandom(32).hex()
	your_private_key = "0x"+os.urandom(32).hex()
	hashed=sha256(sha256(random.randbytes(32)+os.urandom(32)).digest()).digest().hex()
	# print(port)
	port = random.randint(40001,49999)
	while True:
		ganache = subprocess.Popen(["ganache","--secure","--passphrase",password,"--port",str(port+10001),"--host","127.0.0.1",f'--account="{my_private_key},{str(int(int(contract_balance)+(0.1*10e17)))}"',f'--account="{your_private_key},{str(int(player_balance))}"',"--gasPrice","0","--gasLimit","999999"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		time.sleep(3)
		if ganache.poll() is None:
			break
		else:
			port = random.randint(40001,49999)
	time.sleep(3)
	# print('ganache is running!')
	intercept = subprocess.Popen(["python3","intercept.py",str(port)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	web3 = Web3(Web3.HTTPProvider(f"http://localhost:{port}"))
	player_wallet = web3.eth.account.from_key(your_private_key)
	fix(hashed,player_wallet.address)
	compile()
	# print("compiled, exiting...")
	# exit(0)
	f = open(f'build/contracts/Chall{hashed}.json','r')
	os.system(f"rm build/contracts/Chall{hashed}.json")
	contract_json = json.load(f)
	abi = contract_json['abi']
	bytecode = contract_json['bytecode']
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
	intial_deposit = shop.functions.getMoney().build_transaction({'from':wallet.address,'value':contract_balance-total_gas_cost,'gas':gas_limit,'gasPrice':gas_price})
	tx_hash = web3.eth.send_transaction(intial_deposit)
	tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
	web3.geth.personal.lock_account(wallet.address)
	rpc_url = "http://"+public_ip+":"+str(port)
	os.system(f"mkdir {hashed}")
	f = open(f'{hashed}/{hashed}.txt','w')
	f.write(contract_address+"_"+rpc_url+"_"+your_private_key+"_"+player_wallet.address)
	f.close()
	return str(contract_address),str(rpc_url),str(your_private_key),str(player_wallet.address),str(hashed)

info = make_instance()
print("contract address: " + info[0] + "\n" + "rpc-url: " + info[1] + "\n" + "Wallet private-key: " + info[2] + "\n" + "Wallet address: " + info[3] + "\n" + "Secret: " + info[4] + "\n" + "Please save the provided secret, it will be needed to get the flag")
time.sleep(5)
os.system(f"rm -rf ./{info[4]}/")
try:
	# os.remove(f"./contracts/Chall-{info[4]}.sol")
	# os.remove(f"./build/contracts/Chall{info[4]}.json")
	abcd
except:
	print("Something failed!")
finally:
	ganache.terminate()	
	intercept.terminate()
