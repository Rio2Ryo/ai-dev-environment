# AI Development Environment - Claude Code Project Context

このプロジェクトは、スマホ完結型AI開発環境です。Manusを司令塔として、Claude Code、Gemini CLI、Codex CLIを連携させて効率的な開発を行います。

## プロジェクト構造

```
ai-dev-environment/
├── scripts/           # Pythonスクリプト
│   ├── delegate.py           # タスク委譲スクリプト（メイン）
│   ├── ai_orchestrator.py    # AIオーケストレーター
│   ├── frontend_helper.py    # フロントエンド開発ヘルパー
│   └── debug_helper.py       # デバッグヘルパー
├── skills/            # Claude Code Skills
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

以下のスキルが`~/.claude/skills/`に配置されています：

1. **frontend-design** - 高品質UIデザイン
2. **react-best-practices** - Reactベストプラクティス
3. **systematic-debugging** - 体系的デバッグ
4. **mcp-integration** - MCP連携
5. **ai-orchestration** - AI連携戦略

## よく使うコマンド

```bash
# タスク委譲
python3 scripts/delegate.py claude "タスク内容"
python3 scripts/delegate.py gemini "簡単な質問"
python3 scripts/delegate.py codex --review

# 自動選択
python3 scripts/delegate.py auto "タスク内容"

# フォールバック付き
python3 scripts/delegate.py auto "タスク内容" --fallback
```

## 注意事項

- このプロジェクトはManusから委譲されたタスクを実行するために使用されます
- コスト効率を意識し、簡単なタスクはGeminiに委譲することを推奨
- 大規模な変更を行う場合は、事前にManusに確認を取ってください
