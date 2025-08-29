# 貢献ガイド(Contributing Guide)

ipinfo-geoipプロジェクトへの貢献を検討していただきありがとうございます．このガイドではプロジェクトに貢献するためのプロセスと期待事項を説明します．

## 行動規範

このプロジェクトに参加することで，あなたは私たちの[行動規範](CODE_OF_CONDUCT.md)を遵守することに同意したものとみなされます．

## 貢献の種類

以下のような貢献を歓迎します:

### バグ報告
- 明確で詳細な説明
- 再現可能な手順
- 期待される動作と実際の動作
- 環境情報(Pythonバージョン，OSなど)

### 機能要求
- 明確な使用ケースの説明
- 提案するAPIの例
- なぜこの機能が有用なのかの説明

### コード貢献
- バグ修正
- 新機能の実装
- パフォーマンス改善
- ドキュメントの改善
- テストの追加・改善

## 開発環境のセットアップ

### 前提条件

- Python 3.11+
- Git
- [uv](https://docs.astral.sh/uv/) - Pythonパッケージマネージャ
- MaxMind GeoLite2アカウント
- Redisサーバー

### セットアップ手順

1. リポジトリをフォーク・クローン

```bash
git clone https://github.com/yourusername/ipinfo-geoip.git
cd ipinfo-geoip
```

2. 開発環境を初期化

```bash
# uvで依存関係をインストール
uv sync --dev
```

3. 環境変数を設定

```bash
# GeoIP設定
export IPINFO_GEOIP_ACCOUNT_ID="GeoLite2 アカウントID"
export IPINFO_GEOIP_LICENSE_KEY="GeoLite2 ライセンスキー"
export IPINFO_GEOIP_HOST="geolite.info"

# Redis設定
export IPINFO_REDIS_URI="redis://localhost:6379/0"
export IPINFO_REDIS_CACHE_TTL="2419200"  # 28日
```

4. テストを実行して環境が正しく設定されていることを確認

```bash
uvx nox
```

## 開発ワークフロー

### 1. ブランチ作成

```bash
git checkout -b feature/new-feature
# または
git checkout -b fix/bug-description
```

### ブランチ命名規則

- `feature/` - 新機能
- `fix/` - バグ修正
- `docs/` - ドキュメント改善
- `test/` - テスト改善
- `refactor/` - リファクタリング
- `perf/` - パフォーマンス改善

### 2. コード実装

#### コーディング規約

- **PEP 8** に準拠
- **型ヒント** を必須とする(mypy準拠)
- **コメント** を主要機能に追加
- **docstring** はGoogleスタイルを使用

```python
def example_function(param: str) -> dict[str, Any]:
    """関数の説明文.

    Args:
        param: パラメータの説明

    Returns:
        戻り値の説明

    Raises:
        ValueError: エラーが発生する条件
    """
    pass
```

#### コード品質チェック

開発中に以下のコマンドを定期的に実行:

```bash
# フォーマット
uvx nox -s format

# リント
uvx nox -s lint

# 型チェック
uvx nox -s typecheck

# テスト実行
uvx nox -s test
```

### 3. テスト

#### テスト要件

- 新しいコードには対応するテストを追加
- 既存のテストが全て通ること
- カバレッジが80%以上を維持

#### テスト実行

```bash
# 全テスト実行
uvx nox -s test

# 特定のファイルのみ
uvx nox -s test tests/test_specific.py

# カバレッジ付き
uvx nox coverage
```

#### テスト分類

- **単体テスト**: 個別のクラス・関数のテスト
- **統合テスト**: 複数コンポーネント間のテスト
- **モックテスト**: 外部サービス依存のテスト

### 4. コミット

#### コミットメッセージ規約

コミットメッセージは以下の形式に従ってください:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type(必須):**
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント変更のみ
- `style`: フォーマット変更(機能に影響しない)
- `refactor`: リファクタリング
- `test`: テストの追加・修正
- `chore`: ビルド，ツール設定など

**例:**
```
feat(geoip): MaxMindクライアントのタイムアウト設定を追加

GeoIPクライアントでネットワークタイムアウトを設定できるように改善．
デフォルトは30秒とし，環境変数で変更可能．

Fixes #123
```

### 5. プルリクエスト

#### プルリクエスト作成前チェックリスト

- [ ] すべてのテストが通る
- [ ] リント・型チェックでエラーがない
- [ ] カバレッジが下がっていない
- [ ] ドキュメントが更新されている
- [ ] CHANGELOG.md が更新されている(重要な変更の場合)

#### プルリクエストテンプレート

```markdown
## 概要
この PR の目的と変更内容を簡潔に説明

## 変更内容
- 変更点 1
- 変更点 2

## 破壊的変更
あれば記載

## テスト
- [ ] 新しいテストを追加した
- [ ] 既存のテストが全て通る
- [ ] 手動テストを実施した

## チェックリスト
- [ ] リント・型チェックでエラーがない
- [ ] ドキュメントを更新した
- [ ] セキュリティ影響を検討した

## 関連Issue
Closes #issue_number
```

## リリースプロセス

### バージョニング

[Semantic Versioning](https://semver.org/lang/ja/) に従います:

- **MAJOR**: 破壊的変更
- **MINOR**: 新機能追加(後方互換性あり)
- **PATCH**: バグ修正

### リリース手順

1. バージョン更新
2. CHANGELOG.md更新
3. CI/CD により自動的にGitHub Release，PyPI，TestPyPIに公開

## 質問・サポート

- **一般的な質問**: [GitHub Discussions](https://github.com/yourusername/ipinfo-geoip/discussions)
- **バグ報告**: [GitHub Issues](https://github.com/yourusername/ipinfo-geoip/issues)
- **セキュリティ**: [SECURITY.md](SECURITY.md) を参照

## 謝辞

あなたの貢献はこのプロジェクトをより良いものにするために大変重要です．貢献いただいたすべての方に感謝いたします．

## 参考リソース

- [Python開発ガイド](https://docs.python.org/ja/3/tutorial/)
- [pytest ドキュメント](https://docs.pytest.org/)
- [mypy ドキュメント](https://mypy.readthedocs.io/)
- [ruff ドキュメント](https://docs.astral.sh/ruff/)
- [nox ドキュメント](https://nox.thea.codes/)
