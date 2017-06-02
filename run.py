#!/usr/bin/env python3

import sys
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

sys.path.append("lib/pyMattermost/src")

from src.Application import Application

app = Application()
app.run(sys.argv)
