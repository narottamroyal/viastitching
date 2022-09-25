from pathlib import Path
from zipfile import ZipFile

plugin_files = [
    "__init__.py",
    "viastitching_dialog.py",
    "viastitching_gui.py",
    "viastitching_plugin.py",
    "viastitching.png"
]

plugins = Path("plugins")

with ZipFile("viastitching.zip", mode="w") as archive:
    for filename in plugin_files:
        archive.write(filename, plugins / filename)
    archive.write("metadata.json")
