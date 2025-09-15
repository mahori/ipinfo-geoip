"""IPInfoクラスのテスト."""

from collections import UserDict
from typing import Final
from unittest.mock import Mock, patch

import pytest

from ipinfo_geoip.exceptions import ValidationError
from ipinfo_geoip.ipdata import IPData
from ipinfo_geoip.ipinfo import IPInfo

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


class TestIPInfo:
    """IPInfoクラスのテストクラス."""

    @patch("ipinfo_geoip.ipinfo.RedisClient")
    @patch("ipinfo_geoip.ipinfo.GeoIPClient")
    def test_init(self, mock_geoip_client: Mock, mock_redis_client: Mock) -> None:
        """初期化のテスト."""
        # テスト実行
        ipinfo = IPInfo()

        # 検証
        assert isinstance(ipinfo, IPInfo)
        assert isinstance(ipinfo, UserDict)
        mock_geoip_client.assert_called_once()
        mock_redis_client.assert_called_once()

    @patch("ipinfo_geoip.ipinfo.RedisClient")
    @patch("ipinfo_geoip.ipinfo.GeoIPClient")
    def test_missing_with_invalid_ip_value(self, mock_geoip_client: Mock, mock_redis_client: Mock) -> None:
        """IPアドレスが無効な場合の__missing__メソッドテスト."""
        # モック設定
        mock_geoip_instance = Mock()
        mock_geoip_instance.__getitem__ = Mock(return_value=None)
        mock_geoip_client.return_value = mock_geoip_instance

        mock_redis_instance = Mock()
        mock_redis_instance.__getitem__ = Mock(return_value=TEST_IPDATA)
        mock_redis_instance.__setitem__ = Mock()
        mock_redis_client.return_value = mock_redis_instance

        # テスト実行
        ipinfo = IPInfo()

        with pytest.raises(ValidationError):
            _ = ipinfo["invalid.ip"]

        # 検証
        mock_geoip_instance.__getitem__.assert_not_called()
        mock_redis_instance.__getitem__.assert_not_called()
        mock_redis_instance.__setitem__.assert_not_called()

    @patch("ipinfo_geoip.ipinfo.RedisClient")
    @patch("ipinfo_geoip.ipinfo.GeoIPClient")
    def test_missing_from_geoip(self, mock_geoip_client: Mock, mock_redis_client: Mock) -> None:
        """GeoIPインスタンスからIPアドレス情報を取得する__missing__メソッドテスト."""
        # モック設定
        mock_geoip_instance = Mock()
        mock_geoip_instance.__getitem__ = Mock(return_value=TEST_IPDATA)
        mock_geoip_client.return_value = mock_geoip_instance

        mock_redis_instance = Mock()
        mock_redis_instance.__getitem__ = Mock(return_value=None)
        mock_redis_instance.__setitem__ = Mock()
        mock_redis_client.return_value = mock_redis_instance

        # テスト実行
        ipinfo = IPInfo()
        result = ipinfo[TEST_IP_ADDRESS]

        # 検証
        assert result == TEST_IPDATA.to_dict()
        mock_geoip_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS)
        mock_redis_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS)
        mock_redis_instance.__setitem__.assert_called_once_with(TEST_IP_ADDRESS, TEST_IPDATA)

    @patch("ipinfo_geoip.ipinfo.RedisClient")
    @patch("ipinfo_geoip.ipinfo.GeoIPClient")
    def test_missing_from_redis(self, mock_geoip_client: Mock, mock_redis_client: Mock) -> None:
        """RedisインスタンスからIPアドレス情報を取得する__missing__メソッドテスト."""
        # モック設定
        mock_geoip_instance = Mock()
        mock_geoip_instance.__getitem__ = Mock(return_value=None)
        mock_geoip_client.return_value = mock_geoip_instance

        mock_redis_instance = Mock()
        mock_redis_instance.__getitem__ = Mock(return_value=TEST_IPDATA)
        mock_redis_instance.__setitem__ = Mock()
        mock_redis_client.return_value = mock_redis_instance

        # テスト実行
        ipinfo = IPInfo()
        result = ipinfo[TEST_IP_ADDRESS]

        # 検証
        assert result == TEST_IPDATA.to_dict()
        mock_geoip_instance.__getitem__.assert_not_called()
        mock_redis_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS)
        mock_redis_instance.__setitem__.assert_not_called()

    @patch("ipinfo_geoip.ipinfo.RedisClient")
    @patch("ipinfo_geoip.ipinfo.GeoIPClient")
    def test_missing_with_complete_data(self, mock_geoip_client: Mock, mock_redis_client: Mock) -> None:
        """データが完全な場合の__missing__メソッドテスト."""
        # モック設定
        mock_geoip_instance = Mock()
        mock_geoip_instance.__getitem__ = Mock(return_value=TEST_IPDATA)
        mock_geoip_client.return_value = mock_geoip_instance

        # Redisクライアントのモック設定
        mock_redis_instance = Mock()
        mock_redis_instance.__getitem__ = Mock(return_value=None)
        mock_redis_instance.__setitem__ = Mock()
        mock_redis_client.return_value = mock_redis_instance

        # テスト実行
        ipinfo = IPInfo()
        result = ipinfo[TEST_IP_ADDRESS]

        # 検証
        assert result == TEST_IPDATA.to_dict()
        mock_geoip_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS)
        mock_redis_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS)
        mock_redis_instance.__setitem__.assert_called_once_with(TEST_IP_ADDRESS, TEST_IPDATA)

    @patch("ipinfo_geoip.ipinfo.RedisClient")
    @patch("ipinfo_geoip.ipinfo.GeoIPClient")
    def test_missing_with_incomplete_data(self, mock_geoip_client: Mock, mock_redis_client: Mock) -> None:
        """データが不完全な場合の__missing__メソッドテスト."""
        # モック設定
        mock_geoip_instance = Mock()
        mock_geoip_instance.__getitem__ = Mock(return_value=TEST_IPDATA_INCOMPLETE)
        mock_geoip_client.return_value = mock_geoip_instance

        mock_redis_instance = Mock()
        mock_redis_instance.__getitem__ = Mock(return_value=None)
        mock_redis_instance.__setitem__ = Mock()
        mock_redis_client.return_value = mock_redis_instance

        # テスト実行
        ipinfo = IPInfo()
        result = ipinfo[TEST_IP_ADDRESS]

        # 検証
        assert result == TEST_IPDATA_INCOMPLETE.to_dict()
        mock_geoip_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS)
        mock_redis_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS)
        mock_redis_instance.__setitem__.assert_not_called()

    @patch("ipinfo_geoip.ipinfo.RedisClient")
    @patch("ipinfo_geoip.ipinfo.GeoIPClient")
    def test_missing_with_none_data(self, mock_geoip_client: Mock, mock_redis_client: Mock) -> None:
        """データがNoneの場合の__missing__メソッドテスト."""
        # モック設定
        mock_geoip_instance = Mock()
        mock_geoip_instance.__getitem__ = Mock(return_value=None)
        mock_geoip_client.return_value = mock_geoip_instance

        mock_redis_instance = Mock()
        mock_redis_instance.__getitem__ = Mock(return_value=None)
        mock_redis_instance.__setitem__ = Mock()
        mock_redis_client.return_value = mock_redis_instance

        # テスト実行
        ipinfo = IPInfo()
        result = ipinfo[TEST_IP_ADDRESS]

        # 検証
        assert result is None
        mock_geoip_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS)
        mock_redis_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS)
        mock_redis_instance.__setitem__.assert_not_called()
