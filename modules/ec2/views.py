#!/usr/bin/env python


from libs.connections import AWSConnections
from libs.template import Mixins


class Ec2(Mixins,AWSConnections):
    def __init__(self, **kwargs):
        self.args = kwargs
        self.args['aws_asset'] = 'ec2'
        self.args['resource'] = 'client'
        self.loadClient()

    def loadClient(self):
        self.client = self.assumeAccount()

    def describeInstances(self):
        ec2 = self.client.describe_instances()
        return ec2

    def printInstances(self, instances):
        for item in instances:
            if item.has_key('Name'):
                print "{0:<20} | {1:<12} | {2} | {3:<30}".format(
                        item['Name'],
                        item['InstanceId'],
                        item['State'],
                        item['StateReason']
                        )
            else:
                print "{0:<20} | {1:<12} | {2} | {3:<30}".format(
                        'Unnamed',
                        item['InstanceId'],
                        item['State'],
                        item['StateReason']
                        )

    def run(self):
        ilist = []
        key_filter = ['InstanceId', 'StateTransitionReason']
        for item in self.describeInstances()['Reservations']:
            for instance in item['Instances']:
                idict = {}
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        idict['Name'] = tag['Value']
                for key in key_filter:
                    if instance[key]:
                        idict[key] = instance[key]
                ilist.append(idict)
        self.table(self.sortList(ilist))

