import sys
import glob
import time
import socket
import json 
import base64
import zlib
#global 
msgid = 1

def sendRequest(s, request):
    global msgid
    req =  {} 
    
    req['msgid'] = msgid
    req['mtype'] = 'RPC_REQ'
    params ={}
    gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
    
    gzx = gzip_compress.compress(request.encode('utf-8')) + gzip_compress.flush()
    params['encReq'] = base64.b64encode(gzx).decode('utf-8')
 
    req['params'] = params
    msg = json.dumps(req)
    print(msg)
    msgid = msgid + 1
    
    length = len(msg)
    lenPrefix = length.to_bytes(2, 'big')
    print (length, lenPrefix)
    
    payload = str.encode(msg)
    full = lenPrefix + payload
    s.sendall(lenPrefix)
    s.sendall(payload)
    prefix = s.recv(2)
    leng = int.from_bytes(prefix, byteorder='big')
    raw = s.recv(leng)
    data = raw.decode("utf-8")
    print('Received', data )
    resp = json.loads(data)
    body = resp['params']['encResp'] 
    if body == '__EXCEPTION__NO_PEERS':
        print("No peers yet. Will retry.")
    else:
        print ("Body: ", body)
        jsp = zlib.decompress(base64.b64decode(body), 16 + zlib.MAX_WBITS).decode('utf-8')
        print ("Decoded Payload: ", jsp)
    

    

def subscribe(s, topic):
    global msgid
    req =  {} 

    
    req['msgid'] = msgid
    req['mtype'] = 'SUB_REQ'
    params ={}
    params['subject'] = topic
    req['params'] = params
    msg = json.dumps(req)
    print(msg)
    msgid = msgid + 1
    
    length = len(msg)
    lenPrefix = length.to_bytes(2, 'big')
    print (length, lenPrefix)
    
    payload = str.encode(msg)
    full = lenPrefix + payload
    s.sendall(lenPrefix)
    s.sendall(payload)
    prefix = s.recv(2)
    leng = int.from_bytes(prefix, byteorder='big')
    data = s.recv(leng)
    print('Received', data.decode("utf-8") )


def publish(s, topic, body):
    global msgid
    req =  {} 

    
    req['msgid'] = msgid
    req['mtype'] = 'PUB_REQ'
    params ={}
    params['subject'] = topic
    params['body'] = body
    req['params'] = params
    msg = json.dumps(req)
    print(msg)
    msgid = msgid + 1
    
    length = len(msg)
    lenPrefix = length.to_bytes(2, 'big')
    print (length, lenPrefix)
    
    payload = str.encode(msg)
    full = lenPrefix + payload
    s.sendall(lenPrefix)
    s.sendall(payload)
    prefix = s.recv(2)
    leng = int.from_bytes(prefix, byteorder='big')
    data = s.recv(leng)
    print('Received', data.decode("utf-8") )
    
    
def client(port):
    # Make socket
    print ("Starting...")
    #transport = TSocket.TSocket('localhost', port)

    #Buffering is critical. Raw sockets are very slow
    #transport = TTransport.TBufferedTransport(transport)

    #Wrap in a protocol
    #protocol = TBinaryProtocol.TBinaryProtocol(transport)

    #Create a client to use the protocol encoder
    #client = AriviNetworkService.Client(protocol)

    # Connect!
    #transport.open()

    #'{"msgid": 123, "mtype": "RPC", "encReq": "CiA8bnMwOlJlcG9ydCB4bWxuczpuczA9XCJodHRwOi"}'
    #'{"msgid": 456, "mtype": "SUB", "subject": "hello"}'
    #'{"msgid": 789, "mtype": "PUB", "subject": "hello" "body": "PD94bWwgdmVyc2lvbj1cIjEuMFwiIGVuY29kaW5n"}'
    
    host = "127.0.0.1"
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    return s
    

    #retval = client.ping()
    #print('ping status: ' + str(retval))

    #if cmd == "rpc":
        #msg = '{"jsonrpc": "2.0", "method": "get_block_headers", "params": {"start_height": 20000, "count": 10}, "id": 1}'
        #print( '%s' % msg)
        #resp = client.sendRequest(1, msg)
        #print('%s' % resp)
        
        #try:
            #quotient = client.calculate(1, msg)
            #print('Whoa? You know how to divide by zero?')
            #print('FYI the answer is %d' % quotient)
        #except InvalidOperation as e:
            #print('InvalidOperation: %r' % e)

        #msg = '{"jsonrpc": "2.0", "method": "get_block_header", "params": {"height": -1}, "id": 1}'

        #resp = client.sendRequest(1, msg)
        #print('%s' % resp)

    #elif cmd == "sub":
        #topic = 'HELLO'

        #resp = client.subscribe( topic)
        #print('%s' % resp)
    
    #elif cmd == "pub":
        #topic = 'HELLO'

        #resp = client.publish( topic, "hello-world-message")
        #print('%s' % resp)
        
    #Close!
    #transport.close()



if len(sys.argv) < 3:
        print ("Provide Server (on localhost) port to connect.")
        exit(0)
        
sock = client(sys.argv[1])
cmd =  sys.argv[2]
while True:
    if cmd == "rpc":
        r1 = '{"method": "get_block_height", "height": 7000001235 }'
        r2 = '{"method": "get_blocks_heights", "heights": [15000,15001,15002] }'
        
        sendRequest (sock , r1)
        
    elif cmd == "sub":
        subscribe (sock, "get_block_header")

    elif cmd == "pub":
        publish (sock, "get_block_header", "<dummy body>")
        
    time.sleep(10)

