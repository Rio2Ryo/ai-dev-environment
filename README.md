# 🚀 AI Development Environment

**スマホ完結型AI開発環境** - Manusを司令塔として、Claude Codeに開発を委譲する環境です。

## 🎯 コンセプト

```
ユーザー: 「〇〇を開発して」
    │
    ▼
Manus（司令塔・品質管理）
    │
    ▼
Claude Code（実装担当）
    │
    ▼
高品質な成果物
```

**Manusはコードを書きません。Claude Codeに委譲します。**

## 📱 使い方

1. このリポジトリをクローン
2. 普通にManusに開発を依頼
3. Manusが自動的にClaude Codeに委譲
4. Manusがブラウザで品質確認
5. 必要に応じて修正指示
6. 完成

## 📦 セットアップ

```bash
# クローン
gh repo clone Rio2Ryo/ai-dev-environment
cd ai-dev-environment

# Claude Code（必須）
curl -fsSL https://claude.ai/install.sh | bash
```

## 📁 構造

```
ai-dev-environment/
├── MANUS.md          # ← Manusの役割定義（重要）
├── CLAUDE.md         # Claude Code用コンテキスト
├── scripts/          # 自動化スクリプト
│   ├── delegate.py   # タスク委譲
│   └── review.py     # 品質管理
├── skills/           # Claude Code Skills
└── docs/             # ドキュメント
```

## 🔑 重要ファイル

- **MANUS.md** - Manusの役割を定義。Manusはこれを読んで行動する
- **CLAUDE.md** - Claude Codeのコンテキスト
- **delegate.py** - Claude Codeにタスクを委譲するスクリプト
- **review.py** - 品質確認・フィードバック用スクリプト

## 📄 ライセンス

MIT License
