#!/usr/bin/env python3

import sys
import gi
import os

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

basedir = os.path.realpath(__file__)
basedir = os.path.dirname(basedir)

sys.path.append(basedir + "/lib/pyMattermost/src")

from src.Application import Application

app = Application()
app.run(sys.argv)
