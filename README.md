# 🚀 AI Development Environment

**スマホ完結型AI開発環境** - Manusを司令塔として、Claude Code、Gemini CLI、Codex CLIを連携させる効率的な開発環境です。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 概要

この環境は、**Manusのクレジット消費を抑えながら**、複数のAIツールを活用して高品質な開発を行うことを目的としています。

### コンセプト

```
┌─────────────────────────────────────────────────────────────┐
│                    ユーザー（スマホ）                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Manus（司令塔）                         │
│  ・タスク受付・分析                                          │
│  ・適切なAI CLIへの委譲指示                                   │
│  ・結果の確認・報告                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     delegate.py (振り分け)                   │
│              タスクタイプ判定 → 最適なAI選択                   │
│              推奨スキルの自動適用                              │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │ Claude Code │     │ Gemini CLI  │     │  Codex CLI  │
   │  (開発全般)  │     │ (質問/文書) │     │ (レビュー)  │
   └─────────────┘     └─────────────┘     └─────────────┘
```

## 📦 インストール

### 1. リポジトリをクローン

```bash
gh repo clone Rio2Ryo/ai-dev-environment
cd ai-dev-environment
```

### 2. AI CLIツールのインストール

```bash
# Claude Code
curl -fsSL https://claude.ai/install.sh | bash

# Gemini CLI
npm install -g @google/gemini-cli

# Codex CLI
npm install -g @openai/codex

# Python SDK（オプション）
pip install anthropic openai google-genai xai-sdk
```

### 3. スキルの配置（オプション）

```bash
# Claude Codeでスキルを使用する場合
cp -r skills/* ~/.claude/skills/
```

## 🔧 使い方

### Manusへの指示方法（重要）

Manusに以下のように指示してください：

> 「`ai-dev-environment`をクローンして、`delegate.py`を使って**Claude Codeに**[タスク内容]を実行させてください」

これにより、Manusは司令塔として機能し、実際の開発作業はClaude Codeに委譲されます。

### コマンド例

```bash
# Claude Codeに開発タスクを委譲
python3 scripts/delegate.py claude "ログイン機能を実装してください"

# Geminiに簡単な質問を委譲（無料枠活用）
python3 scripts/delegate.py gemini "Pythonでリストをソートする方法"

# Codexにコードレビューを委譲
python3 scripts/delegate.py codex --review

# 自動選択モード（タスクタイプとスキルを自動判定）
python3 scripts/delegate.py auto "タスク内容"

# スキルを指定して実行
python3 scripts/delegate.py claude "Reactコンポーネントを作成" \
  --skill frontend-design --skill react-best-practices

# フォールバック付き（失敗時に別のCLIで再試行）
python3 scripts/delegate.py auto "タスク内容" --fallback

# 統合ワークフロー（Git連携・通知付き）
python3 scripts/dev.py "新機能を実装" --notify --commit --push

# 利用可能なスキル一覧
python3 scripts/delegate.py --list-skills
```

## 📚 スキル

高品質な開発を支援するスキル（ガイドライン）が含まれています：

| スキル | 説明 | 推奨用途 |
|--------|------|----------|
| `frontend-design` | 高品質なフロントエンドUI設計 | UI/コンポーネント作成 |
| `react-best-practices` | React/Next.jsパフォーマンス最適化（45+ルール） | React開発全般 |
| `systematic-debugging` | 体系的デバッグ手法 | バグ修正 |
| `code-review` | コードレビューガイドライン | PR/コードレビュー |
| `git-workflow` | Gitワークフローベストプラクティス | バージョン管理 |
| `webapp-testing` | Playwrightによるテスト | E2Eテスト |
| `mcp-builder` | MCPサーバー開発ガイド | MCP開発 |

### 自動スキル選択

タスクタイプに応じて、推奨スキルが自動的に適用されます：

| タスクタイプ | 自動適用スキル |
|-------------|---------------|
| フロントエンド開発 | `frontend-design`, `react-best-practices` |
| バグ修正 | `systematic-debugging` |
| コードレビュー | `code-review` |
| テスト作成 | `webapp-testing` |

## 💰 コスト最適化

タスクは自動的に最適なAIに振り分けられます：

