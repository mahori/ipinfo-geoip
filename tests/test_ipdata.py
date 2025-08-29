"""IPDataクラスのテスト."""

from ipinfo_geoip.ipdata import IPData


class TestIPData:
    """IPDataクラスのテストクラス."""

    def test_init(self) -> None:
        """初期化のテスト."""
        ip_data = IPData(
            ip_address="8.8.8.8",
            network="8.8.8.0/24",
            as_number="15169",
            country="US",
            organization="Google LLC",
        )

        assert ip_data.ip_address == "8.8.8.8"
        assert ip_data.network == "8.8.8.0/24"
        assert ip_data.as_number == "15169"
        assert ip_data.country == "US"
        assert ip_data.organization == "Google LLC"

    def test_is_complete_with_complete_data(self) -> None:
        """完全なデータでのis_completeテスト."""
        ip_data = IPData(
            ip_address="8.8.8.8", network="8.8.8.0/24", as_number="15169", country="US", organization="Google LLC"
        )

        assert ip_data.is_complete() is True

    def test_is_complete_with_empty_network(self) -> None:
        """空のネットワークでのis_completeテスト."""
        ip_data = IPData(
            ip_address="192.168.1.1",
            network="",  # 空
            as_number="15169",
            country="US",
            organization="Google LLC",
        )

        assert ip_data.is_complete() is False

    def test_is_complete_with_zero_as_number(self) -> None:
        """AS番号が0でのis_completeテスト."""
        ip_data = IPData(
            ip_address="192.168.1.1",
            network="192.168.1.0/24",
            as_number="",  # 空
            country="US",
            organization="Google LLC",
        )

        assert ip_data.is_complete() is False

    def test_is_complete_with_empty_country(self) -> None:
        """空の国コードでのis_completeテスト."""
        ip_data = IPData(
            ip_address="192.168.1.1",
            network="192.168.1.0/24",
            as_number="15169",
            country="",  # 空
            organization="Google LLC",
        )

        assert ip_data.is_complete() is False

    def test_is_complete_with_empty_organization(self) -> None:
        """空の組織名でのis_completeテスト."""
        ip_data = IPData(
            ip_address="192.168.1.1",
            network="192.168.1.0/24",
            as_number="15169",
            country="US",
            organization="",  # 空
        )

        assert ip_data.is_complete() is False

    def test_is_complete_with_all_empty(self) -> None:
        """すべて空でのis_completeテスト."""
        ip_data = IPData(ip_address="invalid", network="", as_number="", country="", organization="")

        assert ip_data.is_complete() is False

    def test_to_dict(self) -> None:
        """to_dictメソッドのテスト."""
        ip_data = IPData(
            ip_address="8.8.8.8", network="8.8.8.0/24", as_number="15169", country="US", organization="Google LLC"
        )

        expected = {
            "ip_address": "8.8.8.8",
            "network": "8.8.8.0/24",
            "as_number": "15169",
            "country": "US",
            "organization": "Google LLC",
        }

        assert ip_data.to_dict() == expected

    def test_to_dict_with_empty_values(self) -> None:
        """空の値を含むto_dictメソッドのテスト."""
        ip_data = IPData(ip_address="192.168.1.1", network="", as_number="", country="", organization="")

        expected = {"ip_address": "192.168.1.1", "network": "", "as_number": "", "country": "", "organization": ""}

        assert ip_data.to_dict() == expected

    def test_dataclass_equality(self) -> None:
        """データクラスの等価性テスト."""
        ip_data1 = IPData(
            ip_address="8.8.8.8",
            network="8.8.8.0/24",
            as_number="15169",
            country="US",
            organization="Google LLC",
        )

        ip_data2 = IPData(
            ip_address="8.8.8.8",
            network="8.8.8.0/24",
            as_number="15169",
            country="US",
            organization="Google LLC",
        )

        assert ip_data1 == ip_data2

    def test_dataclass_inequality(self) -> None:
        """データクラスの非等価性テスト."""
        ip_data1 = IPData(
            ip_address="8.8.8.8",
            network="8.8.8.0/24",
            as_number="15169",
            country="US",
            organization="Google LLC",
        )

        ip_data2 = IPData(
            ip_address="8.8.4.4",  # 異なるIP
            network="8.8.8.0/24",
            as_number="15169",
            country="US",
            organization="Google LLC",
        )

        assert ip_data1 != ip_data2

    def test_dataclass_repr(self) -> None:
        """データクラスの文字列表現テスト."""
        ip_data = IPData(
            ip_address="8.8.8.8",
            network="8.8.8.0/24",
            as_number="15169",
            country="US",
            organization="Google LLC",
        )

        repr_str = repr(ip_data)
        assert "IPData" in repr_str
        assert "8.8.8.8" in repr_str
        assert "15169" in repr_str
        assert "Google LLC" in repr_str
