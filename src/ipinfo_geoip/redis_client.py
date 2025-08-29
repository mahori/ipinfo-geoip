"""Redisキャッシュクライアント."""

import os
from collections import UserDict
from typing import Self, cast

import redis

from .constants import REDIS_CACHE_TTL_ENV, REDIS_URI_ENV
from .exceptions import ConfigurationError, RedisClientError, ValidationError
from .ipdata import IPData


class RedisConfig:
    """Redis接続設定クラス.

    Attributes:
        uri: Redis接続URI

    """

    def __init__(self, uri: str, ttl: str) -> None:
        """Redis設定を初期化する.

        Args:
            uri: Redis接続URI
            ttl: キャッシュのTTL(秒)

        Raises:
            TypeError: uriが文字列でない場合

        """
        if not isinstance(uri, str):
            raise TypeError

        self.uri = uri
        self.ttl = ttl

    @classmethod
    def from_env(cls) -> Self:
        """環境変数からRedis設定を作成する.

        Returns:
            環境変数から作成されたRedisConfig

        Raises:
            ValidationError: 必要な環境変数が設定されていない場合

        """
        missing_vars = []
        if REDIS_URI_ENV not in os.environ:
            missing_vars.append(REDIS_URI_ENV)
        if REDIS_CACHE_TTL_ENV not in os.environ:
            missing_vars.append(REDIS_CACHE_TTL_ENV)

        if missing_vars:
            msg = f"Missing environment variables: {', '.join(missing_vars)}"
            raise ValidationError(msg)

        uri = os.environ[REDIS_URI_ENV]
        ttl = os.environ[REDIS_CACHE_TTL_ENV]

        return cls(uri, ttl)


class RedisClient(UserDict[str, IPData | None]):
    """Redisキャッシュクライアント."""

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
        self.ttl = int(config.ttl)

    def __missing__(self, ip_address: str) -> IPData | None:
        """RedisからIP情報を取得する.

        Args:
            ip_address: 検索するIPアドレス

        Returns:
            キャッシュされたIP情報
            見つからない場合はNone

        Raises:
            TypeError: ip_addressが文字列でない場合
            RedisClientError: Redisでエラーが発生した場合

        """
        if not isinstance(ip_address, str):
            raise TypeError

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
        """IP情報をRedisにキャッシュする.

        Args:
            ip_address: IPアドレス
            ip_data: キャッシュするIP情報

        Raises:
            TypeError: 引数の型が正しくない場合

        """
        if not isinstance(ip_address, str):
            raise TypeError
        if not isinstance(ip_data, IPData):
            raise TypeError

        name = f"ipinfo:{ip_address}"
        mapping = ip_data.to_dict()
        self.client.hset(name, mapping=mapping)
        self.client.expire(name, self.ttl)

        super().__setitem__(ip_address, ip_data)
