"""GeoIPClientクラスのテスト."""

from collections import UserDict
from ipaddress import IPv4Network
from unittest.mock import Mock, patch

import geoip2.errors
import pytest

from ipinfo_geoip.exceptions import ConfigurationError, GeoIPClientError, ValidationError
from ipinfo_geoip.geoip_client import GeoIPClient
from ipinfo_geoip.ipdata import IPData


class TestGeoIPClient:
    """GeoIPClientクラスのテストクラス."""

    @patch("ipinfo_geoip.geoip_client.geoip2.webservice.Client")
    @patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env")
    def test_init(self, mock_from_env: Mock, mock_client: Mock) -> None:
        """初期化のテスト."""
        # モック設定
        mock_config = Mock()
        expected_id = 12345
        mock_config.account_id = expected_id
        mock_config.license_key = "test_key"
        mock_config.host = "geoip.maxmind.com"
        mock_from_env.return_value = mock_config

        # テスト実行
        client = GeoIPClient()

        # 検証
        mock_from_env.assert_called_once()
        mock_client.assert_called_once_with(expected_id, "test_key", "geoip.maxmind.com")
        assert isinstance(client, UserDict)

    @patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env")
    def test_init_with_configuration_error(self, mock_from_env: Mock) -> None:
        """設定エラーでの初期化テスト."""
        mock_from_env.side_effect = ValidationError("Missing environment variable")

        with pytest.raises(ConfigurationError):
            _ = GeoIPClient()

    @patch("ipinfo_geoip.geoip_client.geoip2.webservice.Client")
    @patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env")
    def test_missing_success(self, mock_from_env: Mock, mock_client: Mock) -> None:
        """成功時の__missing__メソッドテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_response = Mock()
        mock_response.traits.network = IPv4Network("8.8.8.0/24")
        mock_response.traits.autonomous_system_number = 15169
        mock_response.country.iso_code = "US"
        mock_response.traits.autonomous_system_organization = "GOOGLE"

        mock_client_instance = Mock()
        mock_client_instance.city.return_value = mock_response
        mock_client.return_value = mock_client_instance

        # テスト実行
        client = GeoIPClient()
        result = client["8.8.8.8"]

        # 検証
        assert isinstance(result, IPData)
        assert result.ip_address == "8.8.8.8"
        assert result.network == "8.8.8.0/24"
        assert result.as_number == "15169"
        assert result.country == "US"
        assert result.organization == "GOOGLE"
        mock_client_instance.city.assert_called_once_with("8.8.8.8")

    @patch("ipinfo_geoip.geoip_client.geoip2.webservice.Client")
    @patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env")
    def test_missing_with_address_not_found(self, mock_from_env: Mock, mock_client: Mock) -> None:
        """アドレスが見つからない場合のテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_client_instance = Mock()
        mock_client_instance.city.side_effect = geoip2.errors.AddressNotFoundError("Address not found")
        mock_client.return_value = mock_client_instance

        # テスト実行
        client = GeoIPClient()

        with pytest.raises(GeoIPClientError):
            _ = client["192.168.1.1"]

    @patch("ipinfo_geoip.geoip_client.geoip2.webservice.Client")
    @patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env")
    def test_missing_with_none_response(self, mock_from_env: Mock, mock_client: Mock) -> None:
        """レスポンスがNoneの場合のテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_client_instance = Mock()
        mock_client_instance.city.return_value = None
        mock_client.return_value = mock_client_instance

        # テスト実行
        client = GeoIPClient()
        result = client["8.8.8.8"]

        # 検証
        assert result is None

    def test_missing_with_invalid_ip_type(self) -> None:
        """無効なIPアドレス型のテスト."""
        with patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env"):
            client = GeoIPClient()

            with pytest.raises(TypeError):
                _ = client[123]  # type: ignore[index]

    def test_missing_with_invalid_ip_value(self) -> None:
        """無効なIPアドレス値のテスト."""
        with patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env"):
            client = GeoIPClient()

            with pytest.raises(ValidationError):
                _ = client["invalid.ip"]

    @patch("ipinfo_geoip.geoip_client.geoip2.webservice.Client")
    @patch("ipinfo_geoip.geoip_client.GeoIPConfig.from_env")
    def test_missing_with_partial_data(self, mock_from_env: Mock, mock_client: Mock) -> None:
        """部分的なデータでのテスト."""
        # モック設定
        mock_config = Mock()
        mock_from_env.return_value = mock_config

        mock_response = Mock()
        mock_response.traits.network = None
        mock_response.traits.autonomous_system_number = None
        mock_response.country.iso_code = "US"
        mock_response.traits.autonomous_system_organization = "GOOGLE"

        mock_client_instance = Mock()
        mock_client_instance.city.return_value = mock_response
        mock_client.return_value = mock_client_instance

        # テスト実行
        client = GeoIPClient()
        result = client["8.8.8.8"]

        # 検証
        assert result is None
