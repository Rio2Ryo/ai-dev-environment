# AI Development Environment - Claude Code Project Context

このプロジェクトは、スマホ完結型AI開発環境です。Manusを司令塔として、Claude Code、Gemini CLI、Codex CLIを連携させて効率的な開発を行います。

## 重要: Manusとの連携

**Manusは「司令塔」として機能し、実際の開発作業はこのClaude Codeに委譲されます。**

Manusからの指示例：
```
「ai-dev-environmentをクローンして、delegate.pyを使ってClaude Codeに
[タスク内容]を実行させてください」
```

## プロジェクト構造

```
ai-dev-environment/
├── scripts/           # Pythonスクリプト
│   ├── delegate.py    # タスク委譲スクリプト（メイン）
│   ├── dev.py         # 統合開発ワークフロー
│   ├── notify.py      # LINE通知スクリプト
│   ├── ai_orchestrator.py    # AIオーケストレーター
│   ├── frontend_helper.py    # フロントエンド開発ヘルパー
│   └── debug_helper.py       # デバッグヘルパー
├── skills/            # Claude Code Skills
│   ├── frontend-design/      # 高品質UIデザイン
│   ├── react-best-practices/ # React/Next.js最適化
│   ├── systematic-debugging/ # 体系的デバッグ
│   ├── code-review/          # コードレビュー
│   ├── git-workflow/         # Gitワークフロー
│   ├── webapp-testing/       # Playwrightテスト
│   └── mcp-builder/          # MCPサーバー開発
├── config/            # 設定ファイル
├── docs/              # ドキュメント
├── CLAUDE.md          # このファイル
└── GEMINI.md          # Gemini CLI用コンテキスト
```

## 開発ガイドライン

### コーディング規約
- Python 3.11+を使用
- 型ヒントを必ず使用
- docstringはGoogle形式
- 日本語コメントOK

### ファイル操作
- 新規ファイルは適切なディレクトリに配置
- スクリプトは`scripts/`に
- スキルは`skills/`に
- ドキュメントは`docs/`に

### テスト
- 変更後は必ず動作確認
- エラーハンドリングを適切に実装

## 利用可能なスキル

| スキル名 | 説明 | 用途 |
|---------|------|------|
| frontend-design | 高品質なフロントエンドUI設計 | UI/コンポーネント作成 |
| react-best-practices | React/Next.jsパフォーマンス最適化 | React開発全般 |
| systematic-debugging | 体系的デバッグ手法 | バグ修正 |
| code-review | コードレビューガイドライン | PR/コードレビュー |
| git-workflow | Gitワークフローベストプラクティス | バージョン管理 |
| webapp-testing | Playwrightによるテスト | E2Eテスト |
| mcp-builder | MCPサーバー開発ガイド | MCP開発 |

## よく使うコマンド

```bash
# タスク委譲（基本）
python3 scripts/delegate.py claude "タスク内容"
python3 scripts/delegate.py gemini "簡単な質問"
python3 scripts/delegate.py codex --review

# スキル指定
python3 scripts/delegate.py claude "Reactコンポーネント作成" \
  --skill frontend-design --skill react-best-practices

# 自動選択（タスクタイプとスキルを自動判定）
python3 scripts/delegate.py auto "タスク内容"

# 統合ワークフロー（Git連携・通知付き）
python3 scripts/dev.py "新機能を実装" --notify --commit

# 利用可能なスキル一覧
python3 scripts/delegate.py --list-skills
```

## コスト最適化

タスクは自動的に最適なAIに振り分けられます：

| タスクタイプ | 推奨AI | 理由 |
|-------------|--------|------|
| 開発・実装 | Claude Code | 高品質なコード生成 |
| バグ修正 | Claude Code | 複雑な問題解決 |
| 簡単な質問 | Gemini | 無料枠あり |
| ドキュメント | Gemini | コスト効率 |
| コードレビュー | Codex | 専門機能 |

## 注意事項

- このプロジェクトはManusから委譲されたタスクを実行するために使用されます
- コスト効率を意識し、簡単なタスクはGeminiに委譲することを推奨
- 大規模な変更を行う場合は、事前にManusに確認を取ってください
- スキルを活用することで高品質な出力を実現できます
