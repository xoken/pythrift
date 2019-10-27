import socketserver
import sys
import socket
import json
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)


def getResponse(data):
    sdata = data.decode("utf-8") 
    obj = json.loads(sdata)
    msgid = obj['msgid']
    mtype = obj['mtype']
    
    if mtype == "RPC_REQ":
        req['msgid'] = msgid
        req['mtype'] = 'RPC_RESP'
        params ={}
        params['encResp'] = "wue5279wusle2oesliru2"
        req['params'] = params
        msg = json.dumps(req)
        
    elif mtype == "PUB_REQ":
        topic = obj['subject']
        req['msgid'] = msgid
        req['mtype'] = 'PUB_RESP'
        params ={}
        params['subject'] = topic
        params['status'] = "ACK"
        req['params'] = params
        msg = json.dumps(req)
    
    #print (msgid, msg)
    return msg
    
    
if len(sys.argv) == 1:
    print ("Provide Server listen port as argument")
    exit(0)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, int(sys.argv[1])))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                prefix = conn.recv(2)
                leng = int.from_bytes(prefix, byteorder='big')
                data = conn.recv(leng)
                print (data)
                if not data:
                    break
                msg = getResponse(data)
                length = len(msg)
                lenPrefix = length.to_bytes(2, 'big')
                payload = str.encode(msg)
                print (lenPrefix, payload)
                conn.sendall(lenPrefix)
                conn.sendall(payload)
                   

