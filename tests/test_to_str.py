"""_to_str関数のテスト."""

from ipaddress import IPv4Network, IPv6Network

import pytest

from ipinfo_geoip.geoip_client import _to_str


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
