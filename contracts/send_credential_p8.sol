pragma solidity ^0.8.0;

// import ERC721URIStorage
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

// required for totalSupply() function
import "@openzeppelin/contracts/token/ERC721/extensions/IERC721Enumerable.sol";

// Credentials inherit ERC721
contract Credential is ERC721URIStorage, IERC721Enumerable {
    // A constructor that sets the initial value of TokenId as well as calls ERC721 Constructor
    constructor() public ERC721("Credential", "CRED") {}


    // Public funtion anyone can call. Returns TokenID
    function BestowCredential(address owner, string memory tokenURI) public returns (uint256){
        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        return tokenId; 
    }
}