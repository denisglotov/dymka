Dymka
=====

[![Build status]](https://travis-ci.org/denisglotov/dymka)
[![Pypi version]](https://pypi.org/project/dymka/)

[Build status]: https://travis-ci.org/denisglotov/dymka.svg?branch=master
[Pypi version]: https://img.shields.io/pypi/v/dymka.svg

Swiss-knife command line tool for interacting with Ethereum-based blockchains.

Install the tool:

    pip3 install --user dymka

Following are the usage examples.


Configuring provider and 'from' account
---------------------------------------

Unless your web3 provider is 'http://localhost:8545', you can use the
`--provider` and specify it every time you run the tool. Or you may create a
file `myprovider` with the following content:

    --provider
    https://rinkeby.infura.io/v3/...

and run the tool with it: `dymka @myprovider exec eth_blockNumber`. Or you may
use environment variable like the following:

    export WEB3_PROVIDER=https://rinkeby.infura.io/v3/...

To specify the account that you use to transact from, use `--from` to specify
account keystore file (and `--password` to specify the file with its pass
phrase) or specify a private key.

Similarly to above, you can put this to a file, say `myaccount`:

    --from
    account.json
    --password
    account.password.txt

and run the tool with it: `dymka @myprovider @myaccount balance`. Or just

    export WEB3_FROM=...

In the following examples I assume you specify both provider and 'from'
account.


Raw RPC requests
----------------

``` shell
$ dymka exec web3_clientVersion
{
    "id": 0,
    "jsonrpc": "2.0",
    "result": "EthereumJS TestRPC/v2.8.0/ethereum-js"
}

$ dymka exec rpc_modules
{
    "id": 0,
    "jsonrpc": "2.0",
    "result": {
        "eth": "1.0",
        "net": "1.0",
        "rpc": "1.0",
        "web3": "1.0",
        "evm": "1.0",
        "personal": "1.0"
    }
}

$ dymka exec web3_sha3 "'0x68656c6c6f20776f726c64'"
$ dymka exec web3_sha3 "'hello world'"
{
    "id": 0,
    "jsonrpc": "2.0",
    "result": "0x47173285a8d7341e5e972fc677286384f802f8ef42a5ec5f03bbfa254cb01fad"
}
```

See [note about arguments] below for why we need double quotes here.

See Ethereum wiki [JSON-RPC] and [Management APIs] for more details.

[note about arguments]: #note-about-arguments
[JSON-RPC]: https://github.com/ethereum/wiki/wiki/JSON-RPC
[Management APIs]: https://github.com/ethereum/go-ethereum/wiki/Management-APIs


Accounts, Balance and nonce
---------------------------

``` shell
$ dymka accounts
[
    "0xB18aE0D7F12105e36a430523721622e5930879cC"
]

$ dymka balance 0xD6F0d25305cD6F53829aF54945d6FDEC370e20a5
[
    {
        "account": "0xD6F0d25305cD6F53829aF54945d6FDEC370e20a5",
        "result": 99945104760000000000
    }
]

$ dymka nonce 0xD6F0d25305cD6F53829aF54945d6FDEC370e20a5
[
    {
        "account": "0xD6F0d25305cD6F53829aF54945d6FDEC370e20a5",
        "result": 40
    }
]
```

Send money
----------

``` shell
dymka send --to 0xb92FbF90bFAC4a34557bbA17b91204C8D36a5055 \
           --value 1000000000000000000 \
           --gasPrice 1000000000 -e
```

Note that `-e` or `--estimate` stands for 'estimate gas'. Alternatively you can
specify `--gas 21000`.


Compile contract
----------------

There is [Demo] contract, compile it like the following so we get `demo.json`.

``` shell
solc --combined-json abi,bin --optimize demo.sol >demo.json
```

or with docker image

``` shell
cd tests
docker run --rm -v $PWD:/src:ro ethereum/solc:0.5.9 \
    /src/demo.sol --combined-json abi,bin --optimize >demo.json
```

[Demo]: https://github.com/denisglotov/dymka/blob/master/tests/demo.sol


Deploy contract
---------------

``` shell
$ dymka -c demo deploy
{
    "hash": "0xe4a8eeb6dc8a21e430077d460d2618c6a0a380e71dfecadcf4ceb252bae729b3",
    "receipt": {...
        "contractAddress": "0xbABA05e6c21551bb50caF7C684a1Fc9B57B02A9A",
    ...}
}
```

If you need to send money to the contract being deployed, use `--value`.

For convenience, export the address as environment variable as following.

``` shell
export WEB3_CONTRACT_DEMO=0xbABA05e6c21551bb50caF7C684a1Fc9B57B02A9A

```

Alternatively, you may specify the address every time you want to call/send to
the contract with `-a 0xbABA05e6c21551bb50caF7C684a1Fc9B57B02A9A`.


Call contract
-------------

``` shell
$ dymka -c demo call value
{
    "result": 42
}

$ dymka -c demo call compare 45
{
    "result": [
        false,
        true
    ]
}

```

Invoke contract
---------------

``` shell
dymka -c demo send set 42 100
dymka -c demo send act
```

If you need to send money to the contract, use `--value`.


Events
------

To list the events of the contract for blocks from 1 till 3:
``` shell
$ dymka -a 0xbABA05e6c21551bb50caF7C684a1Fc9B57B02A9A -j demo.abi.json events 1-3
```

Gas price
---------

Displays gas price of the current provider
([web3.eth.gasPrice](https://web3py.readthedocs.io/en/stable/web3.eth.html?highlight=gasPrice#web3.eth.Eth.gas_price)).

    $ dymka gas
    {
        "gasPrice": 20000000000
    }


Other commands
--------------

* `accounts` - list available accounts,
* `checksum` - calculate correct checksummed string for the given address,
* `show` - display used provider and from address,
* `transaction` - show transaction details for the given hash,
* `receipt` - show receipt for the given hash,
* `keccak` - calculate Keccak-256 of the given string argument,
* `chain` - return an integer value for the currently configured “Chain Id”
  value introduced in [EIP-155] (delegates to `eth_chainId` RPC Method),
* `help` - shows full list of commands and short command description.

[EIP-155]: https://github.com/ethereum/EIPs/blob/master/EIPS/eip-155.md


Note about arguments
--------------------

Arguments for deploy, call and send contracts are first evaluated with python
(`eval()`). Thus addresses should be quoted twice like the following.

``` shell
$ dymka -c demo send teardown "\"0x0000000000000000000000000000000000000000\""
```

The outer quotes are consumed by your shell (e.g. bash) and the inner
(escaped) quotes are consumed by python to make sure your address is not
evaluated to the plain number 0. Use `-vd` (verbose and dry run) to see how
your arguments are evaluated.


Troubleshooting
---------------

Use `-v` and `-vv` flags to see more information. File an [issue]
or send a pull request so I try to help and review.

[issue]: https://github.com/denisglotov/dymka/issues/new


Developer hints
---------------

To set up virtual environment

``` shell
PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
```

To run it from there

``` shell
pipenv run ./dymka -V
```

To publish the new version to pypi

``` shell
python3 -m pip install --user --upgrade setuptools wheel twine
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```
Taken from https://packaging.python.org/tutorials/packaging-projects/.


Why should I trust dymka
------------------------

Dymka source code is open and kept reasonably small for review, it resides in
a single file [dymka] for simplicity. The only runtime [dependency] is a [Web3
python library] that does all actions. Dymka actually is a thin command-line
wrapper over it. Dymka can be used with no Internet access, it only needs to
access its web3 provider (gateway node). No telemetry or other requests are
ever made.


[dymka]: https://web3py.readthedocs.io/
[dependency]: https://github.com/denisglotov/dymka/blob/dev/Pipfile
[Web3 python library]: https://web3py.readthedocs.io/


Donate
------

If you find the tool useful, please donate to ethereum address
0xb92FbF90bFAC4a34557bbA17b91204C8D36a5055.

![qr](https://denisglotov.github.io/dymka/0xb92FbF90bFAC4a34557bbA17b91204C8D36a5055.png)

Happy hacking 🐱.
