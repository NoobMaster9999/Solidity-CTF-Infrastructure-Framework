pragma solidity ^0.8.0;


contract PBJ90fd3dae6c3917b8cbacbb54ae6675a91e2f088c923381322d2b4c84f058a564 {
    uint256 public flagCoin = 100;
    uint256 public eth; 
    uint256 public price; 
    uint256 public totalPrice;
    uint256 public k;
    uint256 public x;
    uint256 public y;
    uint256 public to_pay;
    mapping(address => uint256) public flags;
     constructor() payable {
         eth = msg.value; 
         k = eth * flagCoin;
     }
     function getMoney() public payable {
     //
     }
     function buy(uint256 flag) payable public {
         require(flag <= flagCoin,"Not enough flagCoin!");
         y = flagCoin - flag;
         x = k/y - eth;
         require(msg.value > (x+1),"Incorrect amount sent!");
         eth = eth + x;
         flagCoin = y;
         flags[msg.sender] += flag;
        //require(msg.value == totalPrice,"Incorrect amount sent!");
     }
     function sell(uint256 flag) payable public {
         require(flag <= flagCoin,"Not enough flagCoin!");
         require(flag <= flags[msg.sender],"You do not have that many flagCoins!");
         y = flag + flagCoin;
         x = k/y;
         to_pay = eth - x;
         flagCoin = y;
         eth = x;
         flags[msg.sender] -= flag;
        payable(msg.sender).transfer(to_pay);
     }

}