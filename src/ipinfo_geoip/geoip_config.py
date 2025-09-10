"""GeoLite2 Web Service接続設定."""

import os
from typing import Self

from .constants import GEOIP_ACCOUNT_ID_ENV, GEOIP_HOST_ENV, GEOIP_LICENSE_KEY_ENV
from .exceptions import ValidationError


class GeoIPConfig:
    """GeoLite2 Web Service接続設定クラス.

    Attributes:
        account_id: アカウントID
        license_key: ライセンスキー
        host: ホスト名

    """

    def __init__(self, account_id: str, license_key: str, host: str) -> None:
        """GeoLite2 Web Service設定を初期化する.

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
        """環境変数からGeoLite2 Web Service設定を作成する.

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
