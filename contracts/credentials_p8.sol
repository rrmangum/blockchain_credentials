// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts@4.7.0/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts@4.7.0/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts@4.7.0/access/Ownable.sol";
import "@openzeppelin/contracts@4.7.0/utils/Counters.sol";

contract DigitalCredential is ERC721, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;

    ///// FUNCTION IMPORTS FROM OPENZEPPELIN CONTRACTS WIZARD ///

    // The counter assigns tokenId as they are minted
    Counters.Counter private _tokenIdCounter;

    // // Mapping from token ID to minter address
    mapping(uint256 => address) private _minters;

    // Create Credential ERC721 token
    constructor() ERC721("Vitae Digital Credentials", "VDC") {}

    // anyone can call BestowCredential function
    function bestowCredential(address to, string memory uri) external {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }

    // Necessary solidity overrides
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

    // Displays number of credentials issued by smart contract
    function totalSupply() public view returns (uint256) {
        return _tokenIdCounter.current();
    }

    /// VITAE CONTRACT SPECIFIC FUNCTIONS ///

    // This function mints credentials and is called by bestowCredential
    function _mint(address to, uint256 tokenId) internal override {
        super._mint(to, tokenId);
        _minters[tokenId] = msg.sender;
    }

    // This function allows the owner of the credential to burn it
    function deleteCredential(uint256 tokenId) external {
        require(
            ownerOf(tokenId) == msg.sender,
            "Only the owner or the issuer of the credential can delete it."
        );
        _burn(tokenId);
    }

    // This function allows the issuer to burn the credential
    function revokeCredential(uint256 tokenId) external {
        require(
            _minters[tokenId] == msg.sender,
            "Only the issuer can revoke a credential"
        );
        _burn(tokenId);
    }

    // This function stops the user from transferring the credential
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
}
