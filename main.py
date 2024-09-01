#!/venv/bin/python3
import subprocess
import os
import random
from hashlib import sha256
import socket
from web3 import Web3, HTTPProvider
import json
import yaml

data = yaml.safe_load(open('deployment.yaml'))
starting_balance = data['contract_balance']
player_balance = data['player_balance']
def get_instance():
	deployment_info = subprocess.Popen(["python3","-u","deploy.py",starting_balance,player_balance],stdout=subprocess.PIPE)
	contract_address = deployment_info.stdout.readline().decode()
	rpc_url = deployment_info.stdout.readline().decode()
	private_key = deployment_info.stdout.readline().decode()
	wallet_address = deployment_info.stdout.readline().decode()
	hashed = deployment_info.stdout.readline().decode()
	info = deployment_info.stdout.readline().decode()
	output = (contract_address+rpc_url+private_key+wallet_address+hashed+info)
	print(output,end='')

def get_flag():
	player_hash = input("Please enter the hash provided during deployment: ").strip()
	if not all([(player_hash[i] in "1234567890abcdef")for i in range(len(player_hash))]):
		print("Please provide the correct hash!")
		exit(0)
	try:
		f = open(f'{player_hash}/{player_hash}.txt').read()
		hash = f
	except:
		print("Please provide the correct hash!")
		exit(0)
	try:
		contract_address=hash.split('_')[0]
		rpc_url =  hash.split('_')[1]
		wallet_address =  hash.split('_')[3]
	except:
		print("If you get this error message, please let the admin know")
		exit(0)
	try:
		web3 = Web3(HTTPProvider(rpc_url))
		f=open('abi','r').read()
		abi=eval(f)
		bank = web3.eth.contract(address=contract_address,abi=abi)
		if bank.functions.isChallSolved().call({'from':wallet_address}):
			print(f'Flag: ' + open('flag.txt').read().strip())
		else:
			print("The challenge is not solved yet!")
	except:
		print("Error!")
		exit(0)


def get_input():
	print("""[1] Get an instance\n[2] Get the flag\nChoice: """,end='')
	try:
		x = int(input())
		if x == 1:
			get_instance()
		elif x == 2:
			get_flag()
	except:
		exit(0)

get_input()
	
