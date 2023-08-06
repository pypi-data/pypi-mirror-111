import warnings
import xml.etree.ElementTree as ET
from typing import Dict
from pathlib import Path, PurePath

_fbs_root_path = PurePath("/FBS/Apps")

def _is_valid_add_element(elem):
    return elem.tag == "add" and "key" in elem.attrib and "value" in elem.attrib


class AppSettingsReader:
    def __init__(self, path: str):
        assert Path(path).is_file(), f"File '{path}' does not exist"
        self.path = path

    def read(self) -> Dict[str, str]:
        root = ET.parse(str(self.path)).getroot()
        if root.tag != "appSettings":
            root = root.find(".//appSettings")
        assert root, f"No 'appSettings' element present in specified file '{self.path}'"

        valid_children = [e for e in root if _is_valid_add_element(e)]
        num_invalid = len(root) - len(valid_children)
        if num_invalid > 0:
            warnings.warn(f"There are {num_invalid} invalid child elements in the appSettings which are being ignored.")

        return {
            c.attrib["key"]: c.attrib["value"] for c in valid_children
        }


_envs = ["prod", "dev", "debug"]
_icat_env_names = {
    "prod": "release",
    "dev": "debug",
    "debug": "debug",
}

def _bisapps_path(env):
    return _fbs_root_path / f"BISAppSettings-{env.title()}.config"

def _icat_path(env):
    icat_env = _icat_env_names[env]
    return _fbs_root_path / "isis-icat-configs" / f"isis-icat-{icat_env}.config"

def read_appsettings(path: str) -> Dict[str, str]:
    return AppSettingsReader(path=path).read()

def read_bis_appsettings(env: str) -> Dict[str, str]:
    assert env in _envs, f"env must be one of {_envs}"
    return AppSettingsReader(_bisapps_path(env)).read()

def read_icat_appsettings(env: str) -> Dict[str, str]:
    assert env in _envs, f"env must be one of {_envs}"
    return AppSettingsReader(_icat_path(env)).read()
