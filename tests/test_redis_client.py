"""RedisClientクラスのテスト."""

from collections import UserDict
from typing import Final
from unittest.mock import Mock, patch

import pytest
import redis

from ipinfo_geoip.exceptions import ConfigurationError, RedisClientError, ValidationError
from ipinfo_geoip.ipdata import IPData
from ipinfo_geoip.redis_client import RedisClient

TEST_REDIS_URI: Final[str] = "redis://localhost:6379"
TEST_REDIS_TTL: Final[int] = 3600

TEST_IP_ADDRESS: Final[str] = "192.0.2.1"
TEST_IP_NETWORK: Final[str] = "192.0.2.0/24"
TEST_AS_NUMBER: Final[str] = "65001"
TEST_COUNTRY_CODE: Final[str] = "US"
TEST_ORGANIZATION: Final[str] = "Test Organization"

TEST_IPDATA: Final[IPData] = IPData(
    ip_address=TEST_IP_ADDRESS,
    network=TEST_IP_NETWORK,
    as_number=TEST_AS_NUMBER,
    country=TEST_COUNTRY_CODE,
    organization=TEST_ORGANIZATION,
)
TEST_IPDATA_INCOMPLETE: Final[IPData] = IPData(
    ip_address=TEST_IP_ADDRESS,
    as_number=TEST_AS_NUMBER,
    network="",
    country=TEST_COUNTRY_CODE,
    organization=TEST_ORGANIZATION,
)


