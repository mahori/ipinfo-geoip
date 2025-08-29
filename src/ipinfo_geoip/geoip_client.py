"""MaxMind GeoLite2 Web Serviceクライアント."""

import os
from collections import UserDict
from ipaddress import IPv4Network, IPv6Network
from typing import Self

import geoip2.errors
import geoip2.webservice

from .constants import GEOIP_ACCOUNT_ID_ENV, GEOIP_HOST_ENV, GEOIP_LICENSE_KEY_ENV
from .exceptions import ConfigurationError, GeoIPClientError, ValidationError
from .ipdata import IPData


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


class GeoIPConfig:
    """MaxMind GeoLite2 Web Serviceの設定クラス.

    Attributes:
        account_id: アカウントID
        license_key: ライセンスキー
        host: ホスト名

    """

    def __init__(self, account_id: str, license_key: str, host: str) -> None:
        """GeoIP設定を初期化する.

        Args:
            account_id: アカウントID
            license_key: ライセンスキー
            host: ホスト名

        Raises:
            TypeError: 引数の型が正しくない場合

        """
        if not isinstance(account_id, str):
            raise TypeError
        if not isinstance(license_key, str):
            raise TypeError
        if not isinstance(host, str):
            raise TypeError

        self.account_id = int(account_id)
        self.license_key = license_key
        self.host = host

    @classmethod
    def from_env(cls) -> Self:
        """環境変数からGeoIP設定を作成する.

        Returns:
            環境変数から作成されたGeoIPConfig

        Raises:
            ValidationError: 必要な環境変数が設定されていない場合

        """
        missing_vars = []
        if GEOIP_ACCOUNT_ID_ENV not in os.environ:
            missing_vars.append(GEOIP_ACCOUNT_ID_ENV)
        if GEOIP_LICENSE_KEY_ENV not in os.environ:
            missing_vars.append(GEOIP_LICENSE_KEY_ENV)
        if GEOIP_HOST_ENV not in os.environ:
            missing_vars.append(GEOIP_HOST_ENV)

        if missing_vars:
            msg = f"Missing environment variables: {', '.join(missing_vars)}"
            raise ValidationError(msg)

        account_id = os.environ[GEOIP_ACCOUNT_ID_ENV]
        license_key = os.environ[GEOIP_LICENSE_KEY_ENV]
        host = os.environ[GEOIP_HOST_ENV]

        return cls(account_id, license_key, host)


class GeoIPClient(UserDict[str, IPData | None]):
    """MaxMind GeoLite2 Web Serviceクライアント."""

    def __init__(self) -> None:
        """GeoIPクライアントを初期化する.

        Raises:
            ConfigurationError: 必要な認証情報が不足している場合

        """
        super().__init__()

        try:
            config = GeoIPConfig.from_env()
        except ValidationError as e:
            msg = "GeoIP configuration error"
            raise ConfigurationError(msg, {"error": str(e)}) from e
        self.client = geoip2.webservice.Client(config.account_id, config.license_key, config.host)

    def __missing__(self, ip_address: str) -> IPData | None:
        """指定されたIPアドレスの地理的情報等を取得する.

        Args:
            ip_address: 検索するIPアドレス

        Returns:
            IPアドレスの情報
            見つからない場合はNone

        Raises:
            TypeError: ip_addressが文字列でない場合
            GeoIPClientError: GeoIPサービスでエラーが発生した場合

        """
        if not isinstance(ip_address, str):
            raise TypeError

        try:
            response = self.client.city(ip_address)
        except geoip2.errors.AddressNotFoundError as e:
            msg = f"Address not found: {ip_address}"
            raise GeoIPClientError(msg, {"ip_address": ip_address, "error": str(e)}) from e

        if response is None:
            return None

        network = _to_str(response.traits.network)
        as_number = _to_str(response.traits.autonomous_system_number)
        country = _to_str(response.country.iso_code)
        organization = _to_str(response.traits.autonomous_system_organization)

        ip_data = IPData(ip_address, network, as_number, country, organization)

        super().__setitem__(ip_address, ip_data)

        return ip_data
