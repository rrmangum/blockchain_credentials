pragma solidity ^0.8.0;

// import ERC721
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol";

// required for totalSupply() function
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/IERC721Enumerable.sol";

// Credentials inherit ERC721
contract Credential is ERC721 {
    // A constructor that sets the initial value of TokenId as well as calls ERC721 Constructor
    constructor() public ERC721("Credential", "CRED") {}


    // Public funtion anyone can call. Returns TokenID
    function BestowCredential(address owner, string memory tokenURI) public returns (uint256){
        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);

        return tokenId; 
    }
}