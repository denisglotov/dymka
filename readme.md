Dymka
=====

Minimalist command line tool for interacting with Ethereum-based blockchains.

Install the tool:

    pip install --user dymka

Following are the usage examples.


Raw RPC requests
----------------

    $ dymka exec web3_clientVersion
    {'id': 0,
     'jsonrpc': '2.0',
      'result': 'Geth/v1.8.25-omnibus-c41559d0/linux-amd64/go1.11.1'}

    $ dymka exec rpc_modules
    {'id': 0,
     'jsonrpc': '2.0',
      'result': {'eth': '1.0', 'net': '1.0', 'rpc': '1.0', 'web3': '1.0'}}

    $ dymka exec web3_sha3 "0x68656c6c6f20776f726c64"
    {'id': 0,
     'jsonrpc': '2.0',
      'result': '0x47173285a8d7341e5e972fc677286384f802f8ef42a5ec5f03bbfa254cb01fad'}

See https://github.com/ethereum/wiki/wiki/JSON-RPC and
https://github.com/ethereum/go-ethereum/wiki/Management-APIs for more.


Balance of accounts
-------------------

    $ dymka balance 0x2ae307B3d04E60cBeAcdbE4cb95e811d496BA875
    [{'account': '0x2ae307B3d04E60cBeAcdbE4cb95e811d496BA875', 'balance': 0}]
