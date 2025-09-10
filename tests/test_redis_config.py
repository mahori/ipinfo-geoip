"""RedisConfigクラスのテスト."""

import os
from unittest.mock import patch

import pytest

from ipinfo_geoip.exceptions import ValidationError
from ipinfo_geoip.redis_config import RedisConfig


class TestRedisConfig:
    """RedisConfigクラスのテストクラス."""

    def test_init(self) -> None:
        """初期化のテスト."""
        config = RedisConfig("redis://localhost:6379", "3600")

        assert config.uri == "redis://localhost:6379"
        assert config.ttl == "3600"

    def test_init_with_invalid_uri_type(self) -> None:
        """無効なURI型のテスト."""
        with pytest.raises(TypeError):
            RedisConfig(123, "3600")  # type: ignore[arg-type]

    @patch.dict(
        os.environ,
        {
            "IPINFO_REDIS_URI": "redis://localhost:6379",
            "IPINFO_REDIS_CACHE_TTL": "3600",
        },
        clear=True,
    )
    def test_from_env(self) -> None:
        """環境変数からの作成テスト."""
        config = RedisConfig.from_env()

        assert config.uri == "redis://localhost:6379"
        assert config.ttl == "3600"

    @patch.dict(
        os.environ,
        {
            "IPINFO_REDIS_CACHE_TTL": "3600",
        },
        clear=True,
    )
    def test_from_env_missing_uri(self) -> None:
        """URI環境変数不足のテスト."""
        with pytest.raises(ValidationError):
            RedisConfig.from_env()

    @patch.dict(
        os.environ,
        {
            "IPINFO_REDIS_URI": "redis://localhost:6379",
        },
        clear=True,
    )
    def test_from_env_missing_ttl(self) -> None:
        """TTL環境変数不足のテスト."""
        with pytest.raises(ValidationError):
            RedisConfig.from_env()
