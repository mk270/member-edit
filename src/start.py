#!/usr/bin/env python

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
