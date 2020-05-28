#!/usr/bin/python
# -*- coding: utf-8 -*-

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
    recvResponse(s)
    print("-----------------------------------------\n")

def sendRequest(s, payload):
    s.sendall(payload)

def recvResponse(s):
    raw = s.recv()
    data = loads(raw)
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

    x0 = dumps((0, 1, 'HEIGHT->BLOCK', [(0, 100)]))

    x1 = dumps((0, 1, '[HEIGHT]->[BLOCK]', [(1, [100, 101, 102])]))

    x2 = dumps((0, 1, 'HASH->BLOCK', [(2,
                                       '00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee'
                                       )]))

    x3 = dumps((0, 1, '[HASH]->[BLOCK]', [(3,
                                           ['000000000000000002af2a6de04d4a1a73973827eae348fe4d3f4d05610ff968',
                                            '000000000000000007fc734cbf1fc04c59cf7ecb6af0707fd5cf5b8d46dc4c75'
                                            ])]))

    x4 = dumps((0, 1, 'TXID->TX', [(4,
                                    '3e7861a8f18df990bf3b074718018cf7a1e7f32447bbf13ffc93327b7bf608ac'
                                    )]))

    x5 = dumps((0, 1, '[TXID]->[TX]', [(5,
                                        ['3e7861a8f18df990bf3b074718018cf7a1e7f32447bbf13ffc93327b7bf608ac',
                                         '54c693db802d83596e3a0cdec1f99dc01af246ca51b82adaad2f41e0a8fb2131'
                                         ])]))
    x6 = dumps((0, 1, 'TXID->RAWTX', [(6,
                                       '3e7861a8f18df990bf3b074718018cf7a1e7f32447bbf13ffc93327b7bf608ac'
                                       )]))

    x7 = dumps((0, 1, '[TXID]->[RAWTX]', [(7,
                                        ['3e7861a8f18df990bf3b074718018cf7a1e7f32447bbf13ffc93327b7bf608ac',
                                         '54c693db802d83596e3a0cdec1f99dc01af246ca51b82adaad2f41e0a8fb2131'
                                         ])]))

    x8 = dumps((0, 1, 'ADDR->[OUTPUT]', [(8,
                                          '13n561iVozTtMXJzAJNA5TQsnTboRvpxae')]))

    x9 = dumps((0, 1, '[ADDR]->[OUTPUT]', [(9,
                                            ['1P8Jd8qQM7y45iXLM1eiXCCmGRhCPjykZB',
                                             '16qgC3hzi38xo1vn2gGsNVwWaW1sEH3h9R'])]))

    x10 = dumps((0, 1, 'TXID->[MNODE]', [(10,
                                         '54c693db802d83596e3a0cdec1f99dc01af246ca51b82adaad2f41e0a8fb2131'
                                         )]))

    x11 = dumps((0, 1, 'NAME->[OUTPOINT]', [(11,
                                            '[h', True
                                            )]))

    x12 = dumps((0, 1, 'RELAY_TX', [(12, bytes.fromhex("0100000002fddfd1fbf8072d9740564ea23d0822a8f35d52da586077c6601c74db889795fd040000008a473044022060caf1a091ac111ac039cd2faf5a78de550a378166f086c7303fe5df0c1ad52602206e28097ebb0dc6f781b8fc05a114847f07023d20e4cd54c4f5b35fcce7aa9ad6014104a164392fc49f54ff3806b6287d487a572eebba2f7a4a0f668dc3d192f1c4e4788d0c8fde41adc24d424c95b42b0e2ab988c38fe6e68790b419892abde4bbaf11ffffffff38aa1ff4695d937db4677085d9fdd7fe30992b05b56e416730fda4e10498ce51000000008a47304402201e986e1db9c24a3131754c797b678983a443f933446f2baf59220457ff546ae40220457add517cb3718bffc1c6903a736a9f534421331388dbb98fab36b794e7de4e014104a164392fc49f54ff3806b6287d487a572eebba2f7a4a0f668dc3d192f1c4e4788d0c8fde41adc24d424c95b42b0e2ab988c38fe6e68790b419892abde4bbaf11ffffffff06000000000000000091006a0f416c6c65676f72792f416c6c5061794c7d84000181185b8500820000830082000181830068586f6b656e50325068736f6d657572693181830082000281830068586f6b656e50325068736f6d6575726932828300830082000381830068586f6b656e50325068736f6d657572693318678301830082000481830068586f6b656e50325068736f6d6575726934186840420f000000000017a914a9974100aeee974a20cda9a2f545704a0ab54fdc87400d03000000000017a9147d13547544ecc1f28eda0c0766ef4eb214de104587400d03000000000017a9147d13547544ecc1f28eda0c0766ef4eb214de104587400d03000000000017a9147d13547544ecc1f28eda0c0766ef4eb214de104587400d03000000000017a9147d13547544ecc1f28eda0c0766ef4eb214de10458700000000"))]))


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
    processReqResp(sock, x10)
    processReqResp(sock, x11)
    processReqResp(sock, x12)

    exit()
