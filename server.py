import socketserver
import sys
import socket
import json
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)


def getResponse(data):
    sdata = data.decode("utf-8") 
    obj = json.loads(sdata)
    msgid = obj['msgid']
    body = "wue5279wusle2oesliru2"
    msg = '{"msgid": '+ str(msgid) + ', "mtype": "RPC_RESP", "params": { "encResp": "'+ body + '"} }'
    print (msgid, msg)
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
                data = conn.recv(1024)
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
                   

