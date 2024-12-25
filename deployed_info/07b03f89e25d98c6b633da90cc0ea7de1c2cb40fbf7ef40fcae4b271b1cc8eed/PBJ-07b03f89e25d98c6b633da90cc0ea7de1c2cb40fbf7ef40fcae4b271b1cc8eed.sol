pragma solidity ^0.8.0;


contract PBJ07b03f89e25d98c6b633da90cc0ea7de1c2cb40fbf7ef40fcae4b271b1cc8eed {
    uint256 public flagCoin;
    uint256 public eth; 
    uint256 public price; 
    uint256 public totalPrice;
    mapping(address => uint256) public flags;
     constructor() payable {
         eth = msg.value; 
     }
     function getMoney() public payable {
	// Get money	
}
     function buy(uint256 flag) payable public {
         require(flag <= flagCoin,"Not enough flagCoin!");
         price = eth/flagCoin;
         totalPrice = price * flag;
        require(msg.value == totalPrice,"Incorrect amount sent!");
         flagCoin -= flag;
         eth += msg.value;
         flags[msg.sender] += flag;
     }
     function sell(uint256 flag) payable public { 
         require(flag <= flagCoin,"Not enough flagCoin!");
         require(flag <= flags[msg.sender],"You do not have that many flagCoins!");
         price=eth/flagCoin;
         totalPrice = price * flag;
         flags[msg.sender] -= flag;
         eth -= msg.value;
         //payable(msg.sender).transfer(totalPrice);
     }

}
