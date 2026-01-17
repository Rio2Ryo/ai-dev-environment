# AI Development Environment

スマホ完結型AI開発環境 - Manusをハブとして複数のAIモデルを効率的に活用するためのツールキット

## 概要

この環境は、Claude、GPT、Gemini、Grokなどの複数のAIモデルを統合し、タスクに応じて最適なモデルを自動選択するオーケストレーションシステムを提供します。特にフロントエンド開発の品質向上に焦点を当てたClaude Code Skillsを含んでいます。

## 特徴

- **AIオーケストレーター**: プロンプト内容を分析し、最適なAIモデルを自動選択
- **フロントエンド開発支援**: 高品質なUIコンポーネント生成、コードレビュー
- **体系的デバッグ支援**: 4フェーズのデバッグ手法に基づくバグ解決支援
- **Claude Code Skills**: フロントエンドデザイン、React、デバッグなどのカスタムスキル

## クイックスタート

### 1. リポジトリをクローン

```bash
gh repo clone YOUR_USERNAME/ai-dev-environment
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

### 3. 環境変数を設定

```bash
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
export GEMINI_API_KEY="your-key"
export XAI_API_KEY="your-key"
```

### 4. スキルをコピー

```bash
cp -r skills/* ~/.claude/skills/
```

### 5. 使用開始

```bash
# 利用可能なモデルを確認
python3 scripts/ai_orchestrator.py --check

# コード生成
python3 scripts/ai_orchestrator.py "Reactでログインフォームを作成してください"

# フロントエンド開発
python3 scripts/frontend_helper.py generate "ダークモード対応のナビゲーションバー"

# デバッグ支援
python3 scripts/debug_helper.py analyze "TypeError: Cannot read property 'map' of undefined"
```

## ディレクトリ構成

```
ai-dev-environment/
├── scripts/           # Pythonスクリプト
│   ├── ai_orchestrator.py    # AIオーケストレーター
│   ├── frontend_helper.py    # フロントエンド開発ヘルパー
│   └── debug_helper.py       # デバッグヘルパー
├── skills/            # Claude Code Skills（~/.claude/skills/にコピー）
├── config/            # 設定ファイル
│   └── settings.json  # 環境設定
├── docs/              # ドキュメント
│   └── README.md      # 詳細マニュアル
├── GEMINI.md          # Gemini CLI用プロジェクトコンテキスト
└── README.md          # このファイル
```

## タスク別モデル選択

| タスク | 優先モデル | フォールバック |
|--------|-----------|--------------|
| 簡単なコード生成 | Gemini | Grok Code Fast |
| 複雑なアルゴリズム | GPT-5 | Claude Opus |
| コードレビュー | Grok Code Fast | Codex |
| デバッグ | Claude | Gemini |
| フロントエンド | Claude | GPT-5 |
| ドキュメント | Gemini | GPT-4o |

## ライセンス

MIT License
