"""IPアドレス情報データモデル."""

import ipaddress
from dataclasses import dataclass

from .constants import AS_NUMBER_MAX, AS_NUMBER_MIN, COUNTRY_CODE_LENGTH
from .exceptions import ValidationError


@dataclass
class IPData:
    """IPアドレス情報を表すデータクラス.

    Attributes:
        ip_address: IPアドレス
        network: IPネットワーク(CIDRブロック)
        as_number: 自律システム番号
        country: ISO国コード
        organization: 組織名

    Raises:
        ValidationError: フィールドの値が無効な場合

    """

    ip_address: str
    network: str
    as_number: str
    country: str
    organization: str

    def __post_init__(self) -> None:
        """オブジェクト初期化後のバリデーション.

        Raises:
            ValidationError: フィールドの値が無効な場合

        """
        try:
            _ = ipaddress.ip_address(self.ip_address)
        except ValueError as e:
            raise ValidationError(str(e)) from e

        if self.network != "":
            try:
                _ = ipaddress.ip_network(self.network)
            except ValueError as e:
                raise ValidationError(str(e)) from e

        if self.as_number != "":
            as_number = int(self.as_number)
            if as_number < AS_NUMBER_MIN or as_number >= AS_NUMBER_MAX:
                msg = f"AS number must be between {AS_NUMBER_MIN} and {AS_NUMBER_MAX - 1}"
                raise ValidationError(msg)

        if self.country != "" and len(self.country) != COUNTRY_CODE_LENGTH:
            msg = f"Country code must be {COUNTRY_CODE_LENGTH} characters"
            raise ValidationError(msg)

    def is_complete(self) -> bool:
        """IPアドレス以外のフィールドが空でないかチェックする.

        Returns:
            IPアドレス以外のフィールドが空でない場合True

        """
        return self.network != "" and self.as_number != "" and self.country != "" and self.organization != ""

    def to_dict(self) -> dict[str, str]:
        """データを辞書形式に変換する.

        Returns:
            データのフィールドを含む辞書

        """
        return {
            "ip_address": self.ip_address,
            "network": self.network,
            "as_number": self.as_number,
            "country": self.country,
            "organization": self.organization,
        }
