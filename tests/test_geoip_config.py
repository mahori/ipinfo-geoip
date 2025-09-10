"""GeoIPConfigクラスのテスト."""

import os
from unittest.mock import patch

import pytest

from ipinfo_geoip.exceptions import ValidationError
from ipinfo_geoip.geoip_config import GeoIPConfig


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
