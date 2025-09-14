"""Redis接続設定."""

import os
from typing import Self

from .constants import REDIS_CACHE_TTL_ENV, REDIS_URI_ENV
from .exceptions import ValidationError


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
        if not isinstance(ttl, str):
            raise TypeError

        self.uri = uri
        self.ttl = int(ttl)

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
