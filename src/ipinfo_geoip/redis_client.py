"""Redisクライアント."""

import ipaddress
from collections import UserDict
from typing import cast

import redis

from ipinfo_geoip.exceptions import ConfigurationError, RedisClientError, ValidationError
from ipinfo_geoip.ipdata import IPData
from ipinfo_geoip.redis_config import RedisConfig


class RedisClient(UserDict[str, IPData | None]):
    """Redisクライアント."""

    def __init__(self) -> None:
        """Redisクライアントを初期化する.

        Raises:
            ConfigurationError: 必要な認証情報が不足している場合

        """
        super().__init__()

        try:
            config = RedisConfig.from_env()
        except ValidationError as e:
            msg = "Redis configuration error"
            raise ConfigurationError(msg, {"error": str(e)}) from e
        self.client = redis.Redis.from_url(config.uri, decode_responses=True)
        self.ttl = config.ttl

    def __missing__(self, ip_address: str) -> IPData | None:
        """RedisからIPアドレス情報を取得する.

        Args:
            ip_address: 検索するIPアドレス

        Returns:
            キャッシュされたIPアドレス情報
            見つからない場合はNone

        Raises:
            TypeError: ip_addressが文字列でない場合
            RedisClientError: Redisでエラーが発生した場合

        """
        if not isinstance(ip_address, str):
            raise TypeError

        try:
            _ = ipaddress.ip_address(ip_address)
        except ValueError as e:
            msg = f"Invalid IP address: {ip_address}"
            raise ValidationError(msg, {"error": str(e)}) from e

        name = f"ipinfo:{ip_address}"
        try:
            response = self.client.hgetall(name)
        except redis.ConnectionError as e:
            msg = f"Redis connection error: {e}"
            raise RedisClientError(msg, {"error": str(e)}) from e

        if not response:
            return None

        response = cast("dict[str, str]", response)

        network = response["network"]
        as_number = response["as_number"]
        country = response["country"]
        organization = response["organization"]

        ip_data = IPData(ip_address, network, as_number, country, organization)

        super().__setitem__(ip_address, ip_data)

        return ip_data

    def __setitem__(self, ip_address: str, ip_data: IPData | None) -> None:
        """IPアドレス情報をRedisにキャッシュする.

        Args:
            ip_address: IPアドレス
            ip_data: キャッシュするIPアドレス情報

        Raises:
            TypeError: 引数の型が正しくない場合

        """
        if not isinstance(ip_address, str):
            raise TypeError
        if not isinstance(ip_data, IPData):
            raise TypeError

        name = f"ipinfo:{ip_address}"
        mapping = ip_data.to_dict()

        pipeline = self.client.pipeline()
        pipeline.hset(name, mapping=mapping)
        pipeline.expire(name, self.ttl)
        pipeline.execute()

        super().__setitem__(ip_address, ip_data)
