# Orion CommandLine Tool

================================================

## Overview

A commandline tool to wrap AWS API calls to fit and format to our
needs and standards. This tool utilizes the ~/.aws/credentials file so

## Capabilities

- Add new AWS users to assumed accounts
  - Optional API Key generation
  - Random password hashes per user
  - Optional file use to create multiple users at once.


## Command Line

### List Modules

```
$ python orion -h
usage: orion [-h] {iam} ...

positional arguments:
  {iam}  Active Modules
    iam            Module to create new users to AWS

optional arguments:
  -h, --help       show this help message and exit
```

## Structure

```
orion iam -h
usage: orion iam [-h] --aws-account AWS_ACCOUNT [--username USERNAME]
                  [--groupname GROUPNAME] [--set-key] [--file-name FILE_NAME]
                  [--role-name ROLE_NAME]
                  [--region {us-east-1,us-east-2,eu-west-2}] [--role ROLE]

optional arguments:
  -h, --help            show this help message and exit
  --aws-account AWS_ACCOUNT, -a AWS_ACCOUNT
                        AWS Account Number
  --username USERNAME, -u USERNAME
                        AWS UserName
  --groupname GROUPNAME, -n GROUPNAME
                        AWS GroupName
  --set-key, -k         AWS GroupName
  --file-name FILE_NAME, -f FILE_NAME
                        File with list of users to create
  --role-name ROLE_NAME, -G ROLE_NAME
                        Role Name for CloudTrails
  --region {us-east-1,us-east-2,eu-west-2}, -r {us-east-1,us-east-2,eu-west-2}
                        Region
  --role ROLE, -g ROLE  Role Name, used for STS
```

## Parameters

|Parameter|Usage|Requirement|
| ------- | --- | --------- |
| aws-account | The AWS account to assume and add the users to | **REQUIRED** |
| username | If a file isnt passed as a parameter, this must to used to indicate the user to create | **CONDITIONAL REQUIRED** |
| groupname | Group to associate the users to | **OPTIONAL** |
| set-key | If used, generated API Keys for the user(s) (Default = False) | **OPTIONAL** |
| file-name | File that is new line delimited of usernames to add to the account | **CONDITIONAL REQUIRED**

## Usage

## IAM Usage

All CSVs get created in ~/Documents/credentials-${AWSACCOUNT}.csv

#### Generate Single User with no Key

```
$ orion iam -a ${ASSUME_ACCOUNT_NUMBER} -u foo
CREATED: User foo has been created.
$ cat ~/Documents/credentials-${ASSUME_ACCOUNT_NUMBER}.csv
aws_account,username,password,AccessKeyId,SecretAccessKey,groupname
${ASSUME_ACCOUNT_NUMBER},foo,520566958022bbb5##,N/A,N/A,N/A
```

#### Generate Single User with Key

```
$ orion iam -a ${ASSUME_ACCOUNT_NUMBER} -u bar -k
CREATED: User bar has been created.
$ cat ~/Documents/credentials-${ASSUME_ACCOUNT_NUMBER}.csv
aws_account,username,password,AccessKeyId,SecretAccessKey,groupname
${ASSUME_ACCOUNT_NUMBER},bar,e405fa426ca18f14##,AKIAJXVZ4MQRRAVC3JEA,nxEtLYrdZNV1PUgubDxWdSArlMyqpihWcfUPin9n,N/A
```

#### Generate Users from file with keys 
## BUGGED

```
$ cat test.txt
alice
bob
charlie
$ orion iam -a ${ASSUME_ACCOUNT_NUMBER} -k -n customer_users -f test.txt
CREATED: User charlie has been created.
$ cat ~/Documents/credentials-${ASSUME_ACCOUNT_NUMBER}.csv
aws_account,username,password,AccessKeyId,SecretAccessKey,groupname
${ASSUME_ACCOUNT_NUMBER},charlie,3f31b0855a393b46##,AKIAIOOXBGUV5UOHGWCA,vgabetWf0HFM2HyIuInkI4w9CCoPbTtk1iUqepmU,customer_users
```

## Bugs

#### IAM 
Creating multiple users from a file seems to only create the last one


