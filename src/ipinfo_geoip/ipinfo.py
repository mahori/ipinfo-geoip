"""IPアドレスからネットワーク, AS番号, 国, 組織を取得するメインクラス."""

import ipaddress
from collections import UserDict

from .exceptions import ValidationError
from .geoip_client import GeoIPClient
from .redis_client import RedisClient


class IPInfo(UserDict[str, dict[str, str] | None]):
    """IPアドレスからネットワーク, AS番号, 国, 組織を取得するメインクラス."""

    def __init__(self) -> None:
        """IPInfoを初期化する."""
        super().__init__()

        self.geoip = GeoIPClient()
        self.redis = RedisClient()

    def __missing__(self, ip_address: str) -> dict[str, str] | None:
        """指定されたIPアドレス情報を取得する.

        Redisからキャッシュを検索する
        見つからなければGeoLite2 Web Serviceから取得する
        取得したデータに不備がなければRedisにキャッシュされる

        Args:
            ip_address: 検索するIPアドレス

        Returns:
            IPアドレス情報
            見つからない場合はNone

        Raises:
            TypeError: ip_addressが文字列でない場合

        """
        if not isinstance(ip_address, str):
            raise TypeError

        try:
            _ = ipaddress.ip_address(ip_address)
        except ValueError as e:
            msg = f"Invalid IP address: {ip_address}"
            raise ValidationError(msg, {"error": str(e)}) from e

        ip_data = self.redis[ip_address]
        if ip_data is not None:
            return ip_data.to_dict()

        ip_data = self.geoip[ip_address]
        if ip_data is not None:
            result = ip_data.to_dict()
            if ip_data.is_complete():
                self.redis[ip_address] = ip_data
                super().__setitem__(ip_address, result)
            return result

        return None
