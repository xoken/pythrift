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
import hashlib
import time
import binascii
    
max_nonce = 100000    

def dsha(s):
    s_bytes = bytes.fromhex(s)
    hashed = hashlib.sha256(hashlib.sha256(s_bytes).digest()).digest()
    return bytes.hex(hashed)
    
def merkle_root_from_merkle_proof(coinbase_hash, merkle_proof):
    merkleRootBytes = coinbase_hash
    print('Merkle Root Bytes Init: ',merkleRootBytes)
    for mp in merkle_proof:
        merkleRootBytes = dsha(merkleRootBytes + invert_endianness(mp))
        print('Merkle Root Bytes: ',merkleRootBytes, "; MerkleProof ",mp)
    print(merkleRootBytes)
    return invert_endianness(merkleRootBytes)

def getTarget(bits):
    print(type(bits))
    ll = int(bits[2:4],16)
    vv = int(bits[4:],16)
    return vv * 2 ** (8 * (ll - 3))

def hexify(value, type):
    return binascii.hexlify(struct.Struct(type).pack(value))

def get_block_header(ver,merkle_root, previous_hash, timestamp, bits, nonce):
    version=hexify(ver, '<L')
    previous_hash=binascii.hexlify(binascii.unhexlify(previous_hash)[::-1])
    hash_merkle_root=binascii.hexlify(binascii.unhexlify(merkle_root)[::-1])
    timestamp=hexify(timestamp, '<L')
    bits=hexify(bits, '<L')
    if nonce <= 0:
    	header_hex=b''.join([version,previous_hash,hash_merkle_root,timestamp,bits])
    else:
    	nonce=hexify(nonce, '<L')
    	header_hex=b''.join([version,previous_hash,hash_merkle_root,timestamp,bits,nonce])
    print(header_hex)
    header_bin = header_hex.decode()
    return header_bin

def proof_of_work(header, difficulty_bits):
    target = getTarget(difficulty_bits)
    print(target)
    for nonce in range(max_nonce):
        hash_result = invert_endianness(dsha(header + hexint(nonce)))
        if int(hash_result, 16) < target:
            print("Success with nonce {}".format(nonce))
            print("Hash is {}".format(hash_result))
            return (hash_result,nonce)
    print("Failed to find nonce")
    return nonce

def processReqResp(s, payload):
    sendRequest(s, payload)
    print("send request:", payload)
    print("\n-----------------------------------------")
    x = recvResponse(s)
    print("-----------------------------------------\n")
    return x

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
    wrappedSocket = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS)
    wrappedSocket.connect((hostname, int(port)))
    return wrappedSocket

def hexint(val):
    x = hex(int(val))[2:]
    if len(x) % 2 == 1:
    	x = '0' + x
    x = ('0' * (8 - len(x[:8]))) + x
    return str(invert_endianness(x))
    
def invert_endianness(x):
    if len(x) <= 2:
    	return x
    else:
    	return invert_endianness(x[2:]) + x[:2]

# start
# command line args for host, port
def main():
    cbase = False

    if len(sys.argv) < 3:
        print('Invalid args, need: <hostname> <port> <optional | provide_coinbase_tx>')
        exit(0)
    elif len(sys.argv) >= 4:
        cbase_str = sys.argv[3].lower()
        if cbase_str == "true":
            cbase = True
    else:
        print("provide_coinbase_tx not provided | Using default value False")

    sock = client(sys.argv[1], sys.argv[2])

    print("SENDING GMC COMMAND")
    xgmc = json.dumps({"id":  0, "jsonrpc" : "2.0", "method": 'GET_MINING_CANDIDATE', "params" : { "provide_coinbase_tx" : cbase } }).encode('utf-8')

    resjson = processReqResp(sock, xgmc)
    try:
    	res = json.loads(resjson)['result']
    	mp = res['merkleProof']
    	prevhash = res['prevhash'] #H
    	btime = res['time'] #H
    	time_hex = hexify(btime,'<L')
    	uuid = res['id'] #SMC
    	nbits = res['nBits']
    	nbits_hex = hexify(nbits,'<L') #H

    	version = 536870912
    	version_hex = hexify(version,'<L')
    
    	cbase = res['coinbase']
    	merkleRoot = merkle_root_from_merkle_proof(dsha(cbase),mp)
    	height = res['height']
    	num_tx = res['num_tx']
    	phh=get_block_header(version,merkleRoot,prevhash,res['time'],res['nBits'],-1)
    	(hashres,nonce_int) = proof_of_work(phh,hex(res['nBits']))

    	xsmc = json.dumps({"id":  0, "jsonrpc" : "2.0", "method": 'SUBMIT_MINING_SOLUTION', "params" : { 'id' : uuid, 'nonce' : nonce_int, 'version' : version } }).encode('utf-8')
    	resjson1 = processReqResp(sock, xsmc)
    	print("Done all APIs, keeping connection open for 5 secs.")
    	time.sleep(5)
    	print("Bye.")
    except:
    	res = json.loads(resjson)['result']
    	print("Code: {}\nMessage: {}".format(res['code'],res['message']))    	

main()

