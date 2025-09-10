"""Noxビルドシステムの設定ファイル."""

import shutil
import sys
from pathlib import Path

import nox

nox.options.default_venv_backend = "uv"
nox.options.error_on_external_run = True
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["format", "lint", "typecheck", "test"]
nox.options.stop_on_first_error = True


@nox.session(name="format")
def ruff_format(session: nox.Session) -> None:
    """コードフォーマットを実行する.

    Args:
        session: Noxセッション

    """
    session.install("ruff")
    session.run("ruff", "format")


@nox.session(name="lint")
def ruff_check(session: nox.Session) -> None:
    """リンターチェックを実行する.

    Args:
        session: Noxセッション

    """
    session.install("ruff")
    session.run("ruff", "check")


@nox.session(name="typecheck")
def mypy(session: nox.Session) -> None:
    """型チェックを実行する.

    Args:
        session: Noxセッション

    """
    session.install(".", "mypy", "pytest-mypy-plugins")
    session.run("mypy", "src", "tests")
    session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@nox.session(name="test")
def pytest(session: nox.Session) -> None:
    """テストを実行する.

    Args:
        session: Noxセッション

    """
    session.install(".", "pytest")
    session.run("pytest", "-v", *session.posargs)


@nox.session(name="coverage")
def pytest_coverage(session: nox.Session) -> None:
    """テストカバレッジを実行する.

    Args:
        session: Noxセッション

    """
    session.install(".", "pytest", "pytest-cov")
    session.run(
        "pytest",
        "-v",
        "--cov=ipinfo_geoip",
        "--cov-report=xml:coverage.xml",
        "--cov-report=term-missing",
        *session.posargs,
    )


@nox.session
def build(session: nox.Session) -> None:
    """プロジェクトをビルドする.

    Args:
        session: Noxセッション

    """
    dist_directory = Path("dist")
    if dist_directory.exists():
        shutil.rmtree(dist_directory)
    session.run("uv", "build")


@nox.session
def clean(_session: nox.Session) -> None:
    """クリーンアップを実行する.

    Args:
        session: Noxセッション

    """
    directories = ["build", "dist", ".mypy_cache", ".nox", ".pytest_cache", ".ruff_cache", ".venv"]
    for directory in directories:
        directory_path = Path(directory)
        if directory_path.exists() and directory_path.is_dir():
            shutil.rmtree(directory_path)
    files = [".coverage", "coverage.xml"]
    for file in files:
        file_path = Path(file)
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
    for pycache in Path.cwd().rglob("__pycache__"):
        shutil.rmtree(pycache)
