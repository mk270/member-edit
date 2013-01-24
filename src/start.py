#!/usr/bin/env python

#  MemberEdit, a basic web interface for running member lists, by Martin Keegan

#  Copyright (C) 2013  Martin Keegan
#
#  This programme is free software; you may redistribute and/or modify
#  it under the terms of the Apache Software Licence v2.0

import sys
import ConfigParser
import rsdb_web

def run():
    if len(sys.argv) != 2:
        print "Usage: start.py conf.ini"
        sys.exit(1)

    _, config_file = sys.argv

    config = ConfigParser.ConfigParser()
    config.read(config_file)

    rsdb_web.start(config)

if __name__ == '__main__':
    run()
