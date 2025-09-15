"""GeoIPClientクラスのテスト."""

from collections import UserDict
from ipaddress import IPv4Network
from unittest.mock import Mock, patch

import geoip2.errors
import pytest

from ipinfo_geoip.exceptions import ConfigurationError, GeoIPClientError, ValidationError
from ipinfo_geoip.geoip_client import GeoIPClient
from ipinfo_geoip.ipdata import IPData
from tests.conftest import (
    TEST_AS_NUMBER_INT,
    TEST_AS_NUMBER_STR,
    TEST_COUNTRY_CODE,
    TEST_GEOIP_ACCOUNT_ID_INT,
    TEST_GEOIP_HOST,
    TEST_GEOIP_LICENSE_KEY,
    TEST_IP_ADDRESS_1,
    TEST_IP_NETWORK,
    TEST_IPADDRESS_INVALID_,
    TEST_ORGANIZATION,
)


class TestGeoIPClient:
    """GeoIPClientクラスのテストクラス."""

    @patch("ipinfo_geoip.geoip_client.geoip2.webservice.Client")
    @patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env")
    def test_init(self, mock_from_env: Mock, mock_client: Mock) -> None:
        """初期化のテスト."""
        # モック設定
        mock_config = Mock()
        mock_config.account_id = TEST_GEOIP_ACCOUNT_ID_INT
        mock_config.license_key = TEST_GEOIP_LICENSE_KEY
        mock_config.host = TEST_GEOIP_HOST
        mock_from_env.return_value = mock_config

        # テスト実行
        client = GeoIPClient()

        # 検証
        assert isinstance(client, GeoIPClient)
        assert isinstance(client, UserDict)
        mock_from_env.assert_called_once()
        mock_client.assert_called_once_with(TEST_GEOIP_ACCOUNT_ID_INT, TEST_GEOIP_LICENSE_KEY, TEST_GEOIP_HOST)

    @patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env")
    def test_init_with_configuration_error(self, mock_from_env: Mock) -> None:
        """設定エラーでの初期化テスト."""
        # モック設定
        mock_from_env.side_effect = ValidationError("Missing environment variables")

        # テスト実行
        with pytest.raises(ConfigurationError):
            _ = GeoIPClient()

        # 検証
        mock_from_env.assert_called_once()

    @patch("ipinfo_geoip.geoip_client.geoip2.webservice.Client")
    @patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env")
    def test_missing_with_invalid_ip_value(self, mock_from_env: Mock, mock_client: Mock) -> None:
        """IPアドレスが無効な場合の__missing__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_client_instance = Mock()
        mock_client_instance.city.return_value = None
        mock_client.return_value = mock_client_instance

        # テスト実行
        client = GeoIPClient()

        with pytest.raises(ValidationError):
            _ = client[TEST_IPADDRESS_INVALID_]

        # 検証
        mock_client_instance.city.assert_not_called()

    @patch("ipinfo_geoip.geoip_client.geoip2.webservice.Client")
    @patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env")
    def test_missing_success(self, mock_from_env: Mock, mock_client: Mock) -> None:
        """成功時の__missing__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_response = Mock()
        mock_response.traits.network = IPv4Network(TEST_IP_NETWORK)
        mock_response.traits.autonomous_system_number = TEST_AS_NUMBER_INT
        mock_response.country.iso_code = TEST_COUNTRY_CODE
        mock_response.traits.autonomous_system_organization = TEST_ORGANIZATION

        mock_client_instance = Mock()
        mock_client_instance.city.return_value = mock_response
        mock_client.return_value = mock_client_instance

        # テスト実行
        client = GeoIPClient()
        result = client[TEST_IP_ADDRESS_1]

        # 検証
        assert isinstance(result, IPData)
        assert result.ip_address == TEST_IP_ADDRESS_1
        assert result.network == TEST_IP_NETWORK
        assert result.as_number == TEST_AS_NUMBER_STR
        assert result.country == TEST_COUNTRY_CODE
        assert result.organization == TEST_ORGANIZATION
        mock_client_instance.city.assert_called_once_with(TEST_IP_ADDRESS_1)

    @patch("ipinfo_geoip.geoip_client.geoip2.webservice.Client")
    @patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env")
    def test_missing_with_address_not_found(self, mock_from_env: Mock, mock_client: Mock) -> None:
        """アドレスが見つからない場合の__missing__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_client_instance = Mock()
        mock_client_instance.city.side_effect = geoip2.errors.AddressNotFoundError("Address not found")
        mock_client.return_value = mock_client_instance

        # テスト実行
        client = GeoIPClient()

        with pytest.raises(GeoIPClientError):
            _ = client[TEST_IP_ADDRESS_1]

        # 検証
        mock_client_instance.city.assert_called_once_with(TEST_IP_ADDRESS_1)

    @patch("ipinfo_geoip.geoip_client.geoip2.webservice.Client")
    @patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env")
    def test_missing_with_none_response(self, mock_from_env: Mock, mock_client: Mock) -> None:
        """レスポンスがNoneの場合の__missing__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_client_instance = Mock()
        mock_client_instance.city.return_value = None
        mock_client.return_value = mock_client_instance

        # テスト実行
        client = GeoIPClient()
        result = client[TEST_IP_ADDRESS_1]

        # 検証
        assert result is None
        mock_client_instance.city.assert_called_once_with(TEST_IP_ADDRESS_1)

    @patch("ipinfo_geoip.geoip_client.geoip2.webservice.Client")
    @patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env")
    def test_missing_with_partial_data(self, mock_from_env: Mock, mock_client: Mock) -> None:
        """データが不完全な場合の__missing__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_response = Mock()
        mock_response.traits.network = None
        mock_response.traits.autonomous_system_number = None
        mock_response.country.iso_code = TEST_COUNTRY_CODE
        mock_response.traits.autonomous_system_organization = TEST_ORGANIZATION

        mock_client_instance = Mock()
        mock_client_instance.city.return_value = mock_response
        mock_client.return_value = mock_client_instance

        # テスト実行
        client = GeoIPClient()
        result = client[TEST_IP_ADDRESS_1]

        # 検証
        assert result is None
        mock_client_instance.city.assert_called_once_with(TEST_IP_ADDRESS_1)
