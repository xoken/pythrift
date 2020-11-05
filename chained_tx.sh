#!/bin/bash
for i in {1..5}
do
init_addr=$(bitcoin-cli -regtest getnewaddress)
vout=0
val=25
self=0.999995
init_tx=$(bitcoin-cli -regtest sendtoaddress $init_addr $val)
txid=$init_tx
#nb=$( bitcoin-cli -regtest generatetoaddress 1 $(bitcoin-cli -regtest getnewaddress))
for j in {1..24}
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
done
done
