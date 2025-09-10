"""IPInfoクラスのテスト."""

from collections import UserDict
from unittest.mock import Mock, patch

import pytest

from ipinfo_geoip import IPInfo
from ipinfo_geoip.ipdata import IPData


class TestIPInfo:
    """IPInfoクラスのテストクラス."""

    @patch("ipinfo_geoip.ipinfo.RedisClient")
    @patch("ipinfo_geoip.ipinfo.GeoIPClient")
    def test_init(self, mock_redis_client: Mock, mock_geoip_client: Mock) -> None:
        """初期化のテスト."""
        ipinfo = IPInfo()

        assert isinstance(ipinfo, UserDict)
        mock_redis_client.assert_called_once()
        mock_geoip_client.assert_called_once()

    @patch("ipinfo_geoip.ipinfo.RedisClient")
    @patch("ipinfo_geoip.ipinfo.GeoIPClient")
    def test_missing_with_redis_hit(self, mock_redis_client: Mock, mock_geoip_client: Mock) -> None:
        """Redisキャッシュヒット時のテスト."""
        # テストデータ
        ip_address = "8.8.8.8"
        ip_data = IPData(
            ip_address=ip_address,
            network="8.8.8.0/24",
            as_number="15169",
            country="US",
            organization="Google LLC",
        )

        # Redisクライアントのモック設定
        mock_redis_instance = Mock()
        mock_redis_instance.__getitem__ = Mock(return_value=ip_data)
        mock_redis_instance.__setitem__ = Mock()
        mock_redis_client.return_value = mock_redis_instance

        # GeoIPクライアントのモック設定
        mock_geoip_instance = Mock()
        mock_geoip_instance.__getitem__ = Mock(return_value=None)
        mock_geoip_client.return_value = mock_geoip_instance

        # IPInfoインスタンス作成
        ipinfo = IPInfo()
        ipinfo.redis = mock_redis_instance
        ipinfo.geoip = mock_geoip_instance

        # テスト実行
        result = ipinfo[ip_address]

        # 検証
        assert result == ip_data.to_dict()
        mock_redis_instance.__getitem__.assert_called_once_with(ip_address)
        mock_redis_instance.__setitem__.assert_not_called()
        mock_geoip_instance.__getitem__.assert_not_called()

    @patch("ipinfo_geoip.ipinfo.RedisClient")
    @patch("ipinfo_geoip.ipinfo.GeoIPClient")
    def test_missing_with_geoip_fallback(self, mock_redis_client: Mock, mock_geoip_client: Mock) -> None:
        """GeoIPサービスフォールバックのテスト."""
        # テストデータ
        ip_address = "8.8.8.8"
        ip_data = IPData(
            ip_address=ip_address,
            network="8.8.8.0/24",
            as_number="15169",
            country="US",
            organization="Google LLC",
        )

        # Redisクライアントのモック設定
        mock_redis_instance = Mock()
        mock_redis_instance.__getitem__ = Mock(return_value=None)
        mock_redis_instance.__setitem__ = Mock()
        mock_redis_client.return_value = mock_redis_instance

        # GeoIPクライアントのモック設定
        mock_geoip_instance = Mock()
        mock_geoip_instance.__getitem__ = Mock(return_value=ip_data)
        mock_geoip_client.return_value = mock_geoip_instance

        # IPInfoインスタンス作成
        ipinfo = IPInfo()
        ipinfo.redis = mock_redis_instance
        ipinfo.geoip = mock_geoip_instance

        # テスト実行
        result = ipinfo[ip_address]

        # 検証
        assert result == ip_data.to_dict()
        mock_redis_instance.__getitem__.assert_called_once_with(ip_address)
        mock_redis_instance.__setitem__.assert_called_once_with(ip_address, ip_data)
        mock_geoip_instance.__getitem__.assert_called_once_with(ip_address)

    @patch("ipinfo_geoip.ipinfo.RedisClient")
    @patch("ipinfo_geoip.ipinfo.GeoIPClient")
    def test_missing_with_complete_data_caching(self, mock_redis_client: Mock, mock_geoip_client: Mock) -> None:
        """完全なデータのキャッシュテスト."""
        # 完全なデータのテスト
        ip_address = "8.8.8.8"
        complete_ip_data = IPData(
            ip_address=ip_address,
            network="8.8.8.0/24",
            as_number="15169",
            country="US",
            organization="Google LLC",
        )

        # Redisクライアントのモック設定
        mock_redis_instance = Mock()
        mock_redis_instance.__getitem__ = Mock(return_value=None)
        mock_redis_instance.__setitem__ = Mock()
        mock_redis_client.return_value = mock_redis_instance

        # GeoIPクライアントのモック設定
        mock_geoip_instance = Mock()
        mock_geoip_instance.__getitem__ = Mock(return_value=complete_ip_data)
        mock_geoip_client.return_value = mock_geoip_instance

        # IPInfoインスタンス作成
        ipinfo = IPInfo()
        ipinfo.redis = mock_redis_instance
        ipinfo.geoip = mock_geoip_instance

        # テスト実行
        result = ipinfo[ip_address]

        # 検証
        assert result == complete_ip_data.to_dict()
        # 完全なデータなのでRedisにキャッシュされる
        mock_redis_instance.__getitem__.assert_called_once_with(ip_address)
        mock_redis_instance.__setitem__.assert_called_once_with(ip_address, complete_ip_data)
        mock_geoip_instance.__getitem__.assert_called_once_with(ip_address)

    @patch("ipinfo_geoip.ipinfo.RedisClient")
    @patch("ipinfo_geoip.ipinfo.GeoIPClient")
    def test_missing_with_incomplete_data_no_caching(self, mock_redis_client: Mock, mock_geoip_client: Mock) -> None:
        """不完全なデータのキャッシュなしテスト."""
        # 不完全なデータのテスト
        ip_address = "192.168.1.1"
        incomplete_ip_data = IPData(
            ip_address=ip_address,
            network="",
            as_number="",
            country="",
            organization="",
        )

        # Redisクライアントのモック設定
        mock_redis_instance = Mock()
        mock_redis_instance.__getitem__ = Mock(return_value=None)
        mock_redis_instance.__setitem__ = Mock()
        mock_redis_client.return_value = mock_redis_instance

        # GeoIPクライアントのモック設定
        mock_geoip_instance = Mock()
        mock_geoip_instance.__getitem__ = Mock(return_value=incomplete_ip_data)
        mock_geoip_client.return_value = mock_geoip_instance

        # IPInfoインスタンス作成
        ipinfo = IPInfo()
        ipinfo.redis = mock_redis_instance
        ipinfo.geoip = mock_geoip_instance

        # テスト実行
        result = ipinfo[ip_address]

        # 検証
        assert result == incomplete_ip_data.to_dict()
        # 不完全なデータなのでRedisにキャッシュされない
        mock_redis_instance.__getitem__.assert_called_once_with(ip_address)
        mock_redis_instance.__setitem__.assert_not_called()
        mock_geoip_instance.__getitem__.assert_called_once_with(ip_address)

    @patch("ipinfo_geoip.ipinfo.RedisClient")
    @patch("ipinfo_geoip.ipinfo.GeoIPClient")
    def test_missing_with_none_result(self, mock_redis_client: Mock, mock_geoip_client: Mock) -> None:
        """結果がNoneの場合のテスト."""
        # テストデータ
        ip_address = "invalid.ip"

        # Redisクライアントのモック設定
        mock_redis_instance = Mock()
        mock_redis_instance.__getitem__ = Mock(return_value=None)
        mock_redis_instance.__setitem__ = Mock()
        mock_redis_client.return_value = mock_redis_instance

        # GeoIPクライアントのモック設定
        mock_geoip_instance = Mock()
        mock_geoip_instance.__getitem__ = Mock(return_value=None)
        mock_geoip_client.return_value = mock_geoip_instance

        # IPInfoインスタンス作成
        ipinfo = IPInfo()
        ipinfo.redis = mock_redis_instance
        ipinfo.geoip = mock_geoip_instance

        # テスト実行
        result = ipinfo[ip_address]

        # 検証
        assert result is None
        mock_redis_instance.__getitem__.assert_called_once_with(ip_address)
        mock_redis_instance.__setitem__.assert_not_called()
        mock_geoip_instance.__getitem__.assert_called_once_with(ip_address)

    @patch("ipinfo_geoip.ipinfo.RedisClient")
    @patch("ipinfo_geoip.ipinfo.GeoIPClient")
    def test_missing_with_invalid_ip_type(self, mock_geoip_client: Mock, mock_redis_client: Mock) -> None:
        """無効なIPアドレス型のテスト."""
        del mock_geoip_client, mock_redis_client
        ipinfo = IPInfo()

        with pytest.raises(TypeError):
            _ = ipinfo[123]  # type: ignore[index]
