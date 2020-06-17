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
        size = s.recv(32)
        print(int.from_bytes(size, byteorder='big'))
        raw = s.recv(int.from_bytes(size, byteorder='big'))
        try:
            finalResp += raw.decode('ascii')
            x = json.loads(''.join(finalResp))
            break
        except:
            if not raw:
                break
    data = json.loads(finalResp)
    print('Received', data)

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

while True:

    name = sha256('test')

    x0 = json.dumps({"id":  0, "jsonrpc" : "2.0", "method": 'ADD_XPUBKEY', "params" : {"xpubKey" : 'xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8', "addressCount": 2, "allegoryHash": name}}).encode('utf-8')

    x1 = json.dumps({"id": 1, "jsonrpc" : "2.0", "method": 'NAME->ADDR', "params" : {"allegoryHash": name}}).encode('utf-8')

    processReqResp(sock, x0)
    processReqResp(sock, x1)
    processReqResp(sock, x1)
    exit()
