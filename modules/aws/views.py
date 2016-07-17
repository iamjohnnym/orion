#!/usr/bin/env python

from botocore.exceptions import ClientError
from libs.connections import AWSConnections
import json
import pprint

class Aws(AWSConnections):
    def __init__(self, **kwargs):
        self.args = kwargs
        self.args['resource'] = 'client'

    def loadClient(self):
        self.client = self.assumeAccount()

    def run(self):
        self.loadClient()
        method = getattr(self.client, self.args['method'])
        if self.args['method_args']:
            method_args = json.loads(self.args['method_args'].replace("'", "\""))
            method = method(**method_args)
        else:
            method = method()

        if self.args['pprint']:
            pprint.pprint(method)
        print method
