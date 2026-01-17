# スマホ完結型AI開発環境 - ユーザーマニュアル

## 1. 概要

このドキュメントは、構築された「スマホ完結型AI開発環境」のセットアップ、アーキテクチャ、および使用方法について説明します。この環境は、Manusをハブとして、Claude、GPT、Gemini、Grokなどの複数のAIモデルを効率的に活用し、特にフロントエンド開発の品質と効率を向上させることを目的としています。

## 2. 環境アーキテクチャ

この環境は、以下のコンポーネントで構成されています。

- **AIオーケストレーター**: タスクの内容に応じて最適なAIモデルを自動的に選択し、API呼び出しを実行する中核スクリプト。
- **ヘルパースクリプト**: 特定のタスク（フロントエンド開発、デバッグ）に特化した高レベルの機能を提供。
- **Claude Code Skills**: 高品質な成果物を生成するためのベストプラクティスや設計原則をAIに提供するカスタムスキルセット。
- **CLIツール & SDK**: 各AIサービスと対話するための基本的なツール群。

```mermaid
graph TD
    A[ユーザー (Manus経由)] --> B{AIオーケストレーター};
    B -->|タスク分析| C{モデル選択ロジック};
    C --> D[Gemini];
    C --> E[Claude];
    C --> F[GPT/Codex];
    C --> G[Grok];
    
    H[ヘルパースクリプト] --> B;
    I[Claude Code Skills] --> E;
    
    subgraph "AIサービス"
        D;
        E;
        F;
        G;
    end

    subgraph "開発環境"
        B;
        C;
        H;
        I;
    end
```

## 3. インストール済みツール

### Python SDK

| ライブラリ | バージョン | 説明 |
| :--- | :--- | :--- |
| `anthropic` | 0.76.0 | Anthropic (Claude) APIクライアント |
| `openai` | 2.3.0 | OpenAI (GPT, Codex) APIクライアント |
| `google-genai` | 1.59.0 | Google (Gemini) APIクライアント |
| `xai-sdk` | (最新) | xAI (Grok) APIクライアント |

### CLIツール

| ツール | バージョン | 説明 |
| :--- | :--- | :--- |
| `claude` | 2.1.11 | Claude Code公式CLI |
| `gemini` | 0.24.0 | Gemini公式CLI |
| `codex` | 0.87.0 | OpenAI Codex公式CLI |

## 4. Claude Code Skills

`~/.claude/skills/` ディレクトリに以下のカスタムスキルが導入されています。これらは、特にClaudeを使用する際に、高品質な出力を保証するためのガイドとして機能します。

- **frontend-design.md**: 汎用的な「AIっぽさ」を排し、本番品質のフロントエンドUIを設計するための原則。
- **react-best-practices.md**: モダンなReactアプリケーションを構築するためのベストプラクティス集。
- **systematic-debugging.md**: 根本原因の特定を重視した、4段階の体系的デバッグ手法。
- **mcp-integration.md**: 外部ツールと連携するためのMCPサーバー構築ガイド。
- **ai-orchestration.md**: コストとパフォーマンスを最適化するための複数AIモデル連携戦略。

## 5. 主要スクリプトと使い方

すべてのスクリプトは `/home/ubuntu/ai-dev-environment/scripts/` にあります。

### 5.1. AIオーケストレーター (`ai_orchestrator.py`)

このスクリプトは、プロンプトの内容に応じて最適なAIを自動で選択します。

**使用例:**

```bash
# 利用可能なモデルを確認
python3 scripts/ai_orchestrator.py --check

# 簡単なコード生成（Geminiが優先される）
python3 scripts/ai_orchestrator.py "Pythonでフィボナッチ数列を計算する関数を書いてください"

# タスクタイプを明示して実行
python3 scripts/ai_orchestrator.py --task complex_algorithm "クイックソートを実装してください"
```

### 5.2. フロントエンドヘルパー (`frontend_helper.py`)

フロントエンド開発に特化したヘルパーです。`frontend-design`と`react-best-practices`スキルを活用します。

**使用例:**

```bash
# Reactコンポーネントを生成
python3 scripts/frontend_helper.py generate "ダークモード切り替え機能付きのレスポンシブなログインフォーム"

# UIコードをレビュー
#（例: component.tsx ファイルを作成してから実行）
python3 scripts/frontend_helper.py review path/to/your/component.tsx

# デザイン提案
python3 scripts/frontend_helper.py design "eコマースサイトの商品詳細ページ"
```

### 5.3. デバッグヘルパー (`debug_helper.py`)

`systematic-debugging`スキルに基づき、バグ解決を支援します。

**使用例:**

```bash
# エラーメッセージを分析
python3 scripts/debug_helper.py analyze "TypeError: Cannot read properties of undefined (reading 'map')"

# バグの症状から仮説を生成
python3 scripts/debug_helper.py hypothesis "ユーザーがボタンをクリックしても何も起こらない"

# 修正コードを検証
python3 scripts/debug_helper.py verify "ボタンのクリックイベントが発火しない問題" "onClickハンドラを修正" path/to/fixed_code.js
```

## 6. 今後の拡張

- **LINE通知**: `config/settings.json` の設定に基づき、LINE MCPと連携して開発の進捗やエラーを通知する機能を追加できます。
- **カスタムスキルの追加**: `~/.claude/skills/` に新しいMarkdownファイルを追加することで、独自のスキルを簡単に拡張できます。
- **Grok API連携**: 現在オーケストレーターはGrokのPython SDKを直接呼び出していませんが、`XAI_API_KEY`が設定されているため、`xai-sdk`を利用したGrok呼び出し機能を追加することが可能です。
