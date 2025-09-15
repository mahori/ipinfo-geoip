"""IPInfoクラスのテスト."""

from collections import UserDict
from unittest.mock import Mock, patch

import pytest

from ipinfo_geoip.exceptions import ValidationError
from ipinfo_geoip.ipinfo import IPInfo
from tests.conftest import TEST_IP_ADDRESS_1, TEST_IPDATA, TEST_IPDATA_INCOMPLETE


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
        result = ipinfo[TEST_IP_ADDRESS_1]

        # 検証
        assert result == TEST_IPDATA.to_dict()
        mock_geoip_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS_1)
        mock_redis_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS_1)
        mock_redis_instance.__setitem__.assert_called_once_with(TEST_IP_ADDRESS_1, TEST_IPDATA)

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
        result = ipinfo[TEST_IP_ADDRESS_1]

        # 検証
        assert result == TEST_IPDATA.to_dict()
        mock_geoip_instance.__getitem__.assert_not_called()
        mock_redis_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS_1)
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
        result = ipinfo[TEST_IP_ADDRESS_1]

        # 検証
        assert result == TEST_IPDATA.to_dict()
        mock_geoip_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS_1)
        mock_redis_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS_1)
        mock_redis_instance.__setitem__.assert_called_once_with(TEST_IP_ADDRESS_1, TEST_IPDATA)

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
        result = ipinfo[TEST_IP_ADDRESS_1]

        # 検証
        assert result == TEST_IPDATA_INCOMPLETE.to_dict()
        mock_geoip_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS_1)
        mock_redis_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS_1)
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
        result = ipinfo[TEST_IP_ADDRESS_1]

        # 検証
        assert result is None
        mock_geoip_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS_1)
        mock_redis_instance.__getitem__.assert_called_once_with(TEST_IP_ADDRESS_1)
        mock_redis_instance.__setitem__.assert_not_called()
