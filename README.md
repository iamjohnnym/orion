# Orion CommandLine Tool

================================================

## Overview

A commandline tool to wrap AWS API calls to fit and format to our
needs and standards. This tool utilizes the ~/.aws/credentials file so
ensure you're utilizing your primary account credentials since most interactions
require assume role capabilities via STS.


## Capabilities

## Installation

### Prerequisits

- boto3
- git


### Install

```
git clone https://github.com/iamjohnnym/orion.git ~/.orion
```

So that the binary is in your listed programs, we need to add the following to `~/.bash_profile`
or `~/.profile`.

```
if [ -d "${HOME}/.orion" ] ; then
    PATH="${HOME}/.orion:${PATH}"
fi
```

Once that's in there, we need to source the profile so that it picks up the new ${PATH}

```
source ~/.bash_profile
# or via another method
. ~/.profile
```


## Structure

```
├── README.md
├── defaults.json
├── orion
├── libs
│   ├── __init__.py
│   ├── cli.py
│   └── connections.py
└── modules
    ├── __init__.py
    ├── aws
    │   ├── __init__.py
    │   ├── arguments.json
    │   └── views.py
    ├── cft
    │   ├── __init__.py
    │   ├── arguments.json
    │   └── views.py
    ├── ec2
    │   ├── __init__.py
    │   ├── arguments.json
    │   └── views.py
    ├── iam
    │   ├── README.md
    │   ├── __init__.py
    │   ├── arguments.json
    │   └── views.py
    ├── snapshots
    │   ├── README.md
    │   ├── __init__.py
    │   ├── arguments.json
    │   └── views.py
    └── update
        ├── README.md
        ├── __init__.py
        ├── arguments.json
        └── views.py

8 directories, 28 files
```

# Development
=============

## Acceptable Key's for Arguments json

With the exemption of `long` and `short`, the following keys can be used within the arguments.

| Name | Description |
| ---- | ----------- |
| action | The basic type of action to be taken when this argument is encountered at the command line. |
| nargs | The number of command-line arguments that should be consumed. |
| const | A constant value required by some action and nargs selections. |
| default | The value produced if the argument is absent from the command line. |
| type | The type to which the command-line argument should be converted. |
| choices | A container of the allowable values for the argument. |
| required | Whether or not the command-line option may be omitted (optionals only). |
| help | A brief description of what the argument does. |
| metavar | A name for the argument in usage messages. |
| dest | The name of the attribute to be added to the object returned by parse_args(). |

=============================

## AWS Example Module

There are some requirements for creating modules that work with this tool.  This is required for the 'assume_role' or 'sts' method.  The following args must be present:

- aws-account
- role
- role-name
- region

The rest of the arguments here are for the purpose this exact AWS module.

### Example Arguments

```
$ cat files/aws.json
[
  {
    "long": "--aws-account",
    "short": "-a",
    "help": "AWS Account Number",
    "required": "True"
    },{
    "long": "--role",
    "short": "-r",
    "help": "Role Name, used for STS",
    "default": "AssumeRole"
    },{
    "long": "--role-name",
    "short": "-R",
    "help": "Role Name",
    "default": "OrionCommandLine"
    },{
    "long": "--region",
    "short": "-l",
    "help": "Region",
    "choices": ["us-east-1","us-east-2","eu-west-2"],
    "default": "us-east-1"
    },{
    "long": "--method",
    "short": "-m",
    "help": "AWS Boto3 Method to Call"
    },{
    "long": "--method-args",
    "short": "-M",
    "help": "Boto3 **kwargs to pass to method"
    },{
    "long": "--pprint",
    "short": "-p",
    "help": "Pretty Print Returned Data",
    "action": "store_true"
    }
  ]
```


### Example Class Library

```
$ cat libs/aws.py
#!/usr/bin/env python

from botocore.exceptions import ClientError
from libs.connections import AWSConnections
import json
import pprint

class Aws(AWSConnections):
    def __init__(self, **kwargs):
        self.args = kwargs
        self.args['aws_asset'] = 'ec2'
        self.args['resource'] = 'client'

    def loadClient(self):
        self.client = self.assumeAccount()

    def run(self):
        self.loadClient()
        method = getattr(self.client, self.args['method'])
        method_args = json.loads(self.args['method_args'].replace("'", "\""))
        if self.args['pprint']:
            pprint.pprint(method(**method_args))
        print method(**method_args)
```

### Usage

#### Help

```
$ orion aws -h
usage: orion aws [-h] --aws-account AWS_ACCOUNT [--role ROLE]
                  [--role-name ROLE_NAME]
                  [--region {us-east-1,us-east-2,eu-west-2}] [--method METHOD]
                  [--method-args METHOD_ARGS] [--pprint]

optional arguments:
  -h, --help            show this help message and exit
  --aws-account AWS_ACCOUNT, -a AWS_ACCOUNT
                        AWS Account Number
  --role ROLE, -r ROLE  Role Name, used for STS
  --role-name ROLE_NAME, -R ROLE_NAME
                        Role Name
  --region {us-east-1,us-east-2,eu-west-2}, -l {us-east-1,us-east-2,eu-west-2}
                        Region
  --method METHOD, -m METHOD
                        AWS Boto3 Method to Call
  --method-args METHOD_ARGS, -M METHOD_ARGS
                        Boto3 **kwargs to pass to method
  --pprint, -p          Pretty Print Returned Data
```


#### Command to Test in against Orion's account

```
orion aws -a ${ASSUME_ACCOUNT_NUMBER} --method describe_instances -M "{'MaxResults':5,'Filters':[{'Name':'vpc-id','Values': [${VPC_ID}]}]}"

orion aws -a ${ASSUME_ACCOUNT_NUMBER} --method describe_instances

orion aws -a ${ASSUME_ACCOUNT_NUMBER} --method create_user -M "{'UserName':'foobar'}"
```


## Bugs
