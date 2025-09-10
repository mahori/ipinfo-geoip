"""GeoIPClientクラスのテスト."""

import os
from collections import UserDict
from ipaddress import IPv4Network, IPv6Network
from unittest.mock import Mock, patch

import geoip2.errors
import pytest

from ipinfo_geoip.exceptions import ConfigurationError, GeoIPClientError, ValidationError
from ipinfo_geoip.geoip_client import GeoIPClient, GeoIPConfig, _to_str
from ipinfo_geoip.ipdata import IPData


class TestToStr:
    """_to_str関数のテストクラス."""

    def test_to_str_with_none(self) -> None:
        """Noneの場合のテスト."""
        assert _to_str(None) == ""

    def test_to_str_with_str(self) -> None:
        """文字列の場合のテスト."""
        assert _to_str("hello") == "hello"
        assert _to_str("") == ""

    def test_to_str_with_int(self) -> None:
        """整数の場合のテスト."""
        assert _to_str(42) == "42"
        assert _to_str(0) == "0"
        assert _to_str(-1) == "-1"

    def test_to_str_with_ipv4_network(self) -> None:
        """IPv4Networkの場合のテスト."""
        network = IPv4Network("192.168.1.0/24")
        assert _to_str(network) == "192.168.1.0/24"

    def test_to_str_with_ipv6_network(self) -> None:
        """IPv6Networkの場合のテスト."""
        network = IPv6Network("2001:db8::/32")
        assert _to_str(network) == "2001:db8::/32"

    def test_to_str_with_bool(self) -> None:
        """ブール値の場合のテスト."""
        with pytest.raises(TypeError):
            _to_str(bool(1))
        with pytest.raises(TypeError):
            _to_str(bool(0))

    def test_to_str_with_unsupported_type(self) -> None:
        """サポートされていない型の場合のテスト."""
        with pytest.raises(TypeError):
            _to_str(3.14)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            _to_str([1, 2, 3])  # type: ignore[arg-type]


class TestGeoIPConfig:
    """GeoIPConfigクラスのテストクラス."""

    def test_init(self) -> None:
        """初期化のテスト."""
        config = GeoIPConfig("12345", "license_key", "geoip.maxmind.com")

        expected_id = 12345
        assert config.account_id == expected_id
        assert config.license_key == "license_key"
        assert config.host == "geoip.maxmind.com"

    def test_init_with_invalid_account_id_type(self) -> None:
        """無効なアカウントID型のテスト."""
        with pytest.raises(TypeError):
            GeoIPConfig(12345, "license_key", "host")  # type: ignore[arg-type]

    def test_init_with_invalid_license_key_type(self) -> None:
        """無効なライセンスキー型のテスト."""
        with pytest.raises(TypeError):
            GeoIPConfig("12345", 123, "host")  # type: ignore[arg-type]

    def test_init_with_invalid_host_type(self) -> None:
        """無効なホスト型のテスト."""
        with pytest.raises(TypeError):
            GeoIPConfig("12345", "license_key", 123)  # type: ignore[arg-type]

    @patch.dict(
        os.environ,
        {
            "IPINFO_GEOIP_ACCOUNT_ID": "12345",
            "IPINFO_GEOIP_LICENSE_KEY": "test_key",
            "IPINFO_GEOIP_HOST": "geoip.maxmind.com",
        },
        clear=True,
    )
    def test_from_env(self) -> None:
        """環境変数からの作成テスト."""
        config = GeoIPConfig.from_env()

        expected_id = 12345
        assert config.account_id == expected_id
        assert config.license_key == "test_key"
        assert config.host == "geoip.maxmind.com"

    @patch.dict(
        os.environ,
        {
            "IPINFO_GEOIP_LICENSE_KEY": "test_key",
            "IPINFO_GEOIP_HOST": "geoip.maxmind.com",
        },
        clear=True,
    )
    def test_from_env_missing_account_id(self) -> None:
        """アカウントID環境変数不足のテスト."""
        with pytest.raises(ValidationError):
            GeoIPConfig.from_env()

    @patch.dict(
        os.environ,
        {
            "IPINFO_GEOIP_ACCOUNT_ID": "12345",
            "IPINFO_GEOIP_HOST": "geoip.maxmind.com",
        },
        clear=True,
    )
    def test_from_env_missing_license_key(self) -> None:
        """ライセンスキー環境変数不足のテスト."""
        with pytest.raises(ValidationError):
            GeoIPConfig.from_env()

    @patch.dict(
        os.environ,
        {
            "IPINFO_GEOIP_ACCOUNT_ID": "12345",
            "IPINFO_GEOIP_LICENSE_KEY": "test_key",
        },
        clear=True,
    )
    def test_from_env_missing_host(self) -> None:
        """ホスト環境変数不足のテスト."""
        with pytest.raises(ValidationError):
            GeoIPConfig.from_env()


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
            GeoIPClient()

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
        mock_response.traits.autonomous_system_organization = "Google LLC"

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
        assert result.organization == "Google LLC"
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
            client["192.168.1.1"]

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
        mock_response.traits.autonomous_system_organization = "Google LLC"

        mock_client_instance = Mock()
        mock_client_instance.city.return_value = mock_response
        mock_client.return_value = mock_client_instance

        # テスト実行
        client = GeoIPClient()
        result = client["8.8.8.8"]

        # 検証
        assert isinstance(result, IPData)
        assert result.network == ""
        assert result.as_number == ""
