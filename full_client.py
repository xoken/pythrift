import sys
import glob
import time
import socket


from cbor2 import dumps, loads, CBORTag

#global 
msgId = 1


       
          
def sendRequest(s, payload):
    length = len(payload)
    lenPrefix = length.to_bytes(2, 'big')
    print (length, lenPrefix)
    
    full = lenPrefix + payload
    s.sendall(lenPrefix)
    s.sendall(payload)
    prefix = s.recv(2)
    leng = int.from_bytes(prefix, byteorder='big')
    raw = s.recv(leng)
    data = loads(raw)
    print('Received', data )

    

    

def subscribe(s, topic):
    global msgId
    req =  {} 

    
    req['msgId'] = msgId
    req['msgType'] = 'SUB_REQ'
    payload ={}
    payload['subject'] = topic
    req['payload'] = payload
    msg = json.dumps(req)
    print(msg)
    msgId = msgId + 1
    
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
    global msgId
    req =  {} 

    
    req['msgId'] = msgId
    req['msgType'] = 'PUB_REQ'
    payload ={}
    payload['subject'] = topic
    payload['body'] = body
    req['payload'] = payload
    msg = json.dumps(req)
    print(msg)
    msgId = msgId + 1
    
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
    host = "127.0.0.1"
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    return s
    


               

if len(sys.argv) < 3:
        print ("Provide Server (on localhost) port to connect.")
        exit(0)
        
sock = client(sys.argv[1])
cmd =  sys.argv[2]


while True:
    if cmd == "rpc":
        x1 = dumps((0,1,"HEIGHT->BLOCK",[(0,100)])) 
        x2 = dumps((0,1,"[HEIGHT]->[BLOCK]",[(1,[100,101,102])])) 
        x3 = dumps((0,1,"HASH->BLOCK",[(2,"00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee")])) 
        
        sendRequest (sock , x1)
        sendRequest (sock , x2)
        sendRequest (sock , x3)
        
        #sendRequest (sock , r2)
        #sendRequest (sock , r3)
        
    elif cmd == "sub":
        subscribe (sock, "get_block_header")

    elif cmd == "pub":
        publish (sock, "get_block_header", "<dummy body>")
        
    time.sleep(5)

