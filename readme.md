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


Send money
----------

    $ dymka send --to 0x97E6aF105A1061975fdA6C6D0e7544b7C3600EBC --value 1000000000000000000 --gasPrice 1000000000 -e

Note that `-e` or `--estimate` stands for 'estimate gas'. Alternatively you
can specify `--gas 21000`.


Compile contract
----------------

There is [demo](demo.sol) contract, compile it lile the following so we get `demo.json`.

    solc --combined-json abi,bin --optimize demo.sol >demo.json


Deploy contract
---------------

    $ dymka deploy -c demo
    {'hash': '0xe4a8eeb6dc8a21e430077d460d2618c6a0a380e71dfecadcf4ceb252bae729b3',
     'receipt': {...
                 'contractAddress': '0xbABA05e6c21551bb50caF7C684a1Fc9B57B02A9A',
                 ...}


Call contract
-------------

    $ dymka -c demo -a 0xbABA05e6c21551bb50caF7C684a1Fc9B57B02A9A call value
    {'result': 42}

    $ dymka -c demo -a 0xbABA05e6c21551bb50caF7C684a1Fc9B57B02A9A call compare 45
    {'result': [True, False]}


Invoke contract
---------------

    dymka -c demo -a 0xbABA05e6c21551bb50caF7C684a1Fc9B57B02A9A invoke set 42 100
    dymka -c demo -a 0xbABA05e6c21551bb50caF7C684a1Fc9B57B02A9A invoke act
