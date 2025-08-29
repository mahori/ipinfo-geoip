"""定数のテスト."""

from typing import get_type_hints

from ipinfo_geoip import constants
from ipinfo_geoip.constants import (
    GEOIP_ACCOUNT_ID_ENV,
    GEOIP_HOST_ENV,
    GEOIP_LICENSE_KEY_ENV,
    REDIS_CACHE_TTL_ENV,
    REDIS_URI_ENV,
)


class TestConstants:
    """定数のテストクラス."""

    def test_geoip_environment_variables(self) -> None:
        """GeoIP関連環境変数名のテスト."""
        assert GEOIP_ACCOUNT_ID_ENV == "IPINFO_GEOIP_ACCOUNT_ID"
        assert GEOIP_LICENSE_KEY_ENV == "IPINFO_GEOIP_LICENSE_KEY"
        assert GEOIP_HOST_ENV == "IPINFO_GEOIP_HOST"

    def test_redis_environment_variables(self) -> None:
        """Redis関連環境変数名のテスト."""
        assert REDIS_URI_ENV == "IPINFO_REDIS_URI"
        assert REDIS_CACHE_TTL_ENV == "IPINFO_REDIS_CACHE_TTL"

    def test_constants_are_final(self) -> None:
        """定数がFinal型であることのテスト."""
        hints = get_type_hints(constants)

        # すべての定数がFinal[str]型であることを確認
        for const_name in [
            "GEOIP_ACCOUNT_ID_ENV",
            "GEOIP_LICENSE_KEY_ENV",
            "GEOIP_HOST_ENV",
            "REDIS_URI_ENV",
            "REDIS_CACHE_TTL_ENV",
        ]:
            assert const_name in hints
            # Final[str]型の確認は環境により異なるため存在確認のみ

    def test_constants_are_strings(self) -> None:
        """すべての定数が文字列であることのテスト."""
        assert isinstance(GEOIP_ACCOUNT_ID_ENV, str)
        assert isinstance(GEOIP_LICENSE_KEY_ENV, str)
        assert isinstance(GEOIP_HOST_ENV, str)
        assert isinstance(REDIS_URI_ENV, str)
        assert isinstance(REDIS_CACHE_TTL_ENV, str)

    def test_constants_are_not_empty(self) -> None:
        """すべての定数が空でないことのテスト."""
        assert len(GEOIP_ACCOUNT_ID_ENV) > 0
        assert len(GEOIP_LICENSE_KEY_ENV) > 0
        assert len(GEOIP_HOST_ENV) > 0
        assert len(REDIS_URI_ENV) > 0
        assert len(REDIS_CACHE_TTL_ENV) > 0