| タスクタイプ | 推奨AI | 理由 |
|-------------|--------|------|
| 開発・実装 | Claude Code | 高品質なコード生成 |
| バグ修正 | Claude Code | 複雑な問題解決 |
| リファクタリング | Claude Code | コード理解力 |
| 簡単な質問 | Gemini | **無料枠あり（1,000リクエスト/日）** |
| ドキュメント生成 | Gemini | コスト効率 |
| コードレビュー | Codex | 専門機能 |

### コスト比較

| CLI | 料金 | 用途 |
|-----|------|------|
| Gemini CLI | **無料**（1,000リクエスト/日） | 簡単な質問、ドキュメント |
| Claude Code | 約$0.03/リクエスト | メイン開発 |
| Codex CLI | OpenAI料金 | コードレビュー |

## 📁 プロジェクト構造

```
ai-dev-environment/
├── scripts/                    # 実行スクリプト
│   ├── delegate.py             # タスク委譲（メイン）
│   ├── dev.py                  # 統合ワークフロー
│   ├── notify.py               # LINE通知
│   ├── ai_orchestrator.py      # AIオーケストレーター
│   ├── frontend_helper.py      # フロントエンド支援
│   └── debug_helper.py         # デバッグ支援
├── skills/                     # Claude Code Skills
│   ├── frontend-design/
│   ├── react-best-practices/
│   ├── systematic-debugging/
│   ├── code-review/
│   ├── git-workflow/
│   ├── webapp-testing/
│   └── mcp-builder/
├── config/                     # 設定ファイル
├── docs/                       # ドキュメント
│   ├── README.md               # 詳細マニュアル
│   └── WORKFLOW.md             # ワークフロー設計
├── CLAUDE.md                   # Claude Code用コンテキスト
├── GEMINI.md                   # Gemini CLI用コンテキスト
└── README.md                   # このファイル
```

## 🔄 ワークフロー例

### 1. 新機能開発

```bash
# Manusへの指示
「ai-dev-environmentをクローンして、delegate.pyを使ってClaude Codeに
ユーザー認証機能を実装させてください。frontend-designスキルを使用してください。」

# 実行されるコマンド
python3 scripts/delegate.py claude "ユーザー認証機能を実装" \
  --skill frontend-design
```

### 2. バグ修正

```bash
# Manusへの指示
「delegate.pyを使ってClaude Codeにこのエラーを修正させてください：
[エラーメッセージ]」

# 実行されるコマンド（自動でsystematic-debuggingスキルが適用）
python3 scripts/delegate.py auto "このエラーを修正: [エラー内容]"
```

### 3. 簡単な質問（無料）

```bash
# Manusへの指示
「delegate.pyを使ってGeminiにPythonの質問をしてください」

# 実行されるコマンド
python3 scripts/delegate.py gemini "Pythonでファイルを読み込む方法"
```

### 4. 統合ワークフロー

```bash
# 開発 → コミット → プッシュ → LINE通知
python3 scripts/dev.py "ダッシュボード機能を追加" \
  --branch feature/dashboard \
  --skill frontend-design \
  --commit --push --notify
```

## 📱 LINE通知

開発完了時にLINE通知を受け取ることができます：

```bash
# 通知付きで開発
python3 scripts/dev.py "タスク内容" --notify

# 手動で通知
python3 scripts/notify.py "開発が完了しました" --title "完了通知" --status success

# Flex Message形式
python3 scripts/notify.py "詳細レポート" --flex --title "日次レポート"
```

## 🛠️ カスタマイズ

### 新しいスキルの追加

1. `skills/`ディレクトリに新しいフォルダを作成
2. `SKILL.md`ファイルを作成（フロントマター形式）

```markdown
---
name: my-skill
description: スキルの説明
---

# スキル名

ここにガイドラインを記述...
```

### タスク振り分けルールの変更

`scripts/delegate.py`の`TaskDelegator`クラスを編集：

```python
self.task_cli_map = {
    TaskType.DEVELOPMENT: CLI.CLAUDE,
    TaskType.QUESTION: CLI.GEMINI,
    # カスタマイズ...
}
```

## 📄 ライセンス

MIT License

## 🤝 貢献

プルリクエストを歓迎します。大きな変更を行う場合は、まずissueを開いて議論してください。

---

**Made with ❤️ for efficient AI-powered development**
