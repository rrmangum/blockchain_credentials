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

    // // Mapping from token ID to minter address
    // mapping(uint256 => address) private _minters;

    // Mapping owner address to token count
    mapping(address => uint256) private _balances;

    // Mapping from token ID to owner address
    mapping(uint256 => address) private _owners;

    // This event is emitted when ownership of any ABT changes by any mechanism. This event emits when credentials are issued, deleted, or revoked
    event Attest(address indexed to, uint256 indexed tokenId);

    //This event is emitted when a token is removed
    event Revoke(address indexed to, uint256 indexed tokenId);

    // Create Credential ERC721 token
    constructor() ERC721("Vitae Digital Credentials", "VDC") {}

    // anyone can call BestowCredential function
    function bestowCredential(address to, string memory uri) external {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
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

    function totalSupply() public view returns (uint256) {
        return _tokenIdCounter.current();
    }

    ///// VITAE contract specific functions /////

    // // This function mints tokens
    function _mint(address to, uint256 tokenId) internal virtual override {
        require(to != address(0), "ERC721: mint to the zero address");
        require(!_exists(tokenId), "ERC721: token already minted");

        _beforeTokenTransfer(address(0), to, 1);

        // Check that tokenId was not minted by `_beforeTokenTransfer` hook
        require(!_exists(tokenId), "ERC721: token already minted");

        unchecked {
            // Will not overflow unless all 2**256 token ids are minted to the same owner.
            // Given that tokens are minted one by one, it is impossible in practice that
            // this ever happens. Might change if we allow batch minting.
            // The ERC fails to describe this case.
            _balances[to] += 1;
        }

        _owners[tokenId] = to;

        emit Transfer(address(0), to, tokenId);

        _afterTokenTransfer(address(0), to, tokenId);
    }

    //_minters[tokenId] = msg.sender;

    // This function allows the owner of the token to burn it
    function deleteCredential(uint256 tokenId) external {
        require(
            ownerOf(tokenId) == msg.sender,
            "Only the owner or the issuer of the credential can delete it."
        );
        _burn(tokenId);
    }

    // This function allows the contract owner(us) to burn the token. As written, only the contract creator(us) can revoke the credential
    // TODO: This function should also be callable by the issuer, create a modifier requiring msg.sender to be verified as tokenId issuer address
    function revokeCredential(uint256 tokenId) external {
        // require(
        //     _minters[tokenId] == msg.sender,
        //     "Only the issuer can revoke a credential"
        // );
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
