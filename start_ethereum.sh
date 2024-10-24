#!/bin/bash
GETH1925="./geth"
ETH_DATA=./data

./stop_ethereum.sh
mkdir -p $ETH_DATA/keystore
cp key_new/* $ETH_DATA/keystore/
rm -rf data2/geth/chaindata/ data2/geth/lightchaindata/ data2/geth/transactions.rlp

GETH=$GETH1925
$GETH --datadir=$ETH_DATA init genesis.json
$GETH --datadir=$ETH_DATA --nodiscover --port 10004  --http --http.port 18546 --http.api "eth,net,web3,personal,txpool,admin" --txpool.pricelimit 0 --txpool.globalslots 3 --txpool.globalqueue 1 --txpool.accountslots 2 --txpool.pricebump 1 --maxpeers 32 --networkid 20191003  --verbosity 5 --allow-insecure-unlock --allow-insecure-unlock console 2> console.log


