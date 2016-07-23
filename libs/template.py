#!/usr/bin/env python

from operator import itemgetter
import pprint
import csv
import os
import json as js

class Mixins(object):
    @classmethod
    def csv(self, args, output):
        if '~' in args['path']:
            home = os.path.expanduser('~')
            path = args['path'].replace('~', home)
            del args['path']
            args['path'] = path
        self.path = '{0}/{1}.csv'.format(args['path'], args['aws_account'])
        try:
            with open(self.path, 'w') as o:
                writer = csv.DictWriter(o, output[0])
                writer.writeheader()
                writer.writerows(output)
        except AttributeError as e:
            print e

    @classmethod
    def json(self, args, output):
        print js.dumps(output)

    @classmethod
    def table(self, args, output):
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
                olist.append("{%s:<15}" % key)
                oprint = " | ".join(olist)
            print oprint.format(**output)

    @classmethod
    def pprint(self, args, output):
        print pprint.pprint(output)

    def sortList(self, output):
        return sorted(output, key=itemgetter('Name'))

    def template(self, output):
        method = getattr(Mixins, self.args['output'])
        method(self.args, output)
