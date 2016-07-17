#!/usr/bin/env python

import argparse
import json
import os


class CLIArguments(object):
    def __init__(self, program_path):
        self.program_path = program_path
        self.parser = argparse.ArgumentParser()

    def loadFile(self, filename):
        with open(filename) as f:
            try:
                data = json.load(f)
            except:
                data = f.readlines()
        return data

    def getCommand(self):
        self.command = self.args.__dict__['command']
        return self.command

    def getModulePath(self):
        return "modules.{0}.views.{1}".format(
                self.getCommand(),
                self.getCommand().capitalize()
                )

    def createSubArguments(self, filename='modules.json'):
        self.subparser = self.parser.add_subparsers(
                help='Active Modules',
                dest='command'
                )
        for module in self.loadModules():
            file_path = "{0}/modules/{1}/arguments.json".format(
                    self.program_path,
                    module
                    )
            help_info = "{0} module".format(module.capitalize())
            self.module = self.subparser.add_parser(
                    module,
                    help=help_info
                    )
            self.appendSubArguments('defaults')
            self.appendSubArguments(module)

    def appendSubArguments(self, module):
        try:
            if module == 'defaults':
                file_path = "{0}/{1}.json".format(self.program_path,module)
            else:
                file_path = "{0}/modules/{1}/arguments.json".format(self.program_path,module)
            for item in self.loadFile(file_path):
                self.module.add_argument(
                        item.pop('long'),
                        item.pop('short'),
                        **item
                        )
        except Exception as e:
            print e

    def loadArguments(self):
        # create arguments
        self.createSubArguments()
        self.args = self.parser.parse_args()

    def loadModules(self):
        modules = []
        path = "{0}/modules".format(self.program_path)
        for item in os.listdir(path):
            if '.py' not in item:
                modules.append(item)
        return modules

    def run(self):
        self.loadArguments()
