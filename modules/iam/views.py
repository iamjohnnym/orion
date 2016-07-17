#!/usr/bin/env python

from botocore.exceptions import ClientError
from libs.connections import AWSConnections
import hashlib
import datetime
import random
import boto3
import argparse
import json
import csv
import os


class Iam(AWSConnections):
    def __init__(self, **kwargs):
        self.args = kwargs
        self.args['aws_asset'] = 'iam'
        self.args['resource'] = 'client'
        self.valid_keys = ['aws_account', 'username', 'password',
                'AccessKeyId', 'SecretAccessKey', 'groupname']
        self.loadClient()

    def loadClient(self):
        self.client = self.assumeAccount()

    def addUser(self, **kwargs):
        password = "{0}##".format(self.generatePassword())
        try:
            self.client.create_user(UserName=kwargs['username'])
            self.client.create_login_profile(
                    UserName=kwargs['username'],
                    Password=password,
                    PasswordResetRequired=True
                    )

            kwargs['password'] = password
            if kwargs.has_key('groupname') and kwargs['groupname']:
                self.addUserToGroup(
                        **kwargs
                        )
            if kwargs.has_key('set_key') and kwargs['set_key']:
                response = self.createAccessKeys(
                        username=kwargs['username']
                        )
                kwargs['AccessKeyId'] = response['AccessKey']['AccessKeyId']
                kwargs['SecretAccessKey'] = response['AccessKey']['SecretAccessKey']
            kwargs.pop('set_key')
            self.addUserData(**kwargs)
            print "CREATED: User {0} has been created.".format(kwargs['username'])
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print "SKIPPING: User {0} already exists.".format(kwargs['username'])

    def generatePassword(self):
        random.seed(random.randint(1,2000));
        password = hashlib.sha224(
                str(datetime.datetime.now())+str(random.random())
                ).hexdigest()[:16]
        return password

    def addUserData(self, **kwargs):
        try:
            self.user_list.append(kwargs)
        except AttributeError:
            self.user_list = []
            self.user_list.append(kwargs)

    def addUserToGroup(self, **kwargs):
        self.client.add_user_to_group(
                UserName=kwargs['username'],
                GroupName=kwargs['groupname']
                )

    def createAccessKeys(self, username):
        response = self.client.create_access_key(
                UserName=username
                )
        return response

    def getFilePath(self):
        home = os.path.expanduser('~')
        directory = '{0}/Documents'.format(home)
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = '{0}/credentials-{1}.csv'.format(
                directory,
                self.args['aws_account']
                )
        return filepath

    def getValidValues(self):
        users = []
        for user in self.user_list:
            user_data = {}
            for key in self.valid_keys:
                user_data[key] = user.get(key) or 'N/A'
            users.append(user_data)
        return users

    def createCsv(self):
        try:
            with open(self.getFilePath(), 'w') as output:
                writer = csv.DictWriter(output, self.valid_keys)
                writer.writeheader()
                writer.writerows(self.getValidValues())
        except AttributeError as e:
            print e


    def openFile(self, file_name):
        with open(file_name) as user_list:
            users = [line.rstrip('\n') for line in user_list]
        return users

    def run(self):
        if self.args['file_name']:
            users = self.openFile(self.args['file_name'])
            self.args.pop('file_name')
            for user in users:
                self.args['username'] = user
        else:
            self.args.pop('file_name')
        self.addUser(
                **self.args
                )
        self.createCsv()

