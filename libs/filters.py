#!/usr/bin/env python

class AwsFilters(object):
    def isValidTag(self, metadata, key, value):
        print self.getTag(metadata, key)

    def isTagValue(self, metadata, key, value):
        tag = self.getTag(metadata, key)
        if tag and tag.has_key('Value'):
            if value == tag['Value']:
                return True
            return False

    def isTagKey(self, metadata, key):
        if key:
            if self.getTag(metadata, key): return True; return False

    def getTags(self, metadata):
        tags = []
        if metadata.has_key('Tags'):
            for tag in metadata['Tags']:
                if tag:
                    tags.append(tag)
        return tags

    def getTag(self, metadata, get_tag):
        for tag in self.getTags(metadata):
            if get_tag in tag.itervalues():
                if tag:
                    return tag

    def getTagValue(self, tag):
        return tag['Value']

    def getNameTag(self, instance):
        if not self.isTagKey(instance, 'Name'):
            value = 'Unnamed'
        if self.isTagKey(instance, 'Name'):
            if self.isTagValue(instance, 'Name', ""):
                value = 'Unnamed'
            else:
                value = self.getTag(instance, 'Name')['Value']
        return value

    def getTenancy(self, instance):
        return instance['Placement']['Tenancy']

    def getAvailabilityZone(self, instance):
        return instance['Placement']['AvailabilityZone']

    def getSecurityGroups(self, instance):
        return self.createList(instance, 'SecurityGroups', 'GroupId')

    def getBlockDeviceMappings(self, instance):
        return self.createList(instance, 'BlockDeviceMappings', 'DeviceName')

    def getOutputForList(self, key, items):
        if 'json' not in self.args['output']:
            return self.convertToComma(items)
        return items

    def getState(self, instance):
        return instance['State']['Name']

    def convertToComma(self, items):
        comma_value = ','.join(items)
        return comma_value

    def createList(self, instance, primary_key, secondary_key):
        items = []
        for item in instance[primary_key]:
            items.append(item[secondary_key])
        return items

