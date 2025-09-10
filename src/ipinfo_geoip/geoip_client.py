"""GeoLite2 Web Serviceクライアント."""

from collections import UserDict

import geoip2.errors
import geoip2.webservice

from .exceptions import ConfigurationError, GeoIPClientError, ValidationError
from .geoip_config import GeoIPConfig
from .ipdata import IPData
from .to_str import _to_str


class GeoIPClient(UserDict[str, IPData | None]):
    """GeoLite2 Web Serviceクライアント."""

    def __init__(self) -> None:
        """GeoLite2 Web Serviceクライアントを初期化する.

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
        """指定されたGeoIP情報を取得する.

        Args:
            ip_address: 検索するIPアドレス

        Returns:
            GeoIP情報
            見つからない場合はNone

        Raises:
            TypeError: ip_addressが文字列でない場合
            GeoIPClientError: GeoLite2 Web Serviceでエラーが発生した場合

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
