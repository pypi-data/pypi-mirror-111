# =====================================
# generator=datazen
# version=1.7.6
# hash=c9fa84685e3f942cdda952632ee99b24
# =====================================

"""
vbinds - Package definition for distribution.
"""

# third-party
from vmklib.setup import setup

# internal
from vbinds import PKG_NAME, VERSION, DESCRIPTION


author_info = {
    "name": "Vaughn Kottler",
    "email": "vaughnkottler@gmail.com",
    "username": "vkottler",
}
pkg_info = {"name": PKG_NAME, "version": VERSION, "description": DESCRIPTION}
setup(
    pkg_info,
    author_info,
    url_override="https://github.com/vkottler/keybinds/tree/master/wow",
    console_overrides=["bapi=vbinds.entry:main"],
)
