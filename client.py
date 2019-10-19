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


def main():
    # Make socket
    print ("Starting...")
    transport = TSocket.TSocket('localhost', 9090)

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


    msg = 'wonderful'

    resp = client.sendRequest(1, msg)
    print('%s' % resp)
    
    #try:
        #quotient = client.calculate(1, msg)
        #print('Whoa? You know how to divide by zero?')
        #print('FYI the answer is %d' % quotient)
    #except InvalidOperation as e:
        #print('InvalidOperation: %r' % e)

    msg = ' hello'

    resp = client.sendRequest(1, msg)
    print('%s' % resp)

    #log = client.getStruct(1)
    #print('Check log: %s' % log.value)

    #Close!
    transport.close()

main()
