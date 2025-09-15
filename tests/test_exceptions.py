"""例外クラスのテスト."""

import pytest

from ipinfo_geoip.exceptions import (
    ConfigurationError,
    GeoIPClientError,
    IPInfoError,
    RedisClientError,
    ValidationError,
)
from tests.conftest import TEST_EXCEPTION_DETAILS, TEST_EXCEPTION_MESSAGE


class TestErrorInheritance:
    """各種例外クラスの継承テストクラス."""

    def test_ip_info_error_inheritance(self) -> None:
        """IPInfoErrorの継承テスト."""
        exception = GeoIPClientError(TEST_EXCEPTION_MESSAGE)

        assert isinstance(exception, Exception)

    def test_geoip_client_error_inheritance(self) -> None:
        """GeoIPClientErrorの継承テスト."""
        exception = GeoIPClientError(TEST_EXCEPTION_MESSAGE)

        assert isinstance(exception, IPInfoError)
        assert isinstance(exception, Exception)

    def test_redis_client_error_inheritance(self) -> None:
        """RedisClientErrorの継承テスト."""
        exception = RedisClientError(TEST_EXCEPTION_MESSAGE)

        assert isinstance(exception, IPInfoError)
        assert isinstance(exception, Exception)

    def test_configuration_error_inheritance(self) -> None:
        """ConfigurationErrorの継承テスト."""
        exception = ConfigurationError(TEST_EXCEPTION_MESSAGE)

        assert isinstance(exception, IPInfoError)
        assert isinstance(exception, Exception)

    def test_validation_error_inheritance(self) -> None:
        """ValidationErrorの継承テスト."""
        exception = ValidationError(TEST_EXCEPTION_MESSAGE)

        assert isinstance(exception, IPInfoError)
        assert isinstance(exception, Exception)


class TestErrorMessage:
    """エラーメッセージのテストクラス."""

    @pytest.mark.parametrize(
        "exception_class",
        [
            IPInfoError,
            GeoIPClientError,
            RedisClientError,
            ConfigurationError,
            ValidationError,
        ],
    )
    def test_error_support_message_only(self, exception_class: type) -> None:
        """各種例外がメッセージのみをサポートすることのテスト."""
        exception = exception_class(TEST_EXCEPTION_MESSAGE)

        assert exception.message == TEST_EXCEPTION_MESSAGE
        assert exception.details == {}


class TestErrorDetails:
    """エラー詳細情報のテストクラス."""

    @pytest.mark.parametrize(
        "exception_class",
        [
            IPInfoError,
            GeoIPClientError,
            RedisClientError,
            ConfigurationError,
            ValidationError,
        ],
    )
    def test_error_support_details(self, exception_class: type) -> None:
        """各種例外が詳細情報をサポートすることのテスト."""
        exception = exception_class(TEST_EXCEPTION_MESSAGE, TEST_EXCEPTION_DETAILS)

        assert exception.message == TEST_EXCEPTION_MESSAGE
        assert exception.details == TEST_EXCEPTION_DETAILS


class TestErrorNoneDetails:
    """エラー詳細情報がNoneの場合のテストクラス."""

    @pytest.mark.parametrize(
        "exception_class",
        [
            IPInfoError,
            GeoIPClientError,
            RedisClientError,
            ConfigurationError,
            ValidationError,
        ],
    )
    def test_error_support_none_details(self, exception_class: type) -> None:
        """各種例外がNoneの詳細情報をサポートすることのテスト."""
        exception = exception_class(TEST_EXCEPTION_MESSAGE, None)

        assert exception.message == TEST_EXCEPTION_MESSAGE
        assert exception.details == {}


class TestErrorRaising:
    """例外発生のテストクラス."""

    @pytest.mark.parametrize(
        "exception_class",
        [
            IPInfoError,
            GeoIPClientError,
            RedisClientError,
            ConfigurationError,
            ValidationError,
        ],
    )
    def test_error_raising(self, exception_class: type) -> None:
        """各種例外の発生テスト."""
        with pytest.raises(exception_class):
            raise exception_class(TEST_EXCEPTION_MESSAGE)


class TestCatchAsBaseException:
    """基底例外としてのキャッチテストクラス."""

    @pytest.mark.parametrize(
        "exception_class",
        [
            GeoIPClientError,
            RedisClientError,
            ConfigurationError,
            ValidationError,
        ],
    )
    def test_catch_as_ip_info_error(self, exception_class: type) -> None:
        """IPInfoErrorとしてのキャッチテスト."""
        with pytest.raises(IPInfoError):
            raise exception_class(TEST_EXCEPTION_MESSAGE)

    @pytest.mark.parametrize(
        "exception_class",
        [
            IPInfoError,
            GeoIPClientError,
            RedisClientError,
            ConfigurationError,
            ValidationError,
        ],
    )
    def test_catch_as_exception(self, exception_class: type) -> None:
        """Exceptionとしてのキャッチテスト."""
        with pytest.raises(Exception, match=TEST_EXCEPTION_MESSAGE):
            raise exception_class(TEST_EXCEPTION_MESSAGE)
