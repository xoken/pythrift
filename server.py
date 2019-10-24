import socketserver
import sys
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)


def getResponse(data):
    
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
                conn.sendall(getResponse(data))    

