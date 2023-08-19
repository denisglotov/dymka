#!/bin/bash -eux
cd $(dirname $0)

die() {
    echo $1
    exit 1
}

dymka version
dymka id
dymka block

FROM=$(dymka accounts | jq -r ".[0]")
dymka balance $FROM

echo
echo "Deploy Demo contract."
ADDR=$(dymka -c demo deploy  | jq -r ".receipt.contractAddress")
export WEB3_CONTRACT_DEMO="$ADDR"

echo
echo "Call its value() function."
RES=$(dymka -c demo call value  | jq -r ".result")
[ "$RES" == "42" ] || die "Wrong initial value $RES"

echo
echo "Invoke its act() function."
dymka -c demo send act

echo
echo "Call value() function again. Must be 43."
RES=$(dymka -c demo call value  | jq -r ".result")
[ "$RES" == "43" ] || die "Wrong value $RES"

echo
echo "Call compare(45) function."
RES=$(dymka -c demo call compare 45  | jq -r ".result")
[ $(echo "$RES" | tr -d '[:space:]') == "[false,true]" ] || die "Wrong $RES"

echo
echo "Invoke its set(43, 100) function."
dymka -c demo send set 43 100

echo
echo "Call value() function (with abi only). Must be 100."
RES=$(dymka -j demo.abi.json -c demo call value | jq -r ".result")
[ "$RES" == "100" ] || die "Wrong value $RES"

set +x
LOGS=$(dymka -j demo.abi.json -c demo events 1-)
[ $(echo "$LOGS" | jq -r .[0].event) == "Acted" ] || die "Wrong 1st log name $LOGS"
[ $(echo "$LOGS" | jq -r .[0].args.who) == $FROM ] || die "Wrong 1st log arg $LOGS"
[ $(echo "$LOGS" | jq -r .[1].event) == "Updated" ] || die "Wrong 2nd log name $LOGS"
[ $(echo "$LOGS" | jq -r .[1].args.value) == "43" ] || die "Wrong 2nd log arg $LOGS"
[ $(echo "$LOGS" | jq -r .[2].event) == "Updated" ] || die "Wrong 3rd log name $LOGS"
set -x

echo
echo "Invoke its teardown() function."
dymka -c demo send teardown "'0x0000000000000000000000000000000000000000'"

echo "Success."
