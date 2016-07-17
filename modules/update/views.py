#!/usr/bin/env python

import subprocess


class Update(object):
    def __init__(self, **kwargs):
        self.args = kwargs

    def pull(self, branch="master"):
        command = "git fetch"
        self.runCommand(command)
        command = "git checkout {0}".format(branch)
        self.runCommand(command)
        command = "git pull".format(branch)
        self.runCommand(command)

    def runCommand(self, command):
        command = command.split()
        process = subprocess.Popen(command, cwd=self.args['program_path'])
        process.wait()

    def run(self):
        self.pull(
                branch=self.args['branch']
                )


