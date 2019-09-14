#!/bin/bash
cd $(dirname $0)

die() {
    echo $1
    exit 1
}

dymka version
dymka balance

# From account must be set by travis beforehand.
[ -v WEB3_FROM ] || die "WEB3_FROM must be set for this script to run"

echo "Deploy Demo contract."
ADDR=$(dymka -c demo deploy | jq -r ".receipt.contractAddress")
export WEB3_CONTRACT_DEMO="$ADDR"

echo "Call its value() function."
RES=$(dymka -c demo call value | jq -r ".result")
[ "$RES" == "42" ] || die "Wrong initial value $RES"

echo "Invoke its act() function."
dymka -c demo send act

echo "Call value() function again. Must be 43."
RES=$(dymka -c demo call value | jq -r ".result")
[ "$RES" == "43" ] || die "Wrong value $RES"

echo "Call compare(45) function."
RES=$(dymka -c demo call compare 45 | jq -r ".result")
[ $(echo "$RES" | tr -d '[:space:]') == "[false,true]" ] || die "Wrong $RES"

echo "Invoke its set(43, 100) function."
dymka -c demo send set 43 100

echo "Call value() function. Must be 100."
RES=$(dymka -c demo call value | jq -r ".result")
[ "$RES" == "100" ] || die "Wrong value $RES"

echo "Invoke its teardown() function."
dymka -c demo send teardown "'0x0000000000000000000000000000000000000000'"

echo "Success."
