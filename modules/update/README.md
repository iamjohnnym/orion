# Orion CommandLine Tool

================================================

## Overview

Module to update the current program to a desired branch.  The branch defaults to master.

## Capabilities

- Update 
  - Specify desired branch for use

### List Modules

```
$ python orion -h
usage: orion [-h] {update} ...

positional arguments:
  {update}  Active Modules
    update         Update orion program

optional arguments:
  -h, --help       show this help message and exit
```

### Structure

```
$ orion update -h
usage: orion update [-h] [--branch BRANCH]

optional arguments:
  -h, --help            show this help message and exit
  --branch BRANCH, -b BRANCH 
                        Branch to Update to
```

## Parameters

### Snapshot Parameters

|Parameter|Usage|Requirement|Defaults|
| ------- | --- | --------- | ------ |
| branch | Update tool to current version of ${branch} | **REQUIRED** | master |
 
## Usage

### IAM Usage

```
$ orion update -b master
Switched to branch 'master'
Your branch is behind 'origin/master' by 5 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)
Updating 7738428..b8250dc
Fast-forward
```

## Bugs

- NA

## TODO:

#### Feature

- if modules can be saved in individual repos, specify a repo name with optional url to download for use
