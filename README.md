# 🚀 AI Development Environment

**スマホ完結型AI開発環境** - Manusを司令塔・品質管理役として、Claude Codeに開発を委譲する効率的な開発環境です。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 コンセプト

この環境は、**Manusのクレジット消費を抑えながら**、高品質な開発を行うことを目的としています。

**重要な原則**: Manusは自分でコードを書かず、**Claude Codeに開発を委譲**します。

```
┌─────────────────────────────────────────────────────────────┐
│                    ユーザー（スマホ）                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Manus（司令塔・品質管理役）                      │
│  ・タスク受付・分解                                          │
│  ・Claude Codeへの開発委譲                                   │
│  ・ブラウザで成果物を確認                                     │
│  ・品質向上のためのフィードバック                             │
│  ・最終報告                                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Claude Code（実装担当）                         │
│  ・実際のコーディング                                        │
│  ・Manusからのフィードバックに基づく修正                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    高品質な成果物 ✨
```

## 📱 使い方

### Manusへの指示方法

以下のようにManusに指示してください：

```
ai-dev-environmentをクローンして、Claude Codeに「[タスク内容]」を実行させてください。
完了したらブラウザで確認し、品質に問題があれば修正を指示してください。
```

### 具体例

#### 新規開発

```
ai-dev-environmentをクローンして、Claude Codeに以下を実行させてください：

「React + TypeScriptでシンプルなTodoアプリを作成してください。
frontend-designスキルを使用してください。」

完了したらブラウザで動作確認し、品質に問題があれば修正を指示してください。
最終的に満足できる品質になったら報告してください。
```

#### バグ修正

```
ai-dev-environmentをクローンして、Claude Codeに以下のバグ修正を実行させてください：

「ボタンをクリックしても反応しない問題を修正してください」

修正後、ブラウザで動作確認してください。
```

## 📦 インストール

### 1. リポジトリをクローン

```bash
gh repo clone Rio2Ryo/ai-dev-environment
cd ai-dev-environment
```

### 2. AI CLIツールのインストール

```bash
# Claude Code（必須）
curl -fsSL https://claude.ai/install.sh | bash

# Gemini CLI（オプション - 無料枠活用）
npm install -g @google/gemini-cli

# Codex CLI（オプション - コードレビュー）
npm install -g @openai/codex
```

## 🔧 スクリプト

### delegate.py - タスク委譲

Claude Codeにタスクを委譲するメインスクリプト：

```bash
# Claude Codeに開発タスクを委譲
python3 scripts/delegate.py claude "ログイン機能を実装してください"

# スキルを指定
python3 scripts/delegate.py claude "Reactコンポーネントを作成" \
  --skill frontend-design --skill react-best-practices

# 作業ディレクトリを指定
python3 scripts/delegate.py claude "バグを修正" -C ./project-dir
```

### review.py - 品質管理

成果物を確認し、フィードバックを送るスクリプト：

```bash
# 開発サーバーを起動
python3 scripts/review.py serve ./project-dir

# フィードバックを送信
python3 scripts/review.py feedback "ボタンのホバー効果が動作しない" -C ./project-dir

# 品質チェックリストを表示
python3 scripts/review.py checklist ./project-dir
```

### dev.py - 統合ワークフロー

開発からGit操作、通知までを一括実行：

```bash
python3 scripts/dev.py "新機能を実装" --commit --push --notify
```

## 📚 スキル

高品質な開発を支援するスキル（ガイドライン）：

| スキル | 説明 | 推奨用途 |
|--------|------|----------|
| `frontend-design` | 高品質なフロントエンドUI設計 | UI/コンポーネント作成 |
| `react-best-practices` | React/Next.jsパフォーマンス最適化 | React開発全般 |
| `systematic-debugging` | 体系的デバッグ手法 | バグ修正 |
| `code-review` | コードレビューガイドライン | PR/コードレビュー |
| `git-workflow` | Gitワークフローベストプラクティス | バージョン管理 |
| `webapp-testing` | Playwrightによるテスト | E2Eテスト |
| `mcp-builder` | MCPサーバー開発ガイド | MCP開発 |

## 📁 プロジェクト構造

```
ai-dev-environment/
├── scripts/                    # 実行スクリプト
│   ├── delegate.py             # タスク委譲（メイン）
│   ├── review.py               # 品質管理・レビュー
│   ├── dev.py                  # 統合ワークフロー
│   └── notify.py               # LINE通知
├── skills/                     # Claude Code Skills
├── examples/                   # サンプルプロジェクト
├── docs/                       # ドキュメント
│   ├── QUICKSTART.md           # クイックスタート
│   ├── PROMPT_TEMPLATES.md     # 指示テンプレート
│   ├── ARCHITECTURE.md         # アーキテクチャ設計
│   └── TROUBLESHOOTING.md      # トラブルシューティング
├── CLAUDE.md                   # Claude Code用コンテキスト
├── MANUS_RULES.md              # Manusのワークフロールール
└── README.md                   # このファイル
```

## 🔄 ワークフロー詳細

### Step 1: タスク受付

ユーザーがManusに開発タスクを依頼します。

### Step 2: Claude Codeに委譲

Manusは `delegate.py` を使ってClaude Codeにタスクを委譲します。
**Manusは自分でコードを書きません。**

```bash
python3 scripts/delegate.py claude "タスクの詳細" --skill frontend-design
```

### Step 3: 成果物の確認

Claude Codeが完了したら、Manusがブラウザで成果物を確認します。

```bash
python3 scripts/review.py serve ./project-dir
```

### Step 4: フィードバック

問題を発見したら、Claude Codeに修正を指示します。

```bash
python3 scripts/review.py feedback "問題の詳細" -C ./project-dir
```

### Step 5: 繰り返し

品質が満足できるレベルになるまで、Step 3-4を繰り返します。

### Step 6: 完了報告

最終的な成果物をユーザーに報告します。

## 💡 指示テンプレート

詳細な指示テンプレートは [docs/PROMPT_TEMPLATES.md](./docs/PROMPT_TEMPLATES.md) を参照してください。

### クイックコピー

```
ai-dev-environmentをクローンして、Claude Codeに「[タスク]」を実行させてください。
完了したらブラウザで確認し、問題があれば修正を指示してください。
```

## 📄 ライセンス

MIT License

---

**Made with ❤️ for efficient AI-powered development**
