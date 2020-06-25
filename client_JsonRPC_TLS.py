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

while True:
    x_ = json.dumps({"id":  0, "jsonrpc" : "2.0", "method": 'AUTHENTICATE', "params" : {"username" : "admin", "password": "NTc3MzQ1NzEyMDEwMjk2NTE4MQ=="}}).encode('utf-8')

    x0 = json.dumps({"id":  0, "jsonrpc" : "2.0", "method": 'HEIGHT->BLOCK', "params" : { "sessionKey": "4efe36adc5a118e5cf14a910f0ba618ee94d0a8dc1fb293a7c5fd96a4429f907", "methodParams": {"gbHeight" : 100} } }).encode('utf-8')

    x1 = json.dumps({"id": 1, "jsonrpc" : "2.0", "method": '[HEIGHT]->[BLOCK]', "params" : {"gbHeights": [100, 101, 102]}}).encode('utf-8')

    x2 = json.dumps({"id" : 2, "jsonrpc" : "2.0",  "method": 'HASH->BLOCK', "params" : {"gbBlockHash" : '00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee'}}).encode('utf-8')

    x3 = json.dumps({"id" : 3, "jsonrpc" : "2.0",  "method": '[HASH]->[BLOCK]', "params" : {"gbBlockHashes":
                                           ['000000000000000002af2a6de04d4a1a73973827eae348fe4d3f4d05610ff968',
                                            '000000000000000007fc734cbf1fc04c59cf7ecb6af0707fd5cf5b8d46dc4c75'
                                           ]}}).encode('utf-8')

    x4 = json.dumps({"id": 4, "jsonrpc" : "2.0",  "method" : 'TXID->TX', "params" : {"gtTxHash" : '3e7861a8f18df990bf3b074718018cf7a1e7f32447bbf13ffc93327b7bf608ac'}}).encode('utf-8')

    x5 = json.dumps({"id": 5, "jsonrpc" : "2.0",  "method" : 'TXID->RAWTX', "params" : {"gtRTxHash" : '3e7861a8f18df990bf3b074718018cf7a1e7f32447bbf13ffc93327b7bf608ac'}}).encode('utf-8')

    x6 = json.dumps({"id" : 6, "jsonrpc" : "2.0",  "method": '[TXID]->[TX]', "params" : {"gtTxHashes" :
                                        ['3e7861a8f18df990bf3b074718018cf7a1e7f32447bbf13ffc93327b7bf608ac',
                                         '54c693db802d83596e3a0cdec1f99dc01af246ca51b82adaad2f41e0a8fb2131'
                                        ]}}).encode('utf-8')

    x7 = json.dumps({"id" : 7, "jsonrpc" : "2.0",  "method": '[TXID]->[RAWTX]', "params" : {"gtRTxHashes" :
                                        ['3e7861a8f18df990bf3b074718018cf7a1e7f32447bbf13ffc93327b7bf608ac',
                                         '54c693db802d83596e3a0cdec1f99dc01af246ca51b82adaad2f41e0a8fb2131'
                                        ]}}).encode('utf-8')

    x8 = json.dumps({"id": 8, "jsonrpc" : "2.0",  "method" : 'ADDR->[OUTPUT]', "params" : {"gaAddrOutputs" : '18TLpiL4UFwmQY8nnnjmh2um11dFzZnBd9', "gaPageSize" : 2}}).encode('utf-8')

    x9 = json.dumps({"id" : 9, "jsonrpc" : "2.0",  "method" : '[ADDR]->[OUTPUT]', "params" : {"gasAddrOutputs" :
                                            ['14QdCax3sR6ZVMo6smMyUNzN5Fx9zA8Sjj',
                                             '17VaRoTC8dkb6vHyE37EPZByzpKvK1u2ZU',
                                             '1NGw8LYZ93g2RiZpiP4eCniU4YmQjH1tP9',
                                             '1EHM42QUBLSA9AdJGH6XmAMYSnh7rzTPuR',
                                             '1JbmUfm9fpu5o9BfCATRhbp4NiDR5D3UBX',
                                             '14gMdTsvq3Q6PnXK5jhn8KVgvWJnxzDV5m',
                                             '18E2ymquodpWHNhNzo8BC8d6QDwJNsEaYV',
                                             '1A6NvRKPsswAX8wwPKY4Ti5FBeNCpne1NC'],
                                             "gasPageSize": 5, "lastNominalTxIndex" : 121129000000003
                                             }}).encode('utf-8')

    x10 = json.dumps({"id": 10, "jsonrpc" : "2.0",  "method" : 'SCRIPTHASH->[OUTPUT]', "params" : {"gaScriptHashOutputs" : '8ad0ed1cf403f3d4f589b6b05195d7932425620b0b42e7bfce0295df6f1e3c67', "gaScriptHashPageSize" : 2}}).encode('utf-8')

    x11 = json.dumps({"id" : 11, "jsonrpc" : "2.0",  "method" : '[SCRIPTHASH]->[OUTPUT]', "params" : {"gasScriptHashOutputs" :
                                            ['8ad0ed1cf403f3d4f589b6b05195d7932425620b0b42e7bfce0295df6f1e3c67',
                                             '1fb931ea41f204ce837f63dcffdec09720c8c8d285196050d32fd4e5dc2915be',
                                             'a77c108d9b34194bf6e83145a86e867b74cefa959d16d363b0bee31aa1799160',
                                             '41ae9fa8b864c24467cc8d9bd18c04bbcaa98086dfea8de3366e901b1d5f2fd3',
                                             '5afb578976d3bbfd470f906586cb33abf64830563e0c43255b34a421665e04f7',
                                             '050d94209dfbc9150fad697c37defc83089b138105d23d32e3e6c32eb78f4429',
                                             '946f050043939a8e3d4ccf3ef393d0d8832141dcbdcb9c2363ac78cc3649d080',
                                             'f8f3ff7bb10bc246a0c657c8f79c47db7588b086072e11d821489f461b41b2f5',
                                             '18401302386e56dd7309aa10fb89a7db1bbe77bc6bff5fda8619a9b11a809497',
                                             '81dcf5b60b87b03c66ab530fed899c656c6a3b03f45352ad5f949bd9bfc328e7'],
                                             "gasScriptHashPageSize" : 5, "lastNominalTxIndex" : 2086000000001}}).encode('utf-8')

    x12 = json.dumps({"id" : 12, "jsonrpc" : "2.0",  "method": 'TXID->[MNODE]', "params" : { "gmbMerkleBranch": '54c693db802d83596e3a0cdec1f99dc01af246ca51b82adaad2f41e0a8fb2131'}}).encode('utf-8')

    x13 = json.dumps({"id" : 13, "jsonrpc" : "2.0",  "method": 'NAME->[OUTPOINT]', "params" : {"gaName": '[h', "gaIsProducer": True}}).encode('utf-8')

    gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
    hexValue = bytes.fromhex("0100000002fddfd1fbf8072d9740564ea23d0822a8f35d52da586077c6601c74db889795fd040000008a473044022060caf1a091ac111ac039cd2faf5a78de550a378166f086c7303fe5df0c1ad52602206e28097ebb0dc6f781b8fc05a114847f07023d20e4cd54c4f5b35fcce7aa9ad6014104a164392fc49f54ff3806b6287d487a572eebba2f7a4a0f668dc3d192f1c4e4788d0c8fde41adc24d424c95b42b0e2ab988c38fe6e68790b419892abde4bbaf11ffffffff38aa1ff4695d937db4677085d9fdd7fe30992b05b56e416730fda4e10498ce51000000008a47304402201e986e1db9c24a3131754c797b678983a443f933446f2baf59220457ff546ae40220457add517cb3718bffc1c6903a736a9f534421331388dbb98fab36b794e7de4e014104a164392fc49f54ff3806b6287d487a572eebba2f7a4a0f668dc3d192f1c4e4788d0c8fde41adc24d424c95b42b0e2ab988c38fe6e68790b419892abde4bbaf11ffffffff06000000000000000091006a0f416c6c65676f72792f416c6c5061794c7d84000181185b8500820000830082000181830068586f6b656e50325068736f6d657572693181830082000281830068586f6b656e50325068736f6d6575726932828300830082000381830068586f6b656e50325068736f6d657572693318678301830082000481830068586f6b656e50325068736f6d6575726934186840420f000000000017a914a9974100aeee974a20cda9a2f545704a0ab54fdc87400d03000000000017a9147d13547544ecc1f28eda0c0766ef4eb214de104587400d03000000000017a9147d13547544ecc1f28eda0c0766ef4eb214de104587400d03000000000017a9147d13547544ecc1f28eda0c0766ef4eb214de104587400d03000000000017a9147d13547544ecc1f28eda0c0766ef4eb214de10458700000000")
    gzx = gzip_compress.compress(hexValue) + gzip_compress.flush()
    rTx = base64.b64encode(gzx).decode('utf-8')
    x14 = json.dumps({"id": 14, "jsonrpc" : "2.0",  "method": 'RELAY_TX', "params": {"rTx" : rTx }}).encode('utf-8')

    c = Bitcoin()
    priv = sha256('allegory allpay test dummy seed')
    pub = c.privtopub(priv)
    addr = c.pubtoaddr(pub)


    
    #processReqResp(sock, x_)
    processReqResp(sock, x0)
    # processReqResp(sock, x1)
    # processReqResp(sock, x2)
    # processReqResp(sock, x3)
    # processReqResp(sock, x4)
    # processReqResp(sock, x5)
    # processReqResp(sock, x6)
    # processReqResp(sock, x7)
    # processReqResp(sock, x8)
    # processReqResp(sock, x9)
    # processReqResp(sock, x10)
    # processReqResp(sock, x11)
    # processReqResp(sock, x12)
    # processReqResp(sock, x13)
    # processReqResp(sock, x14)

    exit()
