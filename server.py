#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#
import json
import glob
import sys
sys.path.append('gen-py')
#sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])


#from shared.ttypes import SharedStruct

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from arivi import AriviNetworkService
from arivi.ttypes import *
from thrift import Thrift
#from thrift.transport import TSocket
#from thrift.transport import TTransport
#from thrift.protocol import TBinaryProtocol

class AriviNetworkServiceHandler:
    def __init__(self):
        self.log = {}

    def ping(self):
        print('ping()')


    def sendRequest(self, logid, msg):
        print('sendRequest(%d, %s)' % (logid, msg))
        xx = json.loads(msg)
        print (xx)
        print("---")
        
        val = "dummy-placeholder-response"
        
        #log = SharedStruct()
        #log.key = logid
        #log.value = '%d' % (val)
        #self.log[logid] = log

        return val



if __name__ == '__main__':
    if len(sys.argv) == 1:
        print ("Provide a Thrift Server listen port as argument")
        exit(0)
    handler = AriviNetworkServiceHandler()
    processor = AriviNetworkService.Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=sys.argv[1])
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    # server = TServer.TThreadedServer(
    #     processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)

    print('Starting the server...')
    server.serve()
    print('done.')
