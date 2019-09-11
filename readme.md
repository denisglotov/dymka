Dymka
=====

<img align="right" src="https://denisglotov.github.io/dymka/dymka.jpg">

Minimalist command line tool for interacting with Ethereum-based blockchains.

Install the tool:

    pip install --user dymka

Following are the usage examples.


Configuring provider and 'from' account
---------------------------------------

Unless your web3 provider is 'http://localhost:8545', you can use the
`--provider` and specify it every time you run the tool. Or you may create a
file `myprovider` with the following content:

    --provider
    https://rinkeby.infura.io/v3/...

and run the tool with it: `dymka @myprovider exec eth_blockNumber`. Or you may
use evironment variable like the following:

    export WEB3_PROVIDER=https://rinkeby.infura.io/v3/...

To specify the account that you use to transact from, use `--from` to specify
account keystore file (and `--password` to specify the file with its pass
phrase) or specify a private key.

Similarly to above, you can put this to a file, say `myaccount`:

    --from
    account.json
    --password
    account.password.txt

and run the tool with it: `dymka @myprovider @myaccount balance`.


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

See ethereum wiki [JSON-RPC] and [Managment APIs] for more details.

[JSON-RPC]: https://github.com/ethereum/wiki/wiki/JSON-RPC
[Managment APIs]: https://github.com/ethereum/go-ethereum/wiki/Management-APIs

Balance and nonce of accounts
-----------------------------

    $ dymka balance 0x2ae307B3d04E60cBeAcdbE4cb95e811d496BA875
    [{'account': '0x2ae307B3d04E60cBeAcdbE4cb95e811d496BA875', 'result': 0}]

    $ dymka nonce 0x2ae307B3d04E60cBeAcdbE4cb95e811d496BA875
    [{'account': '0x2ae307B3d04E60cBeAcdbE4cb95e811d496BA875', 'result': 0}]


Send money
----------

    dymka @myaccount send --to 0x97E6aF105A1061975fdA6C6D0e7544b7C3600EBC --value 1000000000000000000 --gasPrice 1000000000 -e

Note that `-e` or `--estimate` stands for 'estimate gas'. Alternatively you
can specify `--gas 21000`.


Compile contract
----------------

There is [demo](demo.sol) contract, compile it like the following so we get
`demo.json`.

    solc --combined-json abi,bin --optimize demo.sol >demo.json


Deploy contract
---------------

    $ dymka @myaccount deploy -c demo
    {'hash': '0xe4a8eeb6dc8a21e430077d460d2618c6a0a380e71dfecadcf4ceb252bae729b3',
     'receipt': {...
                 'contractAddress': '0xbABA05e6c21551bb50caF7C684a1Fc9B57B02A9A',
                 ...}

If you need to send money to the contract being deployed, use `--value`.

For convenience, export the address as environment variable as following.

    export WEB3_CONTRACT_DEMO=0xbABA05e6c21551bb50caF7C684a1Fc9B57B02A9A

Alternatively, you may specify the address every time you want to call/send to
the contract with `-a 0xbABA05e6c21551bb50caF7C684a1Fc9B57B02A9A`.


Call contract
-------------

    $ dymka @myaccount -c demo call value
    {'result': 42}

    $ dymka @myaccount -c demo call compare 45
    {'result': [True, False]}


Invoke contract
---------------

    dymka @myaccount -c demo send set 42 100
    dymka @myaccount -c demo send act

If you need to send money to the contract, use `--value`.


Gas price
---------

Displays gas price of the current provider
([web3.eth.gasPrice](https://web3js.readthedocs.io/en/v1.2.0/web3-eth.html#getgasprice)).

    $ dymka gas
    {'gasPrice': 1000000000}


Other commands
--------------

* `checksum` - calculate correct checksummed string for the given address,
* `show` - display used provider and from address,
* `transaction` - show transaction details for the given hash,
* `receipt` - show receipt for the given hash.
