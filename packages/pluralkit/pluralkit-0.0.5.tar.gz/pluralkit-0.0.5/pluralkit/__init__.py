
from collections import namedtuple

from .v1.client import Client
from .v1.models import (
    Member,
    System,
    ProxyTag,
    ProxyTags,
    Switch,
    Privacy,
    Timestamp,
    Color,
    Birthday,
    Timezone,
    Message,
)
from .v1 import errors

VersionInfo = namedtuple("VersionInfo", "major minor build")
version_info = VersionInfo(
    major=0,
    minor=0,
    build=5,
)

__title__ = "pluralkit"
__author__ = "Madison Landry, Alyx Warner"
__copyright__ = "Copyright 2021-present Madison Landry, Alyx Warner"
__version__ = f"{version_info.major}.{version_info.minor}.{version_info.build}"
