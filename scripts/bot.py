from web3 import Web3, HTTPProvider
import json
import time
import sys
import yaml
import random
time.sleep(10)
data = yaml.safe_load(open('deployment.yaml'))
interval=data['bot_interval']
functions=data['bot_functions']
args=data['function_args']
values = data['function_value']
gas = data['function_gas']
contract_address = str(sys.argv[1])
rpc=str(sys.argv[2])
wallet = str(sys.argv[3])
x=open('compiled_info/abi').read()
abi=eval(x)
web3 = Web3(HTTPProvider(rpc))
shop = web3.eth.contract(address=contract_address,abi=abi)
# gas = 999999
gasPrice = Web3.to_wei('55','gwei')
y=0
while True:
	for i in range(len(functions)):
		cmd="shop.functions."+functions[i]+"("##+"(arg).transact({'from':wallet"
		arg = args[i]
		if arg:
			if " " in arg:
				num1 = int(arg.split(' ')[0])
				num2 = int(arg.split(' ')[1])
				arg = random.randint(num1,num2)
				cmd += "arg).transact({'from':wallet"
			elif "," in arg:
				for j in range(len(arg[i]).split(',')):
					cmd+=arg[i].split(',')[j]
					cmd+=","
				cmd=cmd[:-1]
				cmd+=").transact({'from':wallet"
			else:
				try:
					int(arg)
				except:
					func = arg
					arg = int(eval("shop.functions."+func+"().call({'from':wallet})"))
					print(arg)
					cmd += "arg).transact({'from':wallet"
		else:
			cmd += ").transact({'from':wallet"
		val = values[i]
		if val:
			if " " in val:
				val1 = int(val.split(' ')[0])
				val2 = int(val.split(' ')[1])
				val = Web3.to_wei(random.randint(val1,val2),'ether')
			Gas=int(gas[i].split(' ')[0])
			gasPrice=int(gas[i].split(' ')[1])
			print(val,Gas,gasPrice)
			cmd+=",'value':val+(Gas*gasPrice),'gas':Gas,'gasPrice':gasPrice})"
		else:
			cmd+="})"
		# print(cmd)
		tx_hash = eval(cmd)
		time.sleep(interval)