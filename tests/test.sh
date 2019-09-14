#!/bin/bash
cd $(dirname $0)

dymka version
dymka balance

if [ ! -e WEB3_FROM ]; then
    echo "WEB3_FROM must be set for this script to run"
    exit 1
fi

# Deploy demo contract.
ADDR=$(dymka -c demo deploy | jq -r ".receipt.contractAddress")
export WEB3_CONTRACT_DEMO="$ADDR"

# Call value()
dymka -c demo call value
