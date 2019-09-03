#!/usr/bin/env python

from pprint import pprint
from web3 import Web3, HTTPProvider
import argparse
import json
import logging
import os
import traceback

parser = argparse.ArgumentParser(description='Iteract with ethereum network.')
parser.add_argument('command',
                    help='version, show, balance, deploy, status, receipt, query, send')
parser.add_argument('arguments', nargs='*',
                    help='optional arguments to the command')
parser.add_argument('-a', '--address',
                    help='contract address to send/call')
parser.add_argument('-c', '--contract',
                    help='contract name or its json path')
parser.add_argument('-f', '--from', dest='from_account',
                    help='account name to transact from')
parser.add_argument('-t', '--to',
                    help='account address to transact to')
parser.add_argument('--chainId', type=int,
                    help='explicitly set chain id')
parser.add_argument('--config', type=argparse.FileType('r'), default='./dymka.json',
                    help='config to use, defaults to ./dymka.json')
parser.add_argument('--gas', type=int,
                    help='explicitly set gas amount')
parser.add_argument('--gasPrice', type=int,
                    help='explicitly set gas price')
parser.add_argument('--nonce',
                    help='excplicitly set nonce')
parser.add_argument('--timeout', type=int, default=120,
                    help='timeout to wait after the transaction, default is 120s')
parser.add_argument('--value', type=int,
                    help='money amount to use in transaction')

group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--verbose', action='count',
                   help='verbose output')
group.add_argument('-q', '--quiet', action='count',
                   help='quiet output')

args = parser.parse_args()


def getLogger(defaultLevel):
    log = logging.getLogger('dymka')
    if args.verbose:
        defaultLevel -= 10*args.verbose
    if args.quiet:
        defaultLevel += 10*args.quiet
    log.setLevel(defaultLevel)
    stream = logging.StreamHandler()
    stream.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    log.addHandler(stream)
    return log


log = getLogger(logging.WARN)
config = json.load(args.config)


def getJson(fname):
    with open(fname) as file:
        return json.load(file)


def getOptionalArguments(ord):
    if len(args.arguments) > ord:
        log.debug('Raw args %s', args.arguments[ord:])
        arguments = eval(str(args.arguments[ord:]))
        log.debug('Arguments: %s', arguments)
        return [arguments]
    return [[]]


def getContractData(name):
    fname = name + '.json'
    if not os.path.isfile(fname):
        fname = name
    data = getJson(fname)
    contracts_section = data['contracts']
    contracts = [key for key in contracts_section.keys() if key.endswith(name)]
    if len(contracts) != 1:
        raise ValueError('Ambigous contract list ' + contracts + ' in json ' + fname)
    contract = contracts_section[contracts[0]]
    return contract['abi'], contract['bin']


def getAddress(w3, account_name):
    if account_name:
        return w3.eth.account.from_key(config['accounts'][account_name]).address


def transact(w3, tx, private_key):
    signed = w3.eth.account.sign_transaction(tx, private_key=private_key)
    hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    log.info('Transaction hash: %s', hash.hex())
    try:
        w3.eth.waitForTransactionReceipt(hash, timeout=args.timeout)
    except Exception:
        raise ValueError('Timeout waiting ' + str(args.timeout) + 's for transaction ' +
                         hash.hex())
    return hash


def buildContractSendTx(w3, opts):
    function_name = args.arguments[0]
    abi, _ = getContractData(args.contract)
    contract = w3.eth.contract(abi=abi, address=args.address)
    arguments = getOptionalArguments(1)
    func = contract.functions[function_name]
    func_bound = func(*arguments) if arguments else func()
    return func_bound.buildTransaction(opts)


def processAccounts(fn, name, *vargs):
    pprint(list(map(lambda a: a and {'account': a, name: fn(a)},
                    [*args.arguments, *filter(None, vargs)])))


def main():
    if args.command == 'version':
        print('Version: 0.1')
        return

    provider = HTTPProvider(config['provider']['url'])
    w3 = Web3(provider)
    address_from = getAddress(w3, args.from_account)

    if args.command == 'show':
        status = {'provider': config['provider']}
        if address_from:
            status['name'] = args.from_account
            status['address'] = address_from
        pprint(status)
        return

    if args.command == 'gas':
        pprint(w3.eth.gasPrice)
        return

    if args.command == 'checksum':
        processAccounts(Web3.toChecksumAddress, 'checksummed', address_from, args.to)
        return

    if args.command == 'balance':
        processAccounts(w3.eth.getBalance, 'balance', address_from, args.to)
        return

    if args.command == 'nonce':
        processAccounts(w3.eth.getTransactionCount, 'nonce', address_from, args.to)
        return

    if args.command == 'exec':
        function = args.arguments[0]
        res = provider.make_request(function, *getOptionalArguments(1))
        pprint(res)
        return

    if args.command == 'status':
        hash = args.arguments[0]
        tx = w3.eth.getTransaction(hash)
        pprint(dict(tx))
        return

    if args.command == 'receipt':
        hash = args.arguments[0]
        receipt = w3.eth.getTransactionReceipt(hash)
        pprint(dict(receipt))
        return

    if args.command == 'call' or args.command == 'query':
        function_name = args.arguments[0]
        abi, _ = getContractData(args.contract)
        contract = w3.eth.contract(abi=abi, address=args.address)
        arguments = getOptionalArguments(1)
        func = contract.functions[function_name]
        tx = func(*arguments) if arguments else func()
        status = {'result': tx.call({'from': address_from})}
        pprint(status)
        return

    opts = {
        'from': address_from,
        'nonce': args.nonce or w3.eth.getTransactionCount(address_from)
    }
    for name in ['chainId', 'gas', 'gasPrice', 'value', 'to']:
        if vars(args)[name]:
            opts[name] = vars(args)[name]
    if args.verbose:
        print('Transaction options:', opts)

    if args.command == 'deploy':
        abi, bin = getContractData(args.contract)
        contract = w3.eth.contract(abi=abi, bytecode=bin)
        arguments = getOptionalArguments(0)
        tx = contract.constructor(*arguments).buildTransaction(opts)
        hash = transact(w3, tx, config['accounts'][args.from_account])
        status = {
            'hash': hash.hex(),
            'address': w3.eth.getTransactionReceipt(hash)['contractAddress'],
        }
        pprint(status)
        return

    if args.command == 'send' or args.command == 'invoke':
        tx = opts if not args.contract else buildContractSendTx(w3, opts)
        result = transact(w3, tx, config['accounts'][args.from_account])
        status = {
            'receipt': dict(w3.eth.getTransactionReceipt(result)),
        }
        pprint(status)
        return


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if log.isEnabledFor(logging.DEBUG):
            traceback.print_exc()
        else:
            log.error(e)
