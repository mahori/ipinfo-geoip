"""値を文字列に変換."""

from ipaddress import IPv4Network, IPv6Network


def _to_str(value: int | str | IPv4Network | IPv6Network | None) -> str:
    """値を文字列に変換する.

    Args:
        value: 変換する値

    Returns:
        文字列に変換された値
        Noneの場合は空文字列

    Raises:
        TypeError: サポートされていない型の場合

    """
    if value is None:
        return ""
    if isinstance(value, bool):
        raise TypeError
    if isinstance(value, str):
        return value
    if isinstance(value, (int, IPv4Network, IPv6Network)):
        return str(value)
    raise TypeError
