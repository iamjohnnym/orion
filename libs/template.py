#!/usr/bin/env python

from operator import itemgetter
import pprint
import csv


class Mixins(object):
    def csv(self):
        try:
            with open(self.getFilePath(), 'w') as output:
                writer = csv.DictWriter(output, self.valid_keys)
                writer.writeheader()
                writer.writerows(self.getValidValues())
        except AttributeError as e:
            print e

    def js(self):
        pass

    @classmethod
    def table(self, output):
        olist = []
        olist.append("{Name:<35}")
        oprint = " | ".join(olist)
        if isinstance(output, list):
            for key in output[0].keys():
                if 'Name' not in key:
                    olist.append("{%s:<15}" % key)
                    oprint = " | ".join(olist)
            for row in output:
                print oprint.format(**row)
        else:
            for key in output.keys():
                olist.append("{%s:<18}" % key)
                oprint = " | ".join(olist)
            print oprint.format(**output)

    @classmethod
    def pprint(self, output):
        print pprint.pprint(output)

    def sortList(self, output):
        return sorted(output, key=itemgetter('Name'))

    def template(self, output):
        del output['ResponseMetadata']
        method = getattr(Mixins, self.args['output'])
        for key in output:
            for item in output[key]:
                method(item)
