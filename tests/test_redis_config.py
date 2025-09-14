"""RedisConfigクラスのテスト."""

import os
from unittest.mock import patch

import pytest

from ipinfo_geoip.constants import REDIS_CACHE_TTL_ENV, REDIS_URI_ENV
from ipinfo_geoip.exceptions import ValidationError
from ipinfo_geoip.redis_config import RedisConfig

TEST_REDIS_URI_STR: str = "redis://localhost:6379"
TEST_REDIS_TTL_INT: int = 3600
TEST_REDIS_TTL_STR: str = "3600"


class TestRedisConfig:
    """RedisConfigクラスのテストクラス."""

    def test_init(self) -> None:
        """初期化のテスト."""
        config = RedisConfig(TEST_REDIS_URI_STR, TEST_REDIS_TTL_STR)

        assert config.uri == TEST_REDIS_URI_STR
        assert config.ttl == TEST_REDIS_TTL_INT

    @patch.dict(
        os.environ,
        {
            REDIS_URI_ENV: TEST_REDIS_URI_STR,
            REDIS_CACHE_TTL_ENV: TEST_REDIS_TTL_STR,
        },
        clear=True,
    )
    def test_from_env(self) -> None:
        """環境変数からの作成テスト."""
        config = RedisConfig.from_env()

        assert config.uri == TEST_REDIS_URI_STR
        assert config.ttl == TEST_REDIS_TTL_INT

    @patch.dict(
        os.environ,
        {
            REDIS_CACHE_TTL_ENV: TEST_REDIS_TTL_STR,
        },
        clear=True,
    )
    def test_from_env_missing_uri(self) -> None:
        """URI環境変数不足のテスト."""
        match = f"Missing environment variables: {REDIS_URI_ENV}"
        with pytest.raises(ValidationError, match=match):
            _ = RedisConfig.from_env()

    @patch.dict(
        os.environ,
        {
            REDIS_URI_ENV: TEST_REDIS_URI_STR,
        },
        clear=True,
    )
    def test_from_env_missing_ttl(self) -> None:
        """TTL環境変数不足のテスト."""
        match = f"Missing environment variables: {REDIS_CACHE_TTL_ENV}"
        with pytest.raises(ValidationError, match=match):
            _ = RedisConfig.from_env()

    @patch.dict(
        os.environ,
        {},
        clear=True,
    )
    def test_from_env_missing_environment_variables(self) -> None:
        """複数の環境変数不足のテスト."""
        match = f"Missing environment variables: {REDIS_URI_ENV}, {REDIS_CACHE_TTL_ENV}"
        with pytest.raises(ValidationError, match=match):
            _ = RedisConfig.from_env()
