"""IPの地理的位置情報データモデル."""

from dataclasses import dataclass


@dataclass
class IPData:
    """IPの地理的位置情報を表すデータクラス.

    Attributes:
        ip_address: IPアドレス
        network: ネットワークCIDRブロック
        as_number: 自律システム番号
        country: ISO国コード
        organization: 組織名

    """

    ip_address: str
    network: str
    as_number: str
    country: str
    organization: str

    def is_complete(self) -> bool:
        """すべてのフィールドが空でないかチェックする.

        Returns:
            すべてのフィールドが空でない場合True

        """
        return self.network != "" and self.as_number != "" and self.country != "" and self.organization != ""

    def to_dict(self) -> dict[str, str]:
        """IPデータを辞書形式に変換する.

        Returns:
            IPデータのフィールドを含む辞書

        """
        return {
            "ip_address": self.ip_address,
            "network": self.network,
            "as_number": self.as_number,
            "country": self.country,
            "organization": self.organization,
        }
