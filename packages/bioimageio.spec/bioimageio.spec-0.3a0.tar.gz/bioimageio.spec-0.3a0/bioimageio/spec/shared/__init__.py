import json

from pathlib import Path

from .common import BIOIMAGEIO_CACHE_PATH, yaml


_license_file = Path(__file__).parent.parent / "static" / "licenses.json"
_license_data = json.loads(_license_file.read_text())

LICENSES = {x["licenseId"]: x for x in _license_data["licenses"]}
LICENSE_DATA_VERSION = _license_data['licenseListVersion']
