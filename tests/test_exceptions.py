"""例外クラスのテスト."""

import pytest

from ipinfo_geoip.exceptions import (
    CacheError,
    ConfigurationError,
    GeoIPClientError,
    IPInfoError,
    NetworkError,
    RedisClientError,
    ValidationError,
)


class TestIPInfoError:
    """IPInfoErrorベース例外のテストクラス."""

    def test_init_message_only(self) -> None:
        """メッセージのみでの初期化テスト."""
        error = IPInfoError("テストエラー")
        assert str(error) == "テストエラー"
        assert error.message == "テストエラー"
        assert error.details == {}

    def test_init_with_details(self) -> None:
        """詳細情報付きでの初期化テスト."""
        details = {"ip_address": "192.168.1.1", "code": 500}
        error = IPInfoError("詳細エラー", details)

        assert str(error) == "詳細エラー"
        assert error.message == "詳細エラー"
        assert error.details == details

    def test_init_with_none_details(self) -> None:
        """詳細情報がNoneの場合のテスト."""
        error = IPInfoError("エラー", None)
        assert error.details == {}


class TestSpecificErrors:
    """各種固有例外のテストクラス."""

    def test_geoip_client_error_inheritance(self) -> None:
        """GeoIPClientErrorの継承テスト."""
        error = GeoIPClientError("GeoIPエラー")
        assert isinstance(error, IPInfoError)
        assert isinstance(error, Exception)

    def test_redis_client_error_inheritance(self) -> None:
        """RedisClientErrorの継承テスト."""
        error = RedisClientError("Redisエラー")
        assert isinstance(error, IPInfoError)
        assert isinstance(error, Exception)

    def test_configuration_error_inheritance(self) -> None:
        """ConfigurationErrorの継承テスト."""
        error = ConfigurationError("設定エラー")
        assert isinstance(error, IPInfoError)
        assert isinstance(error, Exception)

    def test_network_error_inheritance(self) -> None:
        """NetworkErrorの継承テスト."""
        error = NetworkError("ネットワークエラー")
        assert isinstance(error, IPInfoError)
        assert isinstance(error, Exception)

    def test_cache_error_inheritance(self) -> None:
        """CacheErrorの継承テスト."""
        error = CacheError("キャッシュエラー")
        assert isinstance(error, IPInfoError)
        assert isinstance(error, Exception)

    def test_validation_error_inheritance(self) -> None:
        """ValidationErrorの継承テスト."""
        error = ValidationError("検証エラー")
        assert isinstance(error, IPInfoError)
        assert isinstance(error, Exception)


class TestErrorDetails:
    """エラー詳細情報のテストクラス."""

    def test_all_errors_support_details(self) -> None:
        """すべてのエラーが詳細情報をサポートすることのテスト."""
        details = {"test": "value"}

        errors = [
            GeoIPClientError("test", details),
            RedisClientError("test", details),
            ConfigurationError("test", details),
            NetworkError("test", details),
            CacheError("test", details),
            ValidationError("test", details),
        ]

        for error in errors:
            assert error.details == details
            assert error.message == "test"


class TestErrorRaising:
    """エラー発生のテストクラス."""

    def test_raise_ipinfo_error(self) -> None:
        """IPInfoErrorの発生テスト."""
        message = "テストエラー"
        details = {"key": "value"}
        with pytest.raises(IPInfoError) as exc_info:
            raise IPInfoError(message, details)

        assert exc_info.value.message == message
        assert exc_info.value.details == details

    def test_raise_geoip_client_error(self) -> None:
        """GeoIPClientErrorの発生テスト."""
        message = "GeoIPテストエラー"
        with pytest.raises(GeoIPClientError):
            raise GeoIPClientError(message)

    def test_raise_redis_client_error(self) -> None:
        """RedisClientErrorの発生テスト."""
        message = "Redisテストエラー"
        with pytest.raises(RedisClientError):
            raise RedisClientError(message)

    def test_catch_as_base_exception(self) -> None:
        """ベース例外としてのキャッチテスト."""
        message1 = "サブクラスエラー"
        message2 = "別のサブクラスエラー"
        with pytest.raises(IPInfoError):
            raise GeoIPClientError(message1)

        with pytest.raises(IPInfoError):
            raise ValidationError(message2)