class TestRedisClient:
    """RedisClientクラスのテストクラス."""

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_init(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """初期化のテスト."""
        # モック設定
        mock_config = Mock()
        mock_config.uri = TEST_REDIS_URI
        mock_config.ttl = TEST_REDIS_TTL
        mock_from_env.return_value = mock_config

        mock_redis_instance = Mock()
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()

        # 検証
        assert isinstance(client, RedisClient)
        assert isinstance(client, UserDict)
        mock_from_env.assert_called_once()
        mock_redis_from_url.assert_called_once_with(TEST_REDIS_URI, decode_responses=True)

    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_init_with_configuration_error(self, mock_from_env: Mock) -> None:
        """設定エラーでの初期化テスト."""
        # モック設定
        mock_from_env.side_effect = ValidationError("Missing environment variables")

        # テスト実行
        with pytest.raises(ConfigurationError):
            _ = RedisClient()

        # 検証
        mock_from_env.assert_called_once()

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_missing_with_invalid_ip_value(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """IPアドレスが無効な場合の__missing__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_redis_instance = Mock()
        mock_redis_instance.hgetall.return_value = {}
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()

        with pytest.raises(ValidationError):
            _ = client["invalid.ip"]

        # 検証
        mock_redis_instance.hgetall.assert_not_called()

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_missing_success(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """成功時の__missing__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_redis_instance = Mock()
        mock_redis_instance.hgetall.return_value = TEST_IPDATA.to_dict()
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()
        result = client[TEST_IP_ADDRESS]

        # 検証
        assert isinstance(result, IPData)
        assert result.ip_address == TEST_IP_ADDRESS
        assert result.network == TEST_IP_NETWORK
        assert result.as_number == TEST_AS_NUMBER
        assert result.country == TEST_COUNTRY_CODE
        assert result.organization == TEST_ORGANIZATION
        mock_redis_instance.hgetall.assert_called_once_with(f"ipinfo:{TEST_IP_ADDRESS}")

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_missing_with_connection_error(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """接続エラーでの__missing__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_redis_instance = Mock()
        mock_redis_instance.hgetall.side_effect = redis.ConnectionError("Connection failed")
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()

        with pytest.raises(RedisClientError):
            _ = client[TEST_IP_ADDRESS]

        # 検証
        mock_redis_instance.hgetall.assert_called_once_with(f"ipinfo:{TEST_IP_ADDRESS}")

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_missing_with_empty_response(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """レスポンスが空な場合の__missing__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_redis_instance = Mock()
        mock_redis_instance.hgetall.return_value = {}
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()
        result = client[TEST_IP_ADDRESS]

        # 検証
        assert result is None
        mock_redis_instance.hgetall.assert_called_once_with(f"ipinfo:{TEST_IP_ADDRESS}")

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_missing_with_partial_data(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """データが不完全な場合の__missing__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_redis_instance = Mock()
        mock_redis_instance.hgetall.return_value = TEST_IPDATA_INCOMPLETE.to_dict()
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()
        result = client[TEST_IP_ADDRESS]

        # 検証
        assert result is None
        mock_redis_instance.hgetall.assert_called_once_with(f"ipinfo:{TEST_IP_ADDRESS}")

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_setitem_with_invalid_ip_value(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """IPアドレスが無効な場合の__setitem__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_redis_pipeline = Mock()
        mock_redis_pipeline.hset.return_value = 0
        mock_redis_pipeline.expire.return_value = False
        mock_redis_pipeline.execute.return_value = [0, False]

        mock_redis_instance = Mock()
        mock_redis_instance.pipeline.return_value = mock_redis_pipeline
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()

        with pytest.raises(ValidationError):
            client["invalid.ip"] = TEST_IPDATA

        # 検証
        mock_redis_instance.pipeline.assert_not_called()
        mock_redis_pipeline.hset.assert_not_called()
        mock_redis_pipeline.expire.assert_not_called()
        mock_redis_pipeline.execute.assert_not_called()

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_setitem_success(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """成功時の__setitem__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_config.ttl = TEST_REDIS_TTL
        mock_from_env.return_value = mock_config

        mock_redis_pipeline = Mock()
        mock_redis_pipeline.hset.return_value = 1
        mock_redis_pipeline.expire.return_value = True
        mock_redis_pipeline.execute.return_value = [1, True]

        mock_redis_instance = Mock()
        mock_redis_instance.pipeline.return_value = mock_redis_pipeline
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()
        client[TEST_IP_ADDRESS] = TEST_IPDATA

        # 検証
        mock_redis_instance.pipeline.assert_called_once()
        mock_redis_pipeline.hset.assert_called_once_with(f"ipinfo:{TEST_IP_ADDRESS}", mapping=TEST_IPDATA.to_dict())
        mock_redis_pipeline.expire.assert_called_once_with(f"ipinfo:{TEST_IP_ADDRESS}", TEST_REDIS_TTL)
        mock_redis_pipeline.execute.assert_called_once()

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_redis_with_incomplete_ipdata(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """データが不完全な場合の__setitem__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_redis_pipeline = Mock()
        mock_redis_pipeline.hset.return_value = 0
        mock_redis_pipeline.expire.return_value = False
        mock_redis_pipeline.execute.return_value = [0, False]

        mock_redis_instance = Mock()
        mock_redis_instance.pipeline.return_value = mock_redis_pipeline
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()
        client[TEST_IP_ADDRESS] = TEST_IPDATA_INCOMPLETE

        # 検証
        mock_redis_instance.pipeline.assert_not_called()
        mock_redis_pipeline.hset.assert_not_called()
        mock_redis_pipeline.expire.assert_not_called()
        mock_redis_pipeline.execute.assert_not_called()

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_redis_with_none_ipdata(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """データがNoneな場合の__setitem__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_redis_pipeline = Mock()
        mock_redis_pipeline.hset.return_value = 0
        mock_redis_pipeline.expire.return_value = False
        mock_redis_pipeline.execute.return_value = [0, False]

        mock_redis_instance = Mock()
        mock_redis_instance.pipeline.return_value = mock_redis_pipeline
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()
        client[TEST_IP_ADDRESS] = None

        # 検証
        mock_redis_instance.pipeline.assert_not_called()
        mock_redis_pipeline.hset.assert_not_called()
        mock_redis_pipeline.expire.assert_not_called()
        mock_redis_pipeline.execute.assert_not_called()
