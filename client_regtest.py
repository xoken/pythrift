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

sessionKey = '29725256988c1c1eba484eb390b84ce637ac13118c22295f0cc48e38f763bb59' # getSessionKey(user, pswd, sock)z

while True:
 
#############################
# Allegory partially sign Txn
# Relay Txn
#############################

    c = Bitcoin(testnet = True, hashcode=0x41)
    priv = '0f4396a043a09537e8712f49828863552bfb0ee7f763fc0c0e06f5ace8da133a01' #sha256('allegory allpay test dummy seed')
    pub = c.privtopub(priv)
    addr = c.privtoaddr(priv) # mn4vGSceDVbuSHUL6LQQ1P7RxPRkVRdyZH
    print('Address: ' + addr)
    inputs = [{'output': 'ffc4134fd708a7e0476b30a3e0d7fb6722acd29f9aae7d89a9136539b199d00a:0', 'value': 1220703}]
    outs = [{'value': 5000, 'address': 'mfX15Eq6QHZ55YnfJg8XDY4kNVim9d9PXK'}] * 200

    tx = c.mktx(inputs, outs)
    print(tx)
    txs = c.sign(tx, 0, priv)
    txser = serialize(txs)
    print(txser)
    print(txhash(txser))
    # save it for later use
    firstTxHash = txhash(txser)
    gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
    hexValue = bytes.fromhex(txser)
    print(hexValue)
    gzx = gzip_compress.compress(hexValue) + gzip_compress.flush()
    rTx = base64.b64encode(gzx).decode('utf-8')
    x14 = json.dumps({"id": 14, "jsonrpc" : "2.0",  "method": 'RELAY_TX', "params": {"sessionKey": sessionKey, "methodParams": {"rawTx" : rTx }}}).encode('utf-8')
    x = dumps((0, 1, 'RELAY_TX', [(14, rTx)]))
    processReqResp(sock,x14)

#############################

    print("Done all APIs, keeping connection open for 10 secs.")
    time.sleep(10)
    print("Bye.")
    exit()
    
