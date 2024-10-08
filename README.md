# Solidity CTF Instancer Framework

Solidity CTF Instancer is an instancer that makes it easy to build and deploy solidity blockchain challenges for CTFs!


# Usage

1. Clone the repo
2. Put your challenge contract in `Chall.sol`
3. Edit `deployment.yaml` to your preferance
4. Run `./build.sh` to download all the required tools
5. Run `./run.sh` to start the instancer! That's it!

# Special Features

Solidity CTF Instancer has a lot of special features, namely:

* Special intercepter which blocks anyone trying to access any account running on a specific RPC-URL. This makes the instancer secure so that any player cannot interfere with any other player.

# How it works

How the instancer basically works:

* Create two wallets, a player wallet and a contract wallet. Deploy the contract with the required amount/arguments. Create a hash to map to the contract

* Provide all the required details to the player

* A get flag feature that allows people to get the flag based on their hash

# To-Do

- [ ] Make a docker container
- [ ] Build script to download all required tools
- [X] Customizable timeout
- [ ] Make a script to start the instancer
- [ ] Lock/Unlock wallet mechanism (????)
- [X] Use solc python module to compile install of truffle
- [ ] Make the constructor arguments actually work
- [ ] Special hashed-contracts + extra security feature
- [ ] Requirements.txt for python packages
- [ ] If someone closes the connection during the deployment (Ctrl C), then stop everything (such as RPC) before exiting


# Creator

Solidity CTF Instancer Framework is created by NoobMaster. If you have any questions and/or feedback regarding any part of the instancer, please feel free to contact me on discord: `noobmaster_1337`
