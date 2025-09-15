"""GeoIPConfigクラスのテスト."""

import os
from unittest.mock import patch

import pytest

from ipinfo_geoip.constants import GEOIP_ACCOUNT_ID_ENV, GEOIP_HOST_ENV, GEOIP_LICENSE_KEY_ENV
from ipinfo_geoip.exceptions import ValidationError
from ipinfo_geoip.geoip_config import GeoIPConfig
from tests.conftest import TEST_GEOIP_ACCOUNT_ID_INT, TEST_GEOIP_ACCOUNT_ID_STR, TEST_GEOIP_HOST, TEST_GEOIP_LICENSE_KEY


class TestGeoIPConfig:
    """GeoIPConfigクラスのテストクラス."""

    def test_init(self) -> None:
        """初期化のテスト."""
        config = GeoIPConfig(TEST_GEOIP_ACCOUNT_ID_STR, TEST_GEOIP_LICENSE_KEY, TEST_GEOIP_HOST)

        assert config.account_id == TEST_GEOIP_ACCOUNT_ID_INT
        assert config.license_key == TEST_GEOIP_LICENSE_KEY
        assert config.host == TEST_GEOIP_HOST

    @patch.dict(
        os.environ,
        {
            GEOIP_ACCOUNT_ID_ENV: TEST_GEOIP_ACCOUNT_ID_STR,
            GEOIP_LICENSE_KEY_ENV: TEST_GEOIP_LICENSE_KEY,
            GEOIP_HOST_ENV: TEST_GEOIP_HOST,
        },
        clear=True,
    )
    def test_from_env(self) -> None:
        """環境変数からの作成テスト."""
        config = GeoIPConfig.from_env()

        assert config.account_id == TEST_GEOIP_ACCOUNT_ID_INT
        assert config.license_key == TEST_GEOIP_LICENSE_KEY
        assert config.host == TEST_GEOIP_HOST

    @patch.dict(
        os.environ,
        {
            GEOIP_LICENSE_KEY_ENV: TEST_GEOIP_LICENSE_KEY,
            GEOIP_HOST_ENV: TEST_GEOIP_HOST,
        },
        clear=True,
    )
    def test_from_env_missing_account_id(self) -> None:
        """アカウントID環境変数不足のテスト."""
        match = f"Missing environment variables: {GEOIP_ACCOUNT_ID_ENV}"
        with pytest.raises(ValidationError, match=match):
            _ = GeoIPConfig.from_env()

    @patch.dict(
        os.environ,
        {
            GEOIP_ACCOUNT_ID_ENV: TEST_GEOIP_ACCOUNT_ID_STR,
            GEOIP_HOST_ENV: TEST_GEOIP_HOST,
        },
        clear=True,
    )
    def test_from_env_missing_license_key(self) -> None:
        """ライセンスキー環境変数不足のテスト."""
        match = f"Missing environment variables: {GEOIP_LICENSE_KEY_ENV}"
        with pytest.raises(ValidationError, match=match):
            _ = GeoIPConfig.from_env()

    @patch.dict(
        os.environ,
        {
            GEOIP_ACCOUNT_ID_ENV: TEST_GEOIP_ACCOUNT_ID_STR,
            GEOIP_LICENSE_KEY_ENV: TEST_GEOIP_LICENSE_KEY,
        },
        clear=True,
    )
    def test_from_env_missing_host(self) -> None:
        """ホスト環境変数不足のテスト."""
        match = f"Missing environment variables: {GEOIP_HOST_ENV}"
        with pytest.raises(ValidationError, match=match):
            _ = GeoIPConfig.from_env()

    @patch.dict(
        os.environ,
        {},
        clear=True,
    )
    def test_from_env_missing_environment_variables(self) -> None:
        """複数の環境変数不足のテスト."""
        match = f"Missing environment variables: {GEOIP_ACCOUNT_ID_ENV}, {GEOIP_LICENSE_KEY_ENV}, {GEOIP_HOST_ENV}"
        with pytest.raises(ValidationError, match=match):
            _ = GeoIPConfig.from_env()
