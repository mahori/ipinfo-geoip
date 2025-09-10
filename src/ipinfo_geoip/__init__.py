"""IPアドレスからネットワーク, AS番号, 国, 組織を取得するPythonモジュール."""

from .exceptions import (
    CacheError,
    ConfigurationError,
    GeoIPClientError,
    IPInfoError,
    NetworkError,
    RedisClientError,
    ValidationError,
)
from .geoip_client import GeoIPClient
from .ipinfo import IPInfo
from .redis_client import RedisClient

__version__ = "0.0.1"
__author__ = "mahori"
__email__ = "4198737+mahori@users.noreply.github.com"

__all__ = [
    "CacheError",
    "ConfigurationError",
    "GeoIPClient",
    "GeoIPClientError",
    "IPInfo",
    "IPInfoError",
    "NetworkError",
    "RedisClient",
    "RedisClientError",
    "ValidationError",
]
