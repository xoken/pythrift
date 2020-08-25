#!/usr/bin/python
# -*- coding: utf-8 -*-

import gzip
import zlib
import base64
import sys
import glob
import time
import socket
import threading
from cryptos import *
from cbor2 import dumps, loads, CBORTag
import codecs
import binascii
import ssl
import json
import configparser
import bitsv
import hashlib
import base58

def frame_op_return(op_return):
    if int(len(op_return)) <= 75:
        # 0x4b
        fmtStr = '%02x'
    elif int(len(op_return)) < 255:
        # 0x4c
        fmtStr = '4c%02x'
    elif int(len(op_return)) < 65535:
        # 0x4d
        fmtStr = '4d%04x'
    else:
        # 0x4e
        fmtStr = '4e%08x'

    # OP_RETURN Allegory/AllPay
    prefix = bytes.fromhex('006a0f416c6c65676f72792f416c6c506179')
    lens = fmtStr % int(len(op_return))
    lenb = bytes.fromhex(lens)
    fs = prefix + lenb + op_return
    print('final', fs)
    return fs


def getSessionKey(user, pswd, sock):
    authRq = json.dumps({"id":  0, "jsonrpc" : "2.0", "method": 'AUTHENTICATE', "params" : {"username" : user, "password": pswd}}).encode('utf-8')
    sendRequest(sock, authRq)
    rawResp = sock.recv()
    prefix = rawResp[:4]
    length = int.from_bytes(prefix, byteorder='big')
    full = rawResp[4:]
    cumlen = len(rawResp) - 4
    while(length > cumlen):
        curr = sock.recv()
        cumlen = cumlen + len(curr)
        full = full + curr
    respObj = json.loads(full);
    return respObj["result"]["auth"]["sessionKey"]

def processReqResp(s, payload):
    sendRequest(s, payload)
    print("send request:", payload)
    print("\n-----------------------------------------")
    x = recvResponse(s)
    print("-----------------------------------------\n")

def sendRequest(s, payload):
    ln = len (payload)
    prefix = (ln).to_bytes(4, byteorder='big')
    s.sendall(prefix + payload)

def recvResponse(s):
    raw = s.recv()
    print('Received 1st', raw)
    prefix = raw[:4]
    leng = int.from_bytes(prefix, byteorder='big')
    print ('Prefixed Length: ', leng)
    full = raw [4:]
    cumlen = len(raw) - 4
    while (leng > cumlen):
        cur = s.recv()
        print('Received next', cur)
        cumlen = cumlen + len(cur)
        full = full + cur
    print ('Full msg: ', full)
    return full

def client(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(100)
    wrappedSocket = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_1)
    wrappedSocket.connect((hostname, int(port)))
    return wrappedSocket

# start
# command line args for host, port
if len(sys.argv) < 3:
    print('Invalid args, need: <hostname> <port>')
    exit(0)

sock = client(sys.argv[1], sys.argv[2])

config = configparser.ConfigParser()
config.read('client.ini')
user = config['credentials']['username']
pswd = config['credentials']['password']

sessionKey = '29725256988c1c1eba484eb390b84ce637ac13118c22295f0cc48e38f763bb59' # getSessionKey(user, pswd, sock)

while True:
 
#############################
# Allegory partially sign Txn
# Relay Txn
#############################
 
    c = Bitcoin(testnet = True, hashcode=SIGHASH_FORKID)
    priv = '84f492a6e83f796c6563ba87bb33fa8cf78d896da69a6607d859de1fc776096d01' 
    pub = c.privtopub(priv)
    addr = c.privtoaddr(priv) # mn4vGSceDVbuSHUL6LQQ1P7RxPRkVRdyZH
    print('Address: ' + addr)
    inputsD = \
        [({"opTxHash": '9c7cfc0604d47705f55182bec232dbea821743972ec7ae84cbe7026c495ee1ff', "opIndex": 0}, 19531250)]


    x = json.dumps(
        {
            "id": 17, 
            "jsonrpc": "2.0",  
            "method": 'PS_ALLEGORY_TX', 
            "params": {
                "sessionKey": sessionKey, 
                "methodParams": {
                    "paymentInputs": inputsD,
                    "name": ([66, 105, 116, 99], False), 
                    "outputOwner": "n3o8eDUmHkFiPrPKE9ymxZnve197yHrfwr", 
                    "outputChange": "n3o8eDUmHkFiPrPKE9ymxZnve197yHrfwr"
                }
            }
        }).encode('utf-8')
        
    print("JSON Request: ", x)
    sendRequest(sock, x)
    print("\n\n")
    respPsaTx1 = recvResponse(sock)
    print("\n\nRaw JSON Response: ", respPsaTx1)

    psaTx = gzip.decompress(base64.b64decode((json.loads(respPsaTx1)["result"]["psaTx"].encode('utf-8'))))
    print("\n\nPartially signed Allegory Tx: ", psaTx)

    fsaTx = c.sign(json.loads(psaTx), 0, priv)
    print('\n\nFully signed Allegory Tx: ', fsaTx)

    serFsaTxHex = serialize(fsaTx)
    print("\n\nSerialized fully signed Allegory Tx (Hex): ", serFsaTxHex)
    serFsaTx = bytes.fromhex(serFsaTxHex)
    print("\n\nSerialized fully signed Allegory Tx: ", serFsaTx)

    hashedTx1 = txhash(serFsaTxHex) 
    print("\n\nHash of fully signed Allegory Tx: ", hashedTx1)

    b64GzippedFsaTx = (base64.b64encode(gzip.compress(serFsaTx))).decode('utf-8')
    print("\n\nBase64-encoded and GZipped fully signed Allegory Tx: ", b64GzippedFsaTx)

    x1 = json.dumps(
        {
            "id": 14, 
            "jsonrpc" : "2.0",  
            "method": 'RELAY_TX', 
            "params": {
                "sessionKey": sessionKey, 
                "methodParams": {
                    "rawTx" : b64GzippedFsaTx 
                }
            }
        }).encode('utf-8')
    
    print("\n\nJSON Request: ", x1)
    sendRequest(sock, x1)
    print("\n\n")
    respRelayTx1 = recvResponse(sock)
    

#############################

    print("Done all APIs, keeping connection open for 10 secs.")
    time.sleep(10)
    print("Bye.")
    exit()
    
