#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import glob
import time
import socket
import threading
from cryptos import Bitcoin, sha256, deserialize, serialize, txhash
from cbor2 import dumps, loads, CBORTag
import codecs
import binascii
import ssl
import json as JSON


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
    print('Received', raw)
    data = loads(raw)
    print('Received', data)
    return raw

def client(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(100)
    wrappedSocket = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_1)
    wrappedSocket.connect((hostname, int(port)))
    return wrappedSocket


#def client(hostname, port):
    #context = ssl.create_default_context()
    #with socket.create_connection((hostname, port)) as sock:
        #with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            #print(ssock.version())
            #ssock.connect((hostname, int(port)))
            #return ssock



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
                                          '18TLpiL4UFwmQY8nnnjmh2um11dFzZnBd9')]))

    x9 = dumps((0, 1, '[ADDR]->[OUTPUT]', [(9,
                                            ['18TLpiL4UFwmQY8nnnjmh2um11dFzZnBd9',
                                             '16qgC3hzi38xo1vn2gGsNVwWaW1sEH3h9R'])]))

    x10 = dumps((0, 1, 'SCRIPTHASH->[OUTPUT]', [(10,
                                          '8ad0ed1cf403f3d4f589b6b05195d7932425620b0b42e7bfce0295df6f1e3c67')]))

    x11 = dumps((0, 1, '[SCRIPTHASH]->[OUTPUT]', [(11,
                                            ['8ad0ed1cf403f3d4f589b6b05195d7932425620b0b42e7bfce0295df6f1e3c67',
                                             '1fb931ea41f204ce837f63dcffdec09720c8c8d285196050d32fd4e5dc2915be'
                                             ])]))

    x12 = dumps((0, 1, 'TXID->[MNODE]', [(12,
                                         '54c693db802d83596e3a0cdec1f99dc01af246ca51b82adaad2f41e0a8fb2131'
                                         )]))

    x13 = dumps((0, 1, 'NAME->[OUTPOINT]', [(13,
                                            '[h', True
                                            )]))

    c = Bitcoin()
    priv = sha256('allegory allpay test dummy seed')
    pub = c.privtopub(priv)
    addr = c.pubtoaddr(pub)

###############
    inputsD = \
        [(0, 'dee533d8d0ac0b1f0ccb49b80f075fee63802a9fab9114a90e9c5ae866695731', 0)]

    inputs = \
        [{'output': 'e4714990d74d9636c2efdb98a5e7dc7c1c516a43572638641eb67dda9df43015:0', 'value': 1000000},
         {'output': '51ce9804e1a4fd3067416eb5052b9930fed7fdd9857067b47d935d69f41faa38:0', 'value': 1000000}]
    outs = [{'value': 1000000,
             'address': '18TLpiL4UFwmQY8nnnjmh2um11dFzZnBd9'},
            {'value': 5555,
             'address': '1GRVVRz75WfU7htxMWDm9i1tnZP2KFqRzL'}]
    allegory = (0, 1, [],
                (0, (0, 0),
                 (0, (0, 1), [(0, "XokenP2P", "someuri1")]),
                 [(0, (0, 2), [(0, "XokenP2P", "someuri2")])],
                 [(0, (0, (0, 3), [(0, "XokenP2P", "someuri3")]), 90), (1, (0, (0, 4), [(0, "XokenP2P", "someuri4")]), 91)]))

    data = dumps(allegory)
    ss = frame_op_return(data).hex()

    print('hexlified ', str(ss))
    op_return = [{'script': ss, 'value': 0}]
    outs = op_return + outs
    tx = c.mktx(inputs, outs)
    print('\n\nRaw Tx : ', tx)
    x17 = dumps((0, 1, 'PS_ALLEGORY_TX', [(15, inputsD, "", True, ('18TLpiL4UFwmQY8nnnjmh2um11dFzZnBd9', 1000000), ('1GRVVRz75WfU7htxMWDm9i1tnZP2KFqRzL', 5555))]))
    sendRequest(sock, x17)

    txs = recvResponse(sock)
    cbortx = loads(txs)[4][0][1].decode('utf-8')
    jsontx = JSON.loads(cbortx)
    print('\n\nJSON Tx (received): ', jsontx)
    txs2 = c.sign(jsontx, 0, priv)
 
    print('\n\nSigning inupts (own) : ', txs2)
    txser = serialize(txs2)
    print(txser)
    print(txhash(txser))
    # save it for later use
    firstTxHash = txhash(txser)
    x14 = dumps((0, 1, 'RELAY_TX', [(14, bytes.fromhex(txser))]))

