#!/bin/bash
for i in 1
do
init_addr=$(bitcoin-cli -regtest getnewaddress)
vout=0
val=3
self=0.999995
init_tx=$(bitcoin-cli -regtest sendtoaddress $init_addr $val)
txid=$init_tx
echo $txid
nb=$( bitcoin-cli -regtest generatetoaddress 1 $(bitcoin-cli -regtest getnewaddress))
echo $nb
sleep 5
for j in {1..2}
do
amt=$(python -c "print($val - 1)")
chg_addr=$(bitcoin-cli -regtest getnewaddress)
new_addr=$(bitcoin-cli -regtest getnewaddress)
#echo $new_addr

raw_tx=$(bitcoin-cli -regtest createrawtransaction '''
    [
      {
        "txid": "'$txid'",
        "vout": '$vout'
      }
    ]
    ''' '''
    {
      "'$new_addr'": '$amt',
      "'$chg_addr'": '$self'
    }'''
)
#echo $raw_tx
s_tx=$(bitcoin-cli -regtest signrawtransaction $raw_tx | jq -r .hex)
#echo $s_tx
txid=$(bitcoin-cli -regtest sendrawtransaction $s_tx)
echo $txid
val=$amt
sleep 5
done
done
