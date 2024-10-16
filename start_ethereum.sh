#!/bin/bash
GETH1925="./geth"
ETH_DATA=./data


mkdir -p $ETH_DATA/keystore
cp key_new/* $ETH_DATA/keystore/
rm -rf data2/geth/chaindata/ data2/geth/lightchaindata/ data2/geth/transactions.rlp

GETH=$GETH1925
$GETH --datadir=$ETH_DATA init genesis.json
$GETH --datadir=$ETH_DATA --nodiscover --port 10004  --http --http.port 8545 --http.api "eth,net,web3,personal,txpool,admin,debug" --miner.gaslimit=12000000 --http.vhosts=* --ws --ws.api="personal,eth,net,web3,debug" --ws.addr=0.0.0.0 --ignore-legacy-receipts --rpc.allow-unprotected-txs --dev --txpool.pricebump 1 --maxpeers 32 --networkid=1337  --allow-insecure-unlock --allow-insecure-unlock console 2> console.log


