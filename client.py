import sys
import glob
sys.path.append('gen-py')
#sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])

from arivi import AriviNetworkService
from arivi.ttypes import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def client(port, cmd):
    # Make socket
    print ("Starting...")
    transport = TSocket.TSocket('localhost', port)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = AriviNetworkService.Client(protocol)

    # Connect!
    transport.open()

    retval = client.ping()
    print('ping status: ' + str(retval))

    if cmd == "rpc":
        msg = '{"jsonrpc": "2.0", "method": "get_block_headers", "params": {"start_height": 20000, "count": 10}, "id": 1}'
        print( '%s' % msg)
        resp = client.sendRequest(1, msg)
        print('%s' % resp)
        
        #try:
            #quotient = client.calculate(1, msg)
            #print('Whoa? You know how to divide by zero?')
            #print('FYI the answer is %d' % quotient)
        #except InvalidOperation as e:
            #print('InvalidOperation: %r' % e)

        msg = '{"jsonrpc": "2.0", "method": "get_block_header", "params": {"height": -1}, "id": 1}'

        resp = client.sendRequest(1, msg)
        print('%s' % resp)

    elif cmd == "sub":
        topic = 'HELLO'

        resp = client.subscribe( topic)
        print('%s' % resp)
    
    elif cmd == "pub":
        topic = 'HELLO'

        resp = client.publish( topic, "hello-world-message")
        print('%s' % resp)
        
    #Close!
    transport.close()



if len(sys.argv) < 3:
        print ("Provide Thrift Server (on localhost) port to connect.")
        exit(0)
        
client(sys.argv[1], sys.argv[2])
