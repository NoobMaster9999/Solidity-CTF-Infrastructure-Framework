# Solidity CTF Instancer Framework

Solidity CTF Instancer is an instancer that makes it easy to build and deploy solidity blockchain challenges for CTFs!


# Usage

1. Clone the repo
2. Put your challenge contract in `Chall.sol`
3. Edit `deployment.yaml` to your preferance
4. Run `./build.sh` to download all the required tools
5. Run `./run.sh <port>` with the port you want to start the instancer!
6. `nc 127.0.0.1 <port>` to connect to the instancer locally!

# Special Features

Solidity CTF Instancer has a lot of special features, namely:

* Special intercepter which blocks anyone trying to access any account running on a specific RPC-URL. This makes the instancer secure so that any player cannot interfere with any other player.
* Special Memory Pool features that mimics the real blockchain by having a queue of transactions (useful for challenges that require analyzing the mempool: front-running attacks for example)

# How it works

How the instancer basically works:

* Create two wallets, a player wallet and a contract wallet. Deploy the contract with the required amount/arguments. Create a hash to map to the contract

* Provide all the required details to the player

* A get flag feature that allows people to get the flag based on their hash

# To-Do

- [ ] Make a docker container
- [X] Build script to download all required tools
- [X] Customizable timeout
- [X] Make a script to start the instancer
- [ ] Lock/Unlock wallet mechanism (????)
- [X] Use solc python module to compile install of truffle
- [ ] Make the constructor arguments actually work
- [ ] Special hashed-contracts + extra security feature
- [X] Requirements.txt for python packages
- [ ] If someone closes the connection during the deployment (Ctrl C), then stop everything (such as RPC) before exiting
- [X] Custom contract names

# Creator

Solidity CTF Instancer Framework is created by NoobMaster. If you have any questions and/or feedback regarding any part of the instancer, please feel free to contact me on discord: `noobmaster_1337`
