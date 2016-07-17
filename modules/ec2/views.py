#!/usr/bin/env python


from libs.connections import AWSConnections


class Ec2(AWSConnections):
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
        for item in self.describeInstances()['Reservations']:
            for instance in item['Instances']:
                idict = {}
                idict['InstanceId'] = instance['InstanceId']
                idict['State'] = instance['State']['Name']
                idict['StateReason'] = instance['StateTransitionReason']
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        idict['Name'] = tag['Value']
                ilist.append(idict)

        return ilist

