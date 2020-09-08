#!/usr/bin/python
# -*- coding: utf-8 -*-

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
    x = recvResponse(s)

def sendRequest(s, payload):
    ln = len (payload)
    prefix = (ln).to_bytes(4, byteorder='big')
    s.sendall(prefix + payload)

def recvResponse(s):
    raw = s.recv()
    prefix = raw[:4]
    leng = int.from_bytes(prefix, byteorder='big')
    full = raw [4:]
    cumlen = len(raw) - 4
    while (leng > cumlen):
        cur = s.recv()
        cumlen = cumlen + len(cur)
        full = full + cur
    return full

def client(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(100)
    wrappedSocket = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_1)
    wrappedSocket.connect((hostname, int(port)))
    return wrappedSocket

config = configparser.ConfigParser()
config.read('name_buying.ini')
user = config['credentials']['username']
pswd = config['credentials']['password']

sock = client(config['nexa']['host'], config['nexa']['port'])

sessionKey = 'bb9af882d2a32cd40e817742bac0d21be1ceda8d496cff0308140d893850363a' 

if(len(sys.argv) < 5):
    print("Arguments: <input tx> <input index> <input amount> <name>")
    exit(0)

inputTxId = sys.argv[1]
inputTxIndex = sys.argv[2]
inputAmount = sys.argv[3]

name = list(map(ord, sys.argv[4]))

while True:
 
#############################
# Purchase an Allegory name
# Sign partially signed transaction
# Relay transaction
#############################
 
    c = Bitcoin(testnet=True, hashcode=0x41)
    priv = '8d9e5dd0761ead0fe1040ba7b4a8841be87b2f6842586596823d15942fdb1810' 
    pub = c.privtopub(priv)
    addr = c.privtoaddr(priv) 
    print('Address: ' + addr)
    inputsD = \
        [({"opTxHash": inputTxId, "opIndex": int(inputTxIndex)}, int(inputAmount))]

    x0 = json.dumps(
        {
            "id": 17, 
            "jsonrpc": "2.0",  
            "method": 'PS_ALLEGORY_TX', 
            "params": {
                "sessionKey": sessionKey, 
                "methodParams": {
                    "paymentInputs": inputsD,
                    "name": (name, False), 
                    "outputOwner": "mzLLg4LGQVNAAPgq9wxAcQtzBQ8Uk8eeB6", 
                    "outputChange": "mzLLg4LGQVNAAPgq9wxAcQtzBQ8Uk8eeB6"
                }
            }
        }).encode('utf-8')
        
    print("\n\nName purchasing (PS_ALLEGORY_TX) JSON request: ", x0)
    sendRequest(sock, x0)
    respPsaTx1 = recvResponse(sock)
    print("\n\nRaw JSON Response: ", respPsaTx1)

    psaTx = base64.b64decode(json.loads(respPsaTx1)["result"]["psaTx"].encode('utf-8'))
    print("\n\nPartially signed Allegory Tx: ", serialize(json.loads(psaTx)))

    psaTxObj = json.loads(psaTx)
    psaTxObj["ins"][1]['amount'] = int(inputAmount) # required for cryptos to sign input
    psaTx = json.dumps(psaTxObj)

    fsaTx = c.sign(json.loads(psaTx), 1, priv)

    serFsaTxHex = serialize(fsaTx)
    print("\n\nFully signed Allegory Tx (", txhash(serFsaTxHex), "): ", serFsaTxHex)

    b64FsaTx = (base64.b64encode(bytes.fromhex(serFsaTxHex))).decode('utf-8')

    x1 = json.dumps(
        {
            "id": 14, 
            "jsonrpc" : "2.0",  
            "method": 'RELAY_TX', 
            "params": {
                "sessionKey": sessionKey, 
                "methodParams": {
                    "rawTx" : b64FsaTx
                }
            }
        }).encode('utf-8')
    
    print("\n\nFully signed transaction relaying JSON request: ", x1)
    sendRequest(sock, x1)
    print("\n\n")
    respRelayTx1 = recvResponse(sock)
    
#############################

    print("Done all APIs, keeping connection open for 10 secs.")
    time.sleep(10)
    print("Bye.")
    exit()
    
