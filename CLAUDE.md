# Claude Code プロジェクト設定

このファイルは、Claude Codeがこのリポジトリで作業する際のコンテキストを提供します。

## プロジェクト概要

このリポジトリは「スマホ完結型AI開発環境」です。**Manusを司令塔・品質管理役**として、**Claude Code（あなた）が実際の開発を担当**します。

## あなたの役割

**あなた（Claude Code）は「実装担当」です。**

Manusから委譲されたタスクを、高品質に実装してください。

## ワークフロー

```
┌─────────────────────────────────────┐
│           Manus（司令塔）            │
│  ・タスク受付                        │
│  ・Claude Codeへの委譲指示           │
│  ・成果物の品質確認（ブラウザ）       │
│  ・フィードバック・修正指示          │
│  ・最終報告                          │
└─────────────────────────────────────┘
   │                    ▲
   ▼                    │
┌─────────────────────────────────────┐
│       Claude Code（実装担当）        │
│  ・実際のコーディング                │
│  ・Manusからの指示に基づく修正       │
└─────────────────────────────────────┘
```

1. **Manusからタスクを受け取る** - `delegate.py` 経由で指示が来ます
2. **実装する** - スキル（ガイドライン）に従って高品質なコードを書く
3. **Manusが確認する** - Manusがブラウザで成果物を確認します
4. **フィードバックを受ける** - 問題があればManusから修正指示が来ます
5. **修正する** - フィードバックに基づいて改善
6. **繰り返し** - 品質が満足できるまで

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
├── examples/          # サンプルプロジェクト
├── CLAUDE.md          # このファイル
├── MANUS_RULES.md     # Manusのワークフロールール
└── README.md          # プロジェクト概要
```

## 利用可能なスキル

以下のスキルが `skills/` ディレクトリにあります。タスクに応じて参照してください：

| スキル名 | 説明 | 用途 |
|---------|------|------|
| frontend-design | 高品質なフロントエンドUI設計 | UI/コンポーネント作成 |
| react-best-practices | React/Next.jsパフォーマンス最適化（45+ルール） | React開発全般 |
| systematic-debugging | 体系的デバッグ手法 | バグ修正 |
| code-review | コードレビューガイドライン | PR/コードレビュー |
| git-workflow | Gitワークフローベストプラクティス | バージョン管理 |
| webapp-testing | Playwrightによるテスト | E2Eテスト |
| mcp-builder | MCPサーバー開発ガイド | MCP開発 |

## コーディング規約

### 一般

- TypeScript/JavaScript: ESLint + Prettier準拠
- Python: PEP 8準拠、型ヒント必須
- コメントは日本語でも英語でも可

### フロントエンド

- React: 関数コンポーネント + Hooks
- スタイリング: Tailwind CSS推奨
- 状態管理: React Context または Zustand

### バックエンド

- Python: FastAPI推奨
- Node.js: Express または Hono

## 重要な注意事項

1. **Manusからのフィードバックを尊重する** - Manusは品質管理役です
2. **スキルを活用する** - 高品質な出力のためにスキルを参照
3. **テスト可能な状態で提出する** - Manusがブラウザで確認できるように
4. **段階的に実装する** - 大きな変更は分割して

## Manusとの連携

このプロジェクトでは、以下の役割分担で開発を進めます：

| 役割 | 担当 | 責任 |
|------|------|------|
| 司令塔・品質管理 | Manus | タスク管理、ブラウザで品質確認、フィードバック |
| 実装担当 | Claude Code | コーディング、修正 |

**Manusが「品質に問題がある」と指摘した場合は、その指示に従って修正してください。**
