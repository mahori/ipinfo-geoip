"""IPアドレスからネットワーク, AS番号, 国, 組織を取得するPythonモジュール."""

from .exceptions import (
    ConfigurationError,
    GeoIPClientError,
    IPInfoError,
    RedisClientError,
    ValidationError,
)
from .ipinfo import IPInfo

__version__ = "0.0.2"
__author__ = "mahori"
__email__ = "4198737+mahori@users.noreply.github.com"

__all__ = [
    "ConfigurationError",
    "GeoIPClientError",
    "IPInfo",
    "IPInfoError",
    "RedisClientError",
    "ValidationError",
]
