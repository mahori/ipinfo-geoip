"""RedisClientクラスのテスト."""

from collections import UserDict
from unittest.mock import Mock, patch

import pytest
import redis

from ipinfo_geoip.exceptions import ConfigurationError, RedisClientError, ValidationError
from ipinfo_geoip.ipdata import IPData
from ipinfo_geoip.redis_client import RedisClient


class TestRedisClient:
    """RedisClientクラスのテストクラス."""

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_init(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """初期化のテスト."""
        # モック設定
        mock_config = Mock()
        mock_config.uri = "redis://localhost:6379"
        mock_config.ttl = 3600
        mock_from_env.return_value = mock_config

        mock_redis_instance = Mock()
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()

        # 検証
        mock_from_env.assert_called_once()
        mock_redis_from_url.assert_called_once_with("redis://localhost:6379", decode_responses=True)
        assert isinstance(client, UserDict)

    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_init_with_configuration_error(self, mock_from_env: Mock) -> None:
        """設定エラーでの初期化テスト."""
        mock_from_env.side_effect = ValidationError("Missing environment variable")

        with pytest.raises(ConfigurationError):
            RedisClient()

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_missing_success(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """成功時の__missing__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_config.ttl = 3600
        mock_from_env.return_value = mock_config

        mock_redis_data = {
            "network": "8.8.8.0/24",
            "as_number": "15169",
            "country": "US",
            "organization": "GOOGLE",
        }

        mock_redis_instance = Mock()
        mock_redis_instance.hgetall.return_value = mock_redis_data
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()
        result = client["8.8.8.8"]

        # 検証
        assert isinstance(result, IPData)
        assert result.ip_address == "8.8.8.8"
        assert result.network == "8.8.8.0/24"
        assert result.as_number == "15169"
        assert result.country == "US"
        assert result.organization == "GOOGLE"
        mock_redis_instance.hgetall.assert_called_once_with("ipinfo:8.8.8.8")

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_missing_with_empty_response(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """空のレスポンスでのテスト."""
        # モック設定
        mock_config = Mock()
        mock_config.ttl = 3600
        mock_from_env.return_value = mock_config

        mock_redis_instance = Mock()
        mock_redis_instance.hgetall.return_value = {}
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()
        result = client["8.8.8.8"]

        # 検証
        assert result is None

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_missing_with_connection_error(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """接続エラーでのテスト."""
        # モック設定
        mock_config = Mock()
        mock_config.ttl = 3600
        mock_from_env.return_value = mock_config

        mock_redis_instance = Mock()
        mock_redis_instance.hgetall.side_effect = redis.ConnectionError("Connection failed")
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()

        with pytest.raises(RedisClientError):
            client["8.8.8.8"]

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_missing_with_invalid_ip_type(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """無効なIPアドレス型のテスト."""
        # モック設定
        mock_config = Mock()
        mock_config.ttl = 3600
        mock_from_env.return_value = mock_config

        mock_redis_instance = Mock()
        mock_redis_from_url.return_value = mock_redis_instance

        client = RedisClient()

        with pytest.raises(TypeError):
            _ = client[123]  # type: ignore[index]

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_missing_with_invalid_ip_value(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """無効なIPアドレス値のテスト."""
        # モック設定
        mock_config = Mock()
        mock_config.ttl = 3600
        mock_from_env.return_value = mock_config

        mock_redis_instance = Mock()
        mock_redis_from_url.return_value = mock_redis_instance

        client = RedisClient()

        with pytest.raises(ValidationError):
            _ = client["invalid.ip"]

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_missing_with_partial_data(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """部分的なデータでのテスト."""
        # モック設定
        mock_config = Mock()
        mock_config.ttl = 3600
        mock_from_env.return_value = mock_config

        mock_redis_data = {
            "network": "",
            "as_number": "15169",
            "country": "US",
            "organization": "GOOGLE",
        }

        mock_redis_instance = Mock()
        mock_redis_instance.hgetall.return_value = mock_redis_data
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()
        result = client["8.8.8.8"]

        # 検証
        assert result is None

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_setitem_success(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """成功時の__setitem__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_config.ttl = 3600
        mock_from_env.return_value = mock_config

        mock_redis_pipeline = Mock()

        mock_redis_instance = Mock()
        mock_redis_instance.pipeline.return_value = mock_redis_pipeline
        mock_redis_from_url.return_value = mock_redis_instance

        # テストデータ
        ip_address = "8.8.8.8"
        ip_data = IPData(
            ip_address=ip_address,
            network="8.8.8.0/24",
            as_number="15169",
            country="US",
            organization="GOOGLE",
        )

        # テスト実行
        client = RedisClient()
        client[ip_address] = ip_data

        # 検証
        expected_mapping = {
            "ip_address": "8.8.8.8",
            "network": "8.8.8.0/24",
            "as_number": "15169",
            "country": "US",
            "organization": "GOOGLE",
        }
        mock_redis_instance.pipeline.assert_called_once()
        mock_redis_pipeline.hset.assert_called_once_with("ipinfo:8.8.8.8", mapping=expected_mapping)
        mock_redis_pipeline.expire.assert_called_once_with("ipinfo:8.8.8.8", 3600)
        mock_redis_pipeline.execute.assert_called_once()

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_setitem_with_invalid_ip_type(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """無効なIPアドレス型での__setitem__テスト."""
        # モック設定
        mock_config = Mock()
        mock_config.ttl = 3600
        mock_from_env.return_value = mock_config

        mock_redis_instance = Mock()
        mock_redis_from_url.return_value = mock_redis_instance

        client = RedisClient()
        ip_data = IPData(
            "8.8.8.8",
            "8.8.8.0/24",
            "15169",
            "US",
            "GOOGLE",
        )

        with pytest.raises(TypeError):
            client[123] = ip_data  # type: ignore[index]

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_setitem_with_invalid_data_type(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """無効なデータ型での__setitem__テスト."""
        # モック設定
        mock_config = Mock()
        mock_config.ttl = 3600
        mock_from_env.return_value = mock_config

        mock_redis_instance = Mock()
        mock_redis_from_url.return_value = mock_redis_instance

        client = RedisClient()

        with pytest.raises(TypeError):
            client["8.8.8.8"] = "invalid_data"  # type: ignore[assignment]

    @patch("ipinfo_geoip.redis_client.redis.Redis.from_url")
    @patch("ipinfo_geoip.redis_client.RedisConfig.from_env")
    def test_redis_key_format(self, mock_from_env: Mock, mock_redis_from_url: Mock) -> None:
        """Redisキー形式のテスト."""
        # モック設定
        mock_config = Mock()
        mock_config.ttl = 3600
        mock_from_env.return_value = mock_config

        mock_redis_instance = Mock()
        mock_redis_instance.hgetall.return_value = {}
        mock_redis_from_url.return_value = mock_redis_instance

        # テスト実行
        client = RedisClient()
        client["192.168.1.1"]

        # キー形式の検証
        mock_redis_instance.hgetall.assert_called_once_with("ipinfo:192.168.1.1")
