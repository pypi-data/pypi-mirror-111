""" AppSettingsReader

A set of functions for reading appSettings elements from .NET config files into a dictionary.

Use `read_appsettings(path)` to specify a full path. The file specified must be XML with an `appSettings` element, with `add` element children which have `key` and `value` attributes.

Use `read_bis_appsettings(env)` or `read_icat_appsettings(env)`, where env is one of "debug", "dev", or "prod", as  shortcuts to the FBS config files for BISApps/isis-icat respectively.

Tested in python 3.7.0, but should work with most/all python 3 versions.
"""

from appsettingsreader.reader import read_appsettings, read_bis_appsettings, read_icat_appsettings
