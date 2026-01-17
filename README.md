# AI Development Environment

スマホ完結型AI開発環境 - **Manusを司令塔、Claude Codeを実行部隊**として効率的に開発するためのツールキット

## コンセプト

このプロジェクトは、Manusのクレジット消費を最小限に抑えながら、高品質な開発を実現するためのワークフローを提供します。

```
┌─────────────────────────────────────────────────────────────┐
│                    ユーザー（スマホ）                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Manus（司令塔）                         │
│  ・タスク受付・分析                                          │
│  ・適切なAI CLIへの委譲                                      │
│  ・結果の確認・報告                                          │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Claude Code    │ │   Gemini CLI    │ │   Codex CLI     │
│  （メイン開発）  │ │ （簡単なタスク） │ │ （コードレビュー）│
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## 特徴

- **タスク委譲**: Manusから各AI CLIへタスクを自動振り分け
- **コスト最適化**: 簡単なタスクはGemini（無料枠）、開発はClaude Code
- **フォールバック**: 失敗時に自動で別のCLIに切り替え
- **Claude Code Skills**: 高品質な成果物のためのカスタムスキル

## クイックスタート

### 1. リポジトリをクローン

```bash
gh repo clone Rio2Ryo/ai-dev-environment
cd ai-dev-environment
```

### 2. 依存関係をインストール

```bash
# Python SDK
pip install anthropic openai google-genai xai-sdk

# CLI Tools
npm install -g @google/gemini-cli @openai/codex
curl -fsSL https://claude.ai/install.sh | bash
```

### 3. スキルをコピー

```bash
cp -r skills/* ~/.claude/skills/
```

## 使い方

### タスク委譲スクリプト（メイン）

```bash
# Claude Codeに開発タスクを委譲
python3 scripts/delegate.py claude "ログイン機能を実装してください"

# Geminiに簡単な質問を委譲（無料枠活用）
python3 scripts/delegate.py gemini "Pythonでリストをソートする方法"

# Codexにコードレビューを委譲
python3 scripts/delegate.py codex --review

# 自動選択モード（タスク内容から最適なCLIを選択）
python3 scripts/delegate.py auto "タスク内容"

# フォールバック付き（失敗時に別のCLIで再試行）
python3 scripts/delegate.py auto "タスク内容" --fallback

# 予算上限を設定（Claude Codeのみ）
python3 scripts/delegate.py claude "タスク" --max-budget 0.10
```

### タスク振り分けルール

| タスク種別 | 自動選択されるCLI | 理由 |
|-----------|-----------------|------|
| 新機能開発 | Claude Code | 高品質なコード生成 |
| バグ修正 | Claude Code | デバッグ能力 |
| 簡単な質問 | Gemini CLI | 無料枠活用 |
| コードレビュー | Codex CLI | 専用機能 |
| ドキュメント | Gemini CLI | コスト効率 |

## ディレクトリ構成

```
ai-dev-environment/
├── scripts/
│   ├── delegate.py           # タスク委譲スクリプト（メイン）
│   ├── ai_orchestrator.py    # AIオーケストレーター
│   ├── frontend_helper.py    # フロントエンド開発ヘルパー
│   └── debug_helper.py       # デバッグヘルパー
├── skills/                   # Claude Code Skills
│   ├── frontend-design.md
│   ├── react-best-practices.md
│   ├── systematic-debugging.md
│   ├── mcp-integration.md
│   └── ai-orchestration.md
├── config/
│   └── settings.json
├── docs/
│   ├── README.md             # 詳細マニュアル
│   └── WORKFLOW.md           # ワークフロー設計
├── CLAUDE.md                 # Claude Code用コンテキスト
├── GEMINI.md                 # Gemini CLI用コンテキスト
└── README.md                 # このファイル
```

## Manusでの使い方

Manusに以下のように指示することで、Claude Codeに開発を委譲できます：

```
「ai-dev-environmentをクローンして、delegate.pyを使って
Claude Codeにログイン機能を実装させてください」
```

Manusは：
1. リポジトリをクローン
2. `delegate.py`でClaude Codeにタスクを委譲
3. 結果を確認して報告

これにより、Manusのクレジット消費を最小限に抑えながら、Claude Codeの開発能力を活用できます。

## コスト比較

| CLI | 料金 | 用途 |
|-----|------|------|
| Gemini CLI | 無料（1,000リクエスト/日） | 簡単な質問、ドキュメント |
| Claude Code | 約$0.03/リクエスト | メイン開発 |
| Codex CLI | OpenAI料金 | コードレビュー |

## ライセンス

MIT License
