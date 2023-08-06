# appsettingsreader

Read `appSettings` from XML configuration files, to share .NET configration with python applications.

As it is only valid for `.config` files to have a single `appSettings` element in .NET only the first will be read, and any others will be ignored.

## Usage

```py
from appsettingsreader import *

# Read from an arbitrary file
settings = read_appsettings("/some/pathlike/thing")

# Shortcuts for FBS configuration
bisappsettings = read_bis_appsettings("dev")
icat_settings = read_icat_appsettings("prod")
```

## Releasing

Building and uploading a release require the `build` and `twine` python packages, respectively.

To make a release, update the version number in `setup.cfg` and run `make release`. Note that there's an issue with mintty and entering credentials for uploading, so prefix the command with `winpty` or use a different terminal.
