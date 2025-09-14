"""IPDataクラスのテスト."""

from typing import Final

import pytest

from ipinfo_geoip.constants import AS_NUMBER_MAX, AS_NUMBER_MIN, COUNTRY_CODE_LENGTH
from ipinfo_geoip.exceptions import ValidationError
from ipinfo_geoip.ipdata import IPData

TEST_IP_ADDRESS_1: Final[str] = "192.0.2.1"
TEST_IP_ADDRESS_2: Final[str] = "192.0.2.2"
TEST_IP_NETWORK: Final[str] = "192.0.2.0/24"
TEST_AS_NUMBER: Final[str] = "65001"
TEST_COUNTRY_CODE: Final[str] = "US"
TEST_ORGANIZATION: Final[str] = "Test Organization"


class TestIPData:
    """IPDataクラスのテストクラス."""

    def test_init(self) -> None:
        """IPDataクラスの初期化テスト."""
        ip_data = IPData(
            ip_address=TEST_IP_ADDRESS_1,
            network=TEST_IP_NETWORK,
            as_number=TEST_AS_NUMBER,
            country=TEST_COUNTRY_CODE,
            organization=TEST_ORGANIZATION,
        )

        assert ip_data.ip_address == TEST_IP_ADDRESS_1
        assert ip_data.network == TEST_IP_NETWORK
        assert ip_data.as_number == TEST_AS_NUMBER
        assert ip_data.country == TEST_COUNTRY_CODE
        assert ip_data.organization == TEST_ORGANIZATION

    def test_dataclass_equality(self) -> None:
        """IPDataクラスの等価性テスト."""
        ip_data1 = IPData(
            ip_address=TEST_IP_ADDRESS_1,
            network=TEST_IP_NETWORK,
            as_number=TEST_AS_NUMBER,
            country=TEST_COUNTRY_CODE,
            organization=TEST_ORGANIZATION,
        )

        ip_data2 = IPData(
            ip_address=TEST_IP_ADDRESS_1,
            network=TEST_IP_NETWORK,
            as_number=TEST_AS_NUMBER,
            country=TEST_COUNTRY_CODE,
            organization=TEST_ORGANIZATION,
        )

        assert ip_data1 == ip_data2

    def test_dataclass_inequality(self) -> None:
        """IPDataクラスの非等価性テスト."""
        ip_data1 = IPData(
            ip_address=TEST_IP_ADDRESS_1,
            network=TEST_IP_NETWORK,
            as_number=TEST_AS_NUMBER,
            country=TEST_COUNTRY_CODE,
            organization=TEST_ORGANIZATION,
        )

        ip_data2 = IPData(
            ip_address=TEST_IP_ADDRESS_2,
            network=TEST_IP_NETWORK,
            as_number=TEST_AS_NUMBER,
            country=TEST_COUNTRY_CODE,
            organization=TEST_ORGANIZATION,
        )

        assert ip_data1 != ip_data2

    def test_dataclass_repr(self) -> None:
        """IPDataクラスの文字列表現テスト."""
        ip_data = IPData(
            ip_address=TEST_IP_ADDRESS_1,
            network=TEST_IP_NETWORK,
            as_number=TEST_AS_NUMBER,
            country=TEST_COUNTRY_CODE,
            organization=TEST_ORGANIZATION,
        )

        repr_str = repr(ip_data)

        assert "IPData" in repr_str
        assert TEST_IP_ADDRESS_1 in repr_str
        assert TEST_IP_NETWORK in repr_str
        assert TEST_AS_NUMBER in repr_str
        assert TEST_COUNTRY_CODE in repr_str
        assert TEST_ORGANIZATION in repr_str

    def test_post_init_invalid_ip_address(self) -> None:
        """無効なIPアドレスでの初期化テスト."""
        match = "'invalid.ip' does not appear to be an IPv4 or IPv6 address"
        with pytest.raises(ValidationError, match=match):
            IPData(
                ip_address="invalid_ip",
                network=TEST_IP_NETWORK,
                as_number=TEST_AS_NUMBER,
                country=TEST_COUNTRY_CODE,
                organization=TEST_ORGANIZATION,
            )

    def test_post_init_invalid_ip_network(self) -> None:
        """無効なIPネットワークでの初期化テスト."""
        match = "'invalid.network' does not appear to be an IPv4 or IPv6 network"
        with pytest.raises(ValidationError, match=match):
            IPData(
                ip_address=TEST_IP_ADDRESS_1,
                network="invalid.network",
                as_number=TEST_AS_NUMBER,
                country=TEST_COUNTRY_CODE,
                organization=TEST_ORGANIZATION,
            )

    @pytest.mark.parametrize(
        "as_number",
        [
            AS_NUMBER_MIN - 1,
            AS_NUMBER_MAX + 1,
        ],
    )
    def test_post_init_invalid_as_number(self, as_number: int) -> None:
        """無効な自律システム番号の初期化テスト."""
        match = f"AS number must be between {AS_NUMBER_MIN} and {AS_NUMBER_MAX - 1}"
        with pytest.raises(ValidationError, match=match):
            IPData(
                ip_address=TEST_IP_ADDRESS_1,
                network=TEST_IP_NETWORK,
                as_number=str(as_number),
                country=TEST_COUNTRY_CODE,
                organization=TEST_ORGANIZATION,
            )

    @pytest.mark.parametrize(
        "country_code",
        [
            "U",
            "USA",
        ],
    )
    def test_post_init_invalid_country_code(self, country_code: str) -> None:
        """無効な国コードの初期化テスト."""
        match = f"Country code must be {COUNTRY_CODE_LENGTH} characters"
        with pytest.raises(ValidationError, match=match):
            IPData(
                ip_address=TEST_IP_ADDRESS_1,
                network=TEST_IP_NETWORK,
                as_number=TEST_AS_NUMBER,
                country=country_code,
                organization=TEST_ORGANIZATION,
            )

    def test_is_complete_with_complete_data(self) -> None:
        """完全なデータでのis_completeテスト."""
        ip_data = IPData(
            ip_address=TEST_IP_ADDRESS_1,
            network=TEST_IP_NETWORK,
            as_number=TEST_AS_NUMBER,
            country=TEST_COUNTRY_CODE,
            organization=TEST_ORGANIZATION,
        )

        assert ip_data.is_complete() is True

    def test_is_complete_with_empty_ip_network(self) -> None:
        """空のIPネットワークでのis_completeテスト."""
        ip_data = IPData(
            ip_address=TEST_IP_ADDRESS_1,
            network="",
            as_number=TEST_AS_NUMBER,
            country=TEST_COUNTRY_CODE,
            organization=TEST_ORGANIZATION,
        )

        assert ip_data.is_complete() is False

    def test_is_complete_with_zero_as_number(self) -> None:
        """空のAS番号でのis_completeテスト."""
        ip_data = IPData(
            ip_address=TEST_IP_ADDRESS_1,
            network=TEST_IP_NETWORK,
            as_number="",
            country=TEST_COUNTRY_CODE,
            organization=TEST_ORGANIZATION,
        )

        assert ip_data.is_complete() is False

    def test_is_complete_with_empty_country_code(self) -> None:
        """空の国コードでのis_completeテスト."""
        ip_data = IPData(
            ip_address=TEST_IP_ADDRESS_1,
            network=TEST_IP_NETWORK,
            as_number=TEST_AS_NUMBER,
            country="",
            organization=TEST_ORGANIZATION,
        )

        assert ip_data.is_complete() is False

    def test_is_complete_with_empty_organization(self) -> None:
        """空の組織名でのis_completeテスト."""
        ip_data = IPData(
            ip_address=TEST_IP_ADDRESS_1,
            network=TEST_IP_NETWORK,
            as_number=TEST_AS_NUMBER,
            country=TEST_COUNTRY_CODE,
            organization="",
        )

        assert ip_data.is_complete() is False

    def test_is_complete_with_all_empty(self) -> None:
        """IPアドレス以外が空でのis_completeテスト."""
        ip_data = IPData(
            ip_address=TEST_IP_ADDRESS_1,
            network="",
            as_number="",
            country="",
            organization="",
        )

        assert ip_data.is_complete() is False

    def test_to_dict(self) -> None:
        """to_dictメソッドのテスト."""
        ip_data = IPData(
            ip_address=TEST_IP_ADDRESS_1,
            network=TEST_IP_NETWORK,
            as_number=TEST_AS_NUMBER,
            country=TEST_COUNTRY_CODE,
            organization=TEST_ORGANIZATION,
        )

        expected = {
            "ip_address": TEST_IP_ADDRESS_1,
            "network": TEST_IP_NETWORK,
            "as_number": TEST_AS_NUMBER,
            "country": TEST_COUNTRY_CODE,
            "organization": TEST_ORGANIZATION,
        }

        assert ip_data.to_dict() == expected

    def test_to_dict_with_empty_values(self) -> None:
        """IPアドレス以外が空でのto_dictテスト."""
        ip_data = IPData(
            ip_address=TEST_IP_ADDRESS_1,
            network="",
            as_number="",
            country="",
            organization="",
        )

        expected = {
            "ip_address": TEST_IP_ADDRESS_1,
            "network": "",
            "as_number": "",
            "country": "",
            "organization": "",
        }

        assert ip_data.to_dict() == expected
