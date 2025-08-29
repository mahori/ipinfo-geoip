"""IPInfo GeoIP関連の例外クラス定義."""

from typing import Any


class IPInfoError(Exception):
    """IPInfo関連のベース例外クラス."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """例外を初期化する.

        Args:
            message: エラーメッセージ
            details: エラーの詳細情報

        """
        super().__init__(message)

        self.message = message
        self.details = details or {}


class GeoIPClientError(IPInfoError):
    """GeoIPクライアント関連のエラー."""


class RedisClientError(IPInfoError):
    """Redisクライアント関連のエラー."""


class ConfigurationError(IPInfoError):
    """設定関連のエラー."""


class NetworkError(IPInfoError):
    """ネットワーク関連のエラー."""


class CacheError(IPInfoError):
    """キャッシュ関連のエラー."""


class ValidationError(IPInfoError):
    """データ検証関連のエラー."""
