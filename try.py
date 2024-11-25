from web3 import Web3

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Sender and recipient addresses
sender_address = '0xDBD8055A04282Fa2333925209dd105fa85a72a80'
recipient_address = '0x96aA445EB9f7A72cD81cEEcAAaAE991799a09d48'

# Target transaction (low gas price)
target_tx = {
    'from': sender_address,
    'to': recipient_address,
    'value': web3.to_wei(0.1, 'ether'),      # Sending 0.1 ETH
    'gas': 21000,
    'gasPrice': web3.to_wei('20', 'gwei')    # Lower gas price
}

# Sign and send the target transaction
target_tx_hash = web3.eth.send_transaction(target_tx)

# Frontrunning transaction (higher gas price)
frontrun_tx = {
    'from': sender_address,
    'to': recipient_address,
    'value': web3.to_wei(0.1, 'ether'),      # Sending 0.1 ETH again
    'gas': 21000,
    'gasPrice': web3.to_wei('50', 'gwei')    # Higher gas price for frontrunning
}

# Sign and send the frontrunning transaction
frontrun_tx_hash = web3.eth.send_transaction(frontrun_tx)
print('done!')
# Check the mining order
receipt_target = web3.eth.wait_for_transaction_receipt(target_tx_hash)
receipt_frontrun = web3.eth.wait_for_transaction_receipt(frontrun_tx_hash)

print("Order of transactions mined:")
print(f"Target Transaction: {receipt_target.transactionHash}")
print(f"Frontrunning Transaction: {receipt_frontrun.transactionHash}")
