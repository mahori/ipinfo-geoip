# ipinfo-geoip

[![Release](https://github.com/mahori/ipinfo-geoip/actions/workflows/release.yml/badge.svg)](https://github.com/mahori/ipinfo-geoip/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/mahori/ipinfo-geoip/actions/workflows/ci.yml/badge.svg)](https://github.com/mahori/ipinfo-geoip/actions/workflows/ci.yml)
[![CodeQL](https://github.com/mahori/ipinfo-geoip/actions/workflows/codeql.yml/badge.svg)](https://github.com/mahori/ipinfo-geoip/actions/workflows/codeql.yml)
[![codecov](https://codecov.io/gh/mahori/ipinfo-geoip/graph/badge.svg?token=70GXGLS97X)](https://codecov.io/gh/mahori/ipinfo-geoip)

IPアドレスからネットワーク，AS番号，国，組織を取得するPythonパッケージ

MaxMind社のGeoLite Web Serviceを使用してIPアドレス情報を取得し，Redisでキャッシュ機能を提供します．

## 特徴

- **GeoLite Web Service** を使用したIPアドレス情報の取得
- **Redis** を使用したIPアドレス情報のキャッシュ
- **型ヒント対応** (mypy準拠)
- **包括的なテスト** (pytest + pytest-cov)

## 環境変数設定

以下の環境変数を設定してください:

```bash
# GeoLite2 Web Service設定
export IPINFO_GEOIP_ACCOUNT_ID="アカウントID"
export IPINFO_GEOIP_LICENSE_KEY="ライセンスキー"
export IPINFO_GEOIP_HOST="geolite.info"

# Redis設定
export IPINFO_REDIS_URI="redis://localhost:6379/0"
export IPINFO_REDIS_CACHE_TTL="2419200"  # 28日
```

## 基本的な使用方法

```python
from ipinfo_geoip import IPInfo
import json

# IPInfoインスタンスを作成
ipinfo = IPInfo()

# IPアドレスからネットワーク，AS番号，国，組織を取得
result = ipinfo["8.8.8.8"]

# 結果を表示
print(f"国: {result['country']}")
print(f"AS番号: {result['as_number']}")
print(f"ネットワーク: {result['network']}")

# またはJSON文字列として表示
print(json.dumps(result))
```

## 出力例

```json
{
  "ip_address": "8.8.8.8",
  "network": "8.8.8.0/24",
  "as_number": "15169",
  "country": "US",
  "organization": "GOOGLE"
}
```

## 例外処理

```python
from ipinfo_geoip import IPInfo
from ipinfo_geoip.exceptions import (
    ConfigurationError,
    IPInfoError
)

try:
    ipinfo = IPInfo()
    result = ipinfo["invalid.ip"]
except ConfigurationError as e:
    print(f"設定エラー: {e}")
except IPInfoError as e:
    print(f"一般的なエラー: {e}")
    print(f"詳細: {e.details}")
```

## 開発者向け情報

### 開発環境セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/mahori/ipinfo-geoip.git
cd ipinfo-geoip

# uvで開発環境セットアップ
uv sync --dev
```

### テスト実行

```bash
# テストを実行
uvx nox -s test

# カバレッジ付きでテストを実行
uvx nox -s coverage
```

### コードフォーマット・リント

```bash
# コードフォーマット
uvx nox -s format

# リント実行
uvx nox -s lint

# 型チェック
uvx nox -s typecheck
```

### ビルド

```bash
# パッケージビルド
uvx nox -s build
```

## 要件

- Python 3.11+
- GeoLite Web Serviceアカウント
- Redisサーバー

## 依存関係

- `geoip2>=5.1.0` - GeoLite2 Web Serviceクライアント
- `redis>=6.4.0` - Redisクライアント

## ライセンス

[MIT License](LICENSE)

本プロジェクトは MIT License で公開されています．

ただし以下の依存パッケージを利用しており，それぞれのライセンス条件にも従う必要があります．

- [geoip2](https://github.com/maxmind/GeoIP2-python) - [Apache License 2.0](https://github.com/maxmind/GeoIP2-python/blob/main/LICENSE)
- [redis](https://github.com/redis/redis-py) - [MIT License](https://github.com/redis/redis-py/blob/master/LICENSE)

## 貢献

貢献を歓迎します．詳細は [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください．

## セキュリティ

セキュリティ関連の問題は [SECURITY.md](SECURITY.md) を参照してください．

## サポート

- [GitHub Issues](https://github.com/mahori/ipinfo-geoip/issues) - バグ報告・機能要望
