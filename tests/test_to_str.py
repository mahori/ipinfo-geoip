"""_to_str関数のテスト."""

from ipaddress import IPv4Network, IPv6Network

import pytest

from ipinfo_geoip.to_str import _to_str


class TestToStr:
    """_to_str関数のテストクラス."""

    def test_to_str_with_none(self) -> None:
        """Noneの場合のテスト."""
        assert _to_str(None) == ""

    def test_to_str_with_bool(self) -> None:
        """ブール値の場合のテスト."""
        with pytest.raises(TypeError):
            _to_str(bool(0))

        with pytest.raises(TypeError):
            _to_str(bool(1))

    def test_to_str_with_int(self) -> None:
        """整数値の場合のテスト."""
        assert _to_str(-6) == "-6"
        assert _to_str(0) == "0"
        assert _to_str(6) == "6"

    def test_to_str_with_str(self) -> None:
        """文字列の場合のテスト."""
        assert _to_str("") == ""
        assert _to_str("テスト") == "テスト"

    def test_to_str_with_ipv4_network(self) -> None:
        """IPv4Networkの場合のテスト."""
        assert _to_str(IPv4Network("192.0.2.0/24")) == "192.0.2.0/24"

    def test_to_str_with_ipv6_network(self) -> None:
        """IPv6Networkの場合のテスト."""
        assert _to_str(IPv6Network("2001:db8::/32")) == "2001:db8::/32"

    def test_to_str_with_unsupported_type(self) -> None:
        """サポートされていない型の場合のテスト."""
        with pytest.raises(TypeError):
            _to_str(3.14)  # type: ignore[arg-type]

        with pytest.raises(TypeError):
            _to_str([1, 2, 3])  # type: ignore[arg-type]

        with pytest.raises(TypeError):
            _to_str({"key": "value"})  # type: ignore[arg-type]
