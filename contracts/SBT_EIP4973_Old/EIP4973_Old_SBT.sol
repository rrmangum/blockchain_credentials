// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts@4.7.0/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts@4.7.0/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts@4.7.0/access/Ownable.sol";
import "@openzeppelin/contracts@4.7.0/utils/Counters.sol";

contract DigitalCredential is ERC721, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;

    ///// function imports from OpenZeppelin contracts wizard ///

    // The counter assigns tokenId as they are minted
    Counters.Counter private _tokenIdCounter;

    // This event is emitted when a token is created and bound to an address
    event Attest(address indexed to, uint256 indexed tokenId);

    //This event is emitted when a token is removed
    event Revoke(address indexed to, uint256 indexed tokenId);

    // TODO: need to assign parameters to constructor for implementation with UI
    constructor() ERC721("DigitalCredential", "DC") {}

    // anyone can call safeMint function
    function safeMint(address to, string memory uri) public {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
        
        // declare variable for issuer wallet 
        // return tx hash
    }

    function _burn(uint256 tokenId)
        internal
        override(ERC721, ERC721URIStorage)
    {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    ///// VITAE contract specific functions /////

    // This function allows the owner of the token to burn it
    function deleteCredential(uint256 tokenId) public {
        require(
            ownerOf(tokenId) == msg.sender,
            "Only the owner or the issuer of the credential can delete it."
        );
        _burn(tokenId);
    }

    // This function allows the contract owner(us) to burn the token. As written, only the contract creator(us) can revoke the credential
    // TODO: This function should also be callable by the issuer, create a modifier requiring msg.sender to be verified as tokenId issuer address
    function revokeCredential(uint256 tokenId) external onlyOwner {
        _burn(tokenId);
    }

    // This function stops the user from transferring the token
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256
    ) internal pure override {
        require(
            from == address(0) || to == address(0),
            "This credential cannot be transferred."
        );
    }

    // This function emits the events to store the data
    function _afterTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    ) internal override {
        if (from == address(0)) {
            emit Attest(to, tokenId);
        } else if (to == address(0)) {
            emit Revoke(to, tokenId);
        }
    }
}
