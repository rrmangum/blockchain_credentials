pragma solidity ^0.5.0;

// import ERC721Full
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

// Credentials inherit ERC721Full
contract Credential is ERC721Full {
    constructor() public ERC721Full("Credential", "CRED") {} // Name is Credenntial symbol is CRED

    // Public funtion anyone can call. Returns TokenID
    function BestowCredential(address owner, string memory tokenURI) public returns (uint256){
        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        return tokenId;
    }
}
