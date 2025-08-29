"""IPアドレスからGeoIP情報を取得するメインクラス."""

from collections import UserDict

from .geoip_client import GeoIPClient
from .redis_client import RedisClient


class IPInfo(UserDict[str, dict[str, str] | None]):
    """IPアドレスからGeoIP情報を取得するメインクラス."""

    def __init__(self) -> None:
        """IPInfoを初期化する."""
        super().__init__()

        self.redis = RedisClient()
        self.geoip = GeoIPClient()

    def __missing__(self, ip_address: str) -> dict[str, str] | None:
        """指定されたIPアドレスの情報を取得する.

        Redisキャッシュから検索する
        見つからなければGeoIPサービスから取得する
        GeoIPから取得した完全なデータはRedisにキャッシュされる

        Args:
            ip_address: 検索するIPアドレス

        Returns:
            IPアドレスの地理的位置情報
            見つからない場合はNone

        Raises:
            TypeError: ip_addressが文字列でない場合

        """
        if not isinstance(ip_address, str):
            raise TypeError

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
