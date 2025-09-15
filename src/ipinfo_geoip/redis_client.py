"""Redisクライアント."""

import ipaddress
from collections import UserDict
from typing import cast

import redis

from .exceptions import ConfigurationError, RedisClientError, ValidationError
from .ipdata import IPData
from .redis_config import RedisConfig


class RedisClient(UserDict[str, IPData | None]):
    """Redisクライアント."""

    def __init__(self) -> None:
        """RedisClientインスタンスを初期化する.

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
            Redisから取得したIPアドレス情報
            見つからない場合はNone

        Raises:
            RedisClientError: Redisでエラーが発生した場合
            ValidationError: ip_addressが不正な場合

        """
        try:
            _ = ipaddress.ip_address(ip_address)
        except ValueError as e:
            msg = f"Invalid IP address: {ip_address}"
            raise ValidationError(msg, {"error": str(e)}) from e

        try:
            response = self.client.hgetall(f"ipinfo:{ip_address}")
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

        if network == "" or as_number == "" or country == "" or organization == "":
            return None

        ip_data = IPData(ip_address, network, as_number, country, organization)

        super().__setitem__(ip_address, ip_data)

        return ip_data

    def __setitem__(self, ip_address: str, ip_data: IPData | None) -> None:
        """IPアドレス情報をRedisに保存する.

        Args:
            ip_address: IPアドレス
            ip_data: 保存するIPアドレス情報

        Raises:
            ValidationError: ip_addressが不正な場合

        """
        try:
            _ = ipaddress.ip_address(ip_address)
        except ValueError as e:
            msg = f"Invalid IP address: {ip_address}"
            raise ValidationError(msg, {"error": str(e)}) from e

        if ip_data is None or not ip_data.is_complete():
            return

        name = f"ipinfo:{ip_address}"
        mapping = ip_data.to_dict()

        pipeline = self.client.pipeline()
        pipeline.hset(name, mapping=mapping)
        pipeline.expire(name, self.ttl)
        pipeline.execute()

        super().__setitem__(ip_address, ip_data)
