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


def processReqResp(s, payload):
    sendRequest(s, payload)
    print("send request:", payload)
    print("\n-----------------------------------------")
    x = recvResponse(s)
    print("-----------------------------------------\n")

def sendRequest(s, payload):
    s.sendall(payload)


def recvResponse(s):
    finalResp = ''
    while 1:
        raw = s.recv(16384)
        try:
            finalResp += raw.decode('ascii')
            x = json.loads(''.join(finalResp))
            break
        except:
            if not raw:
                break
    print('Received', finalResp)
    data = json.loads(finalResp)
    print('Received', data)

def client(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(100)
    wrappedSocket = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_1)
    wrappedSocket.connect((hostname, int(port)))
    return wrappedSocket

if len(sys.argv) < 3:
    print('Invalid args, need: <hostname> <port>')
    exit(0)

sock = client(sys.argv[1], sys.argv[2])

while True:

    x0 = json.dumps({"reqId":  1, "method": 'HEIGHT->BLOCK', "params" : {"gbHeight" : 100}}).encode('utf-8')

    x1 = json.dumps({"reqId": 2, "method": '[HEIGHT]->[BLOCK]', "params" : {"gbHeights": [100, 101, 102]}}).encode('utf-8')

    x2 = json.dumps({"reqId" : 3, "method": 'HASH->BLOCK', "params" : {"gbBlockHash" : '00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee'}}).encode('utf-8')

    x3 = json.dumps({"reqId" : 4, "method": '[HASH]->[BLOCK]', "params" : {"gbBlockHashes":
                                           ['000000000000000002af2a6de04d4a1a73973827eae348fe4d3f4d05610ff968',
                                            '000000000000000007fc734cbf1fc04c59cf7ecb6af0707fd5cf5b8d46dc4c75'
                                           ]}}).encode('utf-8')

    x4 = json.dumps({"reqId": 5, "method" : 'TXID->TX', "params" : {"gtTxHash" : '65de5b56d5711dfed0a914e4372ce0b5c6b3f8d7a88b40fb1cecafa51ae17f1e'}}).encode('utf-8')

    x5 = json.dumps({"reqId" : 6, "method": '[TXID]->[TX]', "params" : {"gtTxHashes" :
                                        ['65de5b56d5711dfed0a914e4372ce0b5c6b3f8d7a88b40fb1cecafa51ae17f1e',
                                         '54c693db802d83596e3a0cdec1f99dc01af246ca51b82adaad2f41e0a8fb2131'
                                        ]}}).encode('utf-8')

    x6 = json.dumps({"reqId": 7, "method" : 'ADDR->[OUTPUT]', "params" : {"gaAddrOutputs" : '13n561iVozTtMXJzAJNA5TQsnTboRvpxae'}}).encode('utf-8')

    x7 = json.dumps({"reqId" : 8, "method" : '[ADDR]->[OUTPUT]', "params" : {"gasAddrOutputs" :
                                            ['1P8Jd8qQM7y45iXLM1eiXCCmGRhCPjykZB',
                                             '16qgC3hzi38xo1vn2gGsNVwWaW1sEH3h9R']}}).encode('utf-8')

    x8 = json.dumps({"reqId" : 9, "method": 'TXID->[MNODE]', "params" : { "gmbMerkleBranch": '54c693db802d83596e3a0cdec1f99dc01af246ca51b82adaad2f41e0a8fb2131'}}).encode('utf-8')

    x9 = json.dumps({"reqId" : 10, "method": 'NAME->[OUTPOINT]', "params" : {"gaName": '[h', "gaIsProducer": True}}).encode('utf-8')

    c = Bitcoin()
    priv = sha256('allegory allpay test dummy seed')
    pub = c.privtopub(priv)
    addr = c.pubtoaddr(pub)

    processReqResp(sock, x0)
    processReqResp(sock, x1)
    processReqResp(sock, x2)
    processReqResp(sock, x3)
    processReqResp(sock, x4)
    processReqResp(sock, x5)
    processReqResp(sock, x6)
    processReqResp(sock, x7)
    processReqResp(sock, x8)
    processReqResp(sock, x9)

    exit()
