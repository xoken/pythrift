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
import yaml
import binascii


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


def sendRequest(s, payload):
    length = len(payload)
    lenPrefix = length.to_bytes(2, 'big')
    full = lenPrefix + payload
    s.sendall(lenPrefix)
    s.sendall(payload)


def recvResponse(s):
    prefix = s.recv(2)
    leng = int.from_bytes(prefix, byteorder='big')
    raw = s.recv(leng)
    data = loads(raw)
    print('Received', data)


def client(host, port):
    print('Starting...')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    return s


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
                                    '7d3eb236b526bd681b7fc499d657d237b4d3bc21ef25b37fc1c70822849f1243'
                                    )]))

    x5 = dumps((0, 1, '[TXID]->[TX]', [(5,
                                        ['6c828920ea3a968f0c3c4a8f14d70b696e0440d8e4e1d019cced1ba2cc63cd51',
                                         '097cf9d4ec10711e809f316b7738bbbff94efe32ea2cd55e57ddf5840f828741'
                                         ])]))

    x6 = dumps((0, 1, 'ADDR->[OUTPUT]', [(6,
                                          '13n561iVozTtMXJzAJNA5TQsnTboRvpxae')]))

    x7 = dumps((0, 1, '[ADDR]->[OUTPUT]', [(7,
                                            ['1P8Jd8qQM7y45iXLM1eiXCCmGRhCPjykZB',
                                             '16qgC3hzi38xo1vn2gGsNVwWaW1sEH3h9R'])]))

    x8 = dumps((0, 1, 'TXID->[MNODE]', [(8,
                                         '571c7508413415debe4ba146a2ed141e4d4204d0743169ab3366b1f1e1960a5d'
                                         )]))

    x9 = dumps((0, 1, 'NAME->[OUTPOINT]', [(9,
                                            '[h', True
                                            )]))

    c = Bitcoin()
    priv = sha256('allegory allpay test dummy seed')
    pub = c.privtopub(priv)
    addr = c.pubtoaddr(pub)

###############

    inputs = \
        [{'output': '6c828920ea3a968f0c3c4a8f14d70b696e0440d8e4e1d019cced1ba2cc63cd51:0', 'value': 1000000},
         {'output': '51ce9804e1a4fd3067416eb5052b9930fed7fdd9857067b47d935d69f41faa38:0', 'value': 1000000}]
    outs = [{'value': 1000000,
             'address': '2N8hwP1WmJrFF5QWABn38y63uYLhnJYJYTF'},
            {'value': 250000,
             'address': 'mrvHv6ggk5gFMatuJtBKAzktTU1N3MYdu2'},
            {'value': 250000,
             'address': 'mrvHv6ggk5gFMatuJtBKAzktTU1N3MYdu2'},
            {'value': 250000,
             'address': 'mrvHv6ggk5gFMatuJtBKAzktTU1N3MYdu2'},
            {'value': 250000,
             'address': 'mrvHv6ggk5gFMatuJtBKAzktTU1N3MYdu2'}]

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
    print(tx)
    txs1 = c.sign(tx, 0, priv)
    txs2 = c.sign(txs1, 1, priv)
    print(txs2)
    txser = serialize(txs2)
    print(txser)
    print(txhash(txser))
    # save it for later use
    firstTxHash = txhash(txser)
    x10 = dumps((0, 1, 'RELAY_TX', [(10, bytes.fromhex(txser))]))

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
    x11 = dumps((0, 1, 'RELAY_TX', [(10, bytes.fromhex(txser))]))

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
    x12 = dumps((0, 1, 'RELAY_TX', [(10, bytes.fromhex(txser))]))
    #

    #

    # x10 = dumps((0, 1, 'RELAY_TX', [(9, bytes.fromhex(''))]))

    # ins = [{'output': u'97f7c7d8ac85e40c255f8a763b6cd9a68f3a94d2e93e8bfa08f977b92e55465e:0', 'value': 50000, 'address': u'1CQLd3bhw4EzaURHbKCwM5YZbUQfA4ReY6'}, {
    #    'output': u'4cc806bb04f730c445c60b3e0f4f44b54769a1c196ca37d8d4002135e4abd171:1', 'value': 50000, 'address': u'1CQLd3bhw4EzaURHbKCwM5YZbUQfA4ReY6'}]
    # outs = [{'value': 3000, 'address': '16iw1MQ1sy1DtRPYw3ao1bCamoyBJtRB4t'}]

    # sendRequest(sock, x2)
    # sendRequest(sock, x3)
    # sendRequest(sock, x4)
    # sendRequest(sock, x5)
    # sendRequest(sock, x6)
    # sendRequest(sock, x7)
    # sendRequest(sock, x8)
    # sendRequest(sock, x9)

    # sendRequest(sock, x1)
    # recvResponse(sock)
    # sendRequest(sock, x10)
    # recvResponse(sock)
    # print("***************************")
    # sendRequest(sock, x11)
    # recvResponse(sock)
    print("***************************")
    sendRequest(sock, x9)
    recvResponse(sock)
    # recvResponse(sock)
    # recvResponse(sock)
    # recvResponse(sock)
    # recvResponse(sock)
    # recvResponse(sock)
    # recvResponse(sock)
    # recvResponse(sock)
    # recvResponse(sock)

    time.sleep(120)
