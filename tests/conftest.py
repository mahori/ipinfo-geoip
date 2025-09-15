"""テスト用定数."""

from typing import Any, Final

from ipinfo_geoip.ipdata import IPData

TEST_EXCEPTION_MESSAGE: Final[str] = "テストエラー"
TEST_EXCEPTION_DETAILS: Final[dict[str, Any]] = {"ip_address": "192.0.2.1", "code": 500}

TEST_GEOIP_ACCOUNT_ID_INT: Final[int] = 12345
TEST_GEOIP_ACCOUNT_ID_STR: Final[str] = "12345"
TEST_GEOIP_LICENSE_KEY: Final[str] = "license_key"
TEST_GEOIP_HOST: Final[str] = "geolite.info"

TEST_REDIS_URI: Final[str] = "redis://localhost:6379"
TEST_REDIS_TTL_INT: Final[int] = 3600
TEST_REDIS_TTL_STR: Final[str] = "3600"

TEST_IP_ADDRESS_1: Final[str] = "192.0.2.1"
TEST_IP_ADDRESS_2: Final[str] = "192.0.2.2"
TEST_IP_NETWORK: Final[str] = "192.0.2.0/24"
TEST_AS_NUMBER_INT: Final[int] = 65001
TEST_AS_NUMBER_STR: Final[str] = "65001"
TEST_COUNTRY_CODE: Final[str] = "US"
TEST_ORGANIZATION: Final[str] = "Test Organization"
TEST_IPADDRESS_INVALID_: Final[str] = "invalid.ip"

TEST_IPDATA: Final[IPData] = IPData(
    ip_address=TEST_IP_ADDRESS_1,
    network=TEST_IP_NETWORK,
    as_number=TEST_AS_NUMBER_STR,
    country=TEST_COUNTRY_CODE,
    organization=TEST_ORGANIZATION,
)
TEST_IPDATA_INCOMPLETE: Final[IPData] = IPData(
    ip_address=TEST_IP_ADDRESS_1,
    as_number=TEST_AS_NUMBER_STR,
    network="",
    country=TEST_COUNTRY_CODE,
    organization=TEST_ORGANIZATION,
)
