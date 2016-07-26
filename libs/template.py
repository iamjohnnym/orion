#!/usr/bin/env python

from operator import itemgetter
import datetime
import pprint
import csv
import os
import json as js
import ConfigParser

class Mixins(object):
    @classmethod
    def saveFile(self,args):
        args['path'] = args['path'].rstrip('/')
        if '~' in args['path']:
            # Because python doesn't enjoy the ~ flag, we have to expand
            # that so it creates an absolute path. Keeps
            home = os.path.expanduser('~')
            path = args['path'].replace('~', home).rstrip('/')
            del args['path']
            args['path'] = path
        today = str(datetime.date.today()).replace('-','')
        self.path = '{0}/{1}.{2}.csv'.format(args['path'], args['aws_account'], today)
        inc = 0
        while True:
            if os.path.isfile(self.path):
                if inc == 0:
                    pass
                else:
                    self.path = '{0}/{1}.{2}.{3}.csv'.format(args['path'], args['aws_account'], today, inc)
                inc += 1
            else:
                break
        return self.path

    @classmethod
    def csv(self, args, output):
        """
        Lets be honest, this right here is the sticks. Some god awful code.
        It will be cleaned, sanitized, and better.
        """
        self.path = self.saveFile(args)
        try:
            with open(self.path, 'w') as o:
                writer = csv.DictWriter(o, output[0])
                writer.writeheader()
                writer.writerows(output)
                print "Your file has been saved to: {0}".format(self.path)
        except AttributeError as e:
            print e

    @classmethod
    def json(self, args, output):
        print js.dumps(output)

    @classmethod
    def ini(self, args, output):
        config = ConfigParser.ConfigParser(allow_no_value=True)
        for item in output:
            try:
                config.add_section(item['header'])
                config.set(item['header'], '; {0}'.format(item['name']))
                config.set(item['header'], 'role_arn', item['role_arn'])
                config.set(item['header'], 'region', item['region'])
            except Exception as e:
                print e
            with open(args['save_path'], 'w') as ini:
                config.write(ini)
            print "Your file has been saved to: {0}".format(self.path)


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
