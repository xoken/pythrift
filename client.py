import sys
import glob
import time
import socket
import json 

#global 
msgid = 1

def sendRequest(s, request):
    global msgid
    req =  {} 
    
    req['msgid'] = msgid
    req['mtype'] = 'RPC_REQ'
    params ={}
    params['encReq'] = request
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
        sendRequest (sock , "asdlfwoeurosdjhfljwslfjwelrsdjfowieuosdkjf")
        
    elif cmd == "sub":
        subscribe (sock, "get_block_header")

    elif cmd == "pub":
        publish (sock, "get_block_header", "<dummy body>")
        
    time.sleep(50)

