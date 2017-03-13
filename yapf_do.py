#!/usr/bin/env python

# -*- coding: utf-8 -*-
import re
import sys
import os

now_dir = os.getcwd()
os.chdir('/mnt/ilustre/users/jun.yan/.local/lib/python2.7/site-packages/yapf-0.16.0-py2.7.egg/')
from yapf import run_main
os.chdir(now_dir)
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(run_main())
