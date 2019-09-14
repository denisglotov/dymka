#!/bin/bash
dymka version
dymka balance

# Deploy demo contract.
ADDR=$(dymka -c demo deploy | jq -r ".receipt.contractAddress")
export WEB3_CONTRACT_DEMO="$ADDR"

# Call value()
dymka -c demo call value
