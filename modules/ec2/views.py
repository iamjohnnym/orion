#!/usr/bin/env python


from libs.connections import AWSConnections
from libs.template import Mixins


filters = {
        "build": ['InstanceType','VpcId','PrivateIpAddress','PublicIpAddress', 'AvailabilityZone','SubnetId','Tenancy','SecurityGroups']
        }


class Ec2(Mixins,AWSConnections):
    def __init__(self, **kwargs):
        self.args = kwargs
        self.args['aws_asset'] = 'ec2'
        self.args['resource'] = 'client'
        self.loadClient()

    def loadFile(self, filename):
        with open(filename) as f:
            try:
                data = json.load(f)
            except:
                data = f.readlines()
        return data

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

    def getFilter(self, filter_name):
        self.args['program_path']
        return loadFile("{0}/modules/ec2/filter_groups/{1}".filter(
            self.args['program_path'],
            filter_name
            ))

    def run(self):
        ilist = []
        key_filter = filters[self.args['filter_group']]
        for item in self.describeInstances()['Reservations']:
            for instance in item['Instances']:
                idict = {}
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        idict['Name'] = tag['Value']
                for key in key_filter:
                    try:
                        if key in ['AvailabilityZone','Tenancy']:
                            idict[key] = instance['Placement'][key]
                        elif key == 'SecurityGroups':
                            sg_list = []
                            for sg in instance[key]:
                                sg_list.append(sg['GroupId'])
                            if self.args['output'] == 'csv':
                                sg_string = " \n"
                                idict[key] = sg_string.join(sg_list)
                            else:
                                idict[key] = ','.join(sg_list)
                        else:
                            if instance[key]:
                                idict[key] = instance[key]
                    except Exception as e:
                        idict[key] = 'N/A'
                ilist.append(idict)
        self.template(self.sortList(ilist))

