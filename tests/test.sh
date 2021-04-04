#!/bin/bash -x
cd $(dirname $0)

die() {
    echo $1
    exit 1
}

dymka version
dymka block
dymka accounts
dymka balance

# From account must be set by travis beforehand.
[ -v WEB3_FROM ] || die "WEB3_FROM must be set for this script to run"

echo
echo "Deploy Demo contract."
ADDR=$(dymka -c demo deploy | tee /dev/tty | jq -r ".receipt.contractAddress")
export WEB3_CONTRACT_DEMO="$ADDR"

echo
echo "Call its value() function."
RES=$(dymka -c demo call value | tee /dev/tty | jq -r ".result")
[ "$RES" == "42" ] || die "Wrong initial value $RES"

echo
echo "Invoke its act() function."
dymka -c demo send act

echo
echo "Call value() function again. Must be 43."
RES=$(dymka -c demo call value | tee /dev/tty | jq -r ".result")
[ "$RES" == "43" ] || die "Wrong value $RES"

echo
echo "Call compare(45) function."
RES=$(dymka -c demo call compare 45 | tee /dev/tty | jq -r ".result")
[ $(echo "$RES" | tr -d '[:space:]') == "[false,true]" ] || die "Wrong $RES"

echo
echo "Invoke its set(43, 100) function."
dymka -c demo send set 43 100

echo
echo "Call value() function (with abi only). Must be 100."
RES=$(dymka -j demo.abi.json -c demo call value | jq -r ".result")
[ "$RES" == "100" ] || die "Wrong value $RES"

LOGS=$(dymka -j demo.abi.json -c demo events 1- | tee /dev/tty)
[ $(echo "$LOGS" | jq .[0].event) == "Acted" ] || die "Wrong 1st log"

echo
echo "Invoke its teardown() function."
dymka -c demo send teardown "'0x0000000000000000000000000000000000000000'"

echo "Success."
