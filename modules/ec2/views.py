#!/usr/bin/env python


from libs.connections import AWSConnections
from libs.template import Mixins
from libs.filters import AwsFilters


filters = {
        "build": ['InstanceType','VpcId','PrivateIpAddress','PublicIpAddress', 'AvailabilityZone','SubnetId','Tenancy','SecurityGroups','BlockDeviceMappings'],
        "ips": ['PrivateIpAddress','AvailabilityZone', 'State','PublicIpAddress'],
        "test": ['Tenancy','SecurityGroups','BlockDeviceMappings','AvailabilityZone']
        }


class Ec2(Mixins,AWSConnections,AwsFilters):
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

    def getFilter(self, filter_name):
        self.args['program_path']
        return loadFile("{0}/modules/ec2/filter_groups/{1}".filter(
            self.args['program_path'],
            filter_name
            ))

    def run(self):
        """

        """
        ilist = []
        key_filter = filters[self.args['filter_group']]
        for item in self.client.describe_instances()['Reservations']:
            for instance in item['Instances']:
                data = {}
                # Get the name tag from the AwsFilters object.
                data['Name'] = self.getNameTag(instance)

                for key in key_filter:
                    try:
                        method_to_use = 'get{0}'.format(key)
                        if key in ['AvailabilityZone','Tenancy','State']:
                            method = getattr(self, method_to_use)
                            data[key] = method(instance)
                        elif key in ['SecurityGroups','BlockDeviceMappings']:
                            method = getattr(self, method_to_use)
                            data[key] = self.getOutputForList(key, method(instance))
                        else:
                            if instance[key]:
                                data[key] = instance[key]
                    except Exception as e:
                        print e
                        data[key] = 'N/A'
                ilist.append(data)
        self.template(self.sortList(ilist))

