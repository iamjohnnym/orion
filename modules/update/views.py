#!/usr/bin/env python

import subprocess


class Update(object):
    def __init__(self, **kwargs):
        self.args = kwargs

    def pull(self, branch="master"):
        """
        Update your application to the desired version!

        :PARAM: STRING : branch :: DEFAULT=master : This determines which
                    version of the core framework will be running.
        """
        command = "git fetch"
        self.runCommand(command)
        command = "git checkout {0}".format(branch)
        self.runCommand(command)
        command = "git pull".format(branch)
        self.runCommand(command)

    def runCommand(self, command):
        """
        Exec a shell command via subprocess.Popen

        :PARAM: STRING : command :: Full shell command
        """
        command = command.split()
        process = subprocess.Popen(command, cwd=self.args['program_path'])
        process.wait()

    def run(self):
        """
        Since this module is pretty simple at the moment, we're just doing a
        self.pull()
        """
        self.pull(
                branch=self.args['branch']
                )


