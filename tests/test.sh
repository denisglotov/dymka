#!/bin/bash
cd $(dirname $0)

dymka version
dymka balance

# From account must be set by travis beforehand.
[ -v WEB3_FROM ] || ( echo "WEB3_FROM must be set for this script to run" && exit 1 )

# Deploy demo contract.
ADDR=$(dymka -c demo deploy | jq -r ".receipt.contractAddress")
export WEB3_CONTRACT_DEMO="$ADDR"

# Call value() function.
RES=$(dymka -c demo call value | jq -r ".result")
[ "$RES" == "42" ] || ( echo "Wrong initial value" && exit 1 )

# Invoke act() function.
dymka -c demo send act

# Call value() function.
RES=$(dymka -c demo call value | jq -r ".result")
[ "$RES" == "43" ] || ( echo "Wrong initial value" && exit 1 )

echo "Success."
