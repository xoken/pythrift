import sys
import glob
import time
import socket
from json import dumps, loads

#global 
msgid = 1

def sendRequest(s, request):
    global msgid
    msg = '{"msgid": '+ str(msgid) + ', "mtype": "RPC", "params": { "encReq": "'+ request + '"} }'
    msgid = msgid + 1
    
    length = len(msg)
    print (length)
    lenPrefix = length.to_bytes(2, 'big')
    print (lenPrefix)
    
    payload = str.encode(msg)
    full = lenPrefix + payload
    s.sendall(lenPrefix)
    s.sendall(payload)
    data = s.recv(1024)
    print('Received', repr(data))
    
    
def client(port, cmd):
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
        
sock = client(sys.argv[1], sys.argv[2])
while True:
    sendRequest (sock , "asdlfwoeurosdjhfljwslfjwelrsdjfowieuosdkjf")
    time.sleep(5)