###########

    inputs = \
        [{'output': (firstTxHash + ':3'), 'value': 1000000},
         {'output': '51ce9804e1a4fd3067416eb5052b9930fed7fdd9857067b47d935d69f41faa38:0', 'value': 1000000}]
    outs = [{'value': 1000000,
             'address': '2N8hwP1WmJrFF5QWABn38y63uYLhnJYJYTF'},
            {'value': 1000000,
             'address': 'mrvHv6ggk5gFMatuJtBKAzktTU1N3MYdu2'}]

    allegory = (0, 1, [90],
                (1, (0, 0),
                 (0, (0, 1), [(0, "XokenP2P", "someuri000")]),
                 [(0, "Allegory", "standard", (0, "XokenP2P", "uriuriuri"),
                   (0, "addrcommit1234", "utxocommit1234", "signature1234",  8123456))]))

    data = dumps(allegory)
    ss = frame_op_return(data).hex()

    print('hexlified ', str(ss))
    op_return = [{'script': ss, 'value': 0}]
    outs = op_return + outs
    tx = c.mktx(inputs, outs)
    print(tx)
    txs1 = c.sign(tx, 0, priv)
    txs2 = c.sign(txs1, 1, priv)
    print(txs2)
    txser = serialize(txs2)
    print(txser)
    print(txhash(txser))
    secondTxHash = txhash(txser)
    x15 = dumps((0, 1, 'RELAY_TX', [(14, bytes.fromhex(txser))]))

############

    inputs = \
        [{'output': firstTxHash + ':4', 'value': 1000000},
         {'output': '51ce9804e1a4fd3067416eb5052b9930fed7fdd9857067b47d935d69f41faa38:0', 'value': 1000000}]
    outs = [{'value': 1000000,
             'address': '2N8hwP1WmJrFF5QWABn38y63uYLhnJYJYTF'},
            {'value': 200000,
             'address': 'mrvHv6ggk5gFMatuJtBKAzktTU1N3MYdu2'},
            {'value': 200000,
             'address': 'mrvHv6ggk5gFMatuJtBKAzktTU1N3MYdu2'},
            {'value': 200000,
             'address': 'mrvHv6ggk5gFMatuJtBKAzktTU1N3MYdu2'},
            {'value': 200000,
             'address': 'mrvHv6ggk5gFMatuJtBKAzktTU1N3MYdu2'}]

    allegory = (0, 1, [91],
                (0, (0, 0),
                 (0, (0, 1), [(0, "XokenP2P", "someuri1")]),
                 [(0, (0, 2), [(0, "XokenP2P", "someuri2")])],
                 [(0, (0, (0, 3), [(0, "XokenP2P", "someuri3")]), 103), (1, (0, (0, 4), [(0, "XokenP2P", "someuri4")]), 104)]))

    data = dumps(allegory)
    ss = frame_op_return(data).hex()

    print('hexlified ', str(ss))
    op_return = [{'script': ss, 'value': 0}]
    outs = op_return + outs
    tx = c.mktx(inputs, outs)
    print(tx)
    txs1 = c.sign(tx, 0, priv)
    txs2 = c.sign(txs1, 1, priv)
    print(txs2)
    txser = serialize(txs2)
    print(txser)
    print(txhash(txser))
    # save it for later use
    firstTxHash = txhash(txser)
    x16 = dumps((0, 1, 'RELAY_TX', [(14, bytes.fromhex(txser))]))

    # x10 = dumps((0, 1, 'RELAY_TX', [(9, bytes.fromhex(''))]))
    # ins = [{'output': u'97f7c7d8ac85e40c255f8a763b6cd9a68f3a94d2e93e8bfa08f977b92e55465e:0', 'value': 50000, 'address': u'1CQLd3bhw4EzaURHbKCwM5YZbUQfA4ReY6'}, {
    #    'output': u'4cc806bb04f730c445c60b3e0f4f44b54769a1c196ca37d8d4002135e4abd171:1', 'value': 50000, 'address': u'1CQLd3bhw4EzaURHbKCwM5YZbUQfA4ReY6'}]
    # outs = [{'value': 3000, 'address': '16iw1MQ1sy1DtRPYw3ao1bCamoyBJtRB4t'}]

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
    processReqResp(sock, x13)
    processReqResp(sock, x14)
    processReqResp(sock, x15)
    processReqResp(sock, x16)

    exit()
