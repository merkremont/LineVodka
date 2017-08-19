# -*- coding: utf-8 -*-
from .LineClient import LineClient
from types import *
from ..LineThrift.ttypes import OpType
from .LineServer import url

try:
    from thrift.protocol import fastbinary
except:
    fastbinary = None

class LineTracer(object):
    OpInterrupt = {}
    client = None

    def __init__(self, client):
        if type(client) is not LineClient:
            raise Exception(
                "You need to set LineClient instance to initialize LineTracer")

        self.client = client
        self.client.endPoint(url.LINE_POLL_QUERY_PATH_FIR)

    def addOpInterruptWithDict(self, OpInterruptDict):
        """To add Operation with Callback function {Optype.NOTIFIED_INTO_GROUP: func}"""
        self.OpInterrupt.update(OpInterruptDict)

    def addOpInterrupt(self, OperationType, DisposeFunc):
        self.OpInterrupt[OperationType] = DisposeFunc

    def execute(self):
        try:
            operations = self.client.fetchOperation(self.client.revision, 1)
        except EOFError:
            return
        except KeyboardInterrupt:
            exit()
        except:
            return

        for op in operations:
            if op.type in self.OpInterrupt.keys():
                self.OpInterrupt[op.type](op)

            self.client.revision = max(op.revision, self.client.revision)
