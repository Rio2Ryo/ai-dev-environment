# Manus → Claude Code 委譲ワークフロー設計

## 概要

このドキュメントは、Manusを「司令塔」、Claude Codeを「実行部隊」とする開発ワークフローを定義します。

## アーキテクチャ

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
│  ・進捗管理                                                  │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Claude Code    │ │   Gemini CLI    │ │   Codex CLI     │
│  （メイン開発）  │ │ （簡単なタスク） │ │ （コードレビュー）│
│                 │ │  （無料枠活用）  │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## タスク振り分けルール

| タスク種別 | 優先CLI | 理由 |
|-----------|---------|------|
| 新機能開発 | Claude Code | 高品質なコード生成、ファイル操作 |
| バグ修正 | Claude Code | コンテキスト理解、デバッグ能力 |
| 簡単な質問 | Gemini CLI | 無料枠、高速応答 |
| コードレビュー | Codex CLI | 専用reviewコマンド |
| リファクタリング | Claude Code | 大規模変更に強い |
| ドキュメント生成 | Gemini CLI | コスト効率 |

## 実行フロー

### 1. タスク受付（Manus）
```
ユーザー: 「ログイン機能を実装して」
Manus: タスクを分析 → 「新機能開発」と判定
```

### 2. CLI選択と実行（Manus → Claude Code）
```bash
# Manusが以下のコマンドを実行
claude -p "ログイン機能を実装してください。
要件:
- メールアドレスとパスワードによる認証
- バリデーション付きフォーム
- エラーハンドリング
作業ディレクトリ: /path/to/project" \
  --output-format json \
  --permission-mode acceptEdits
```

### 3. 結果確認（Manus）
```
Manus: Claude Codeの出力を解析
- 成功/失敗の判定
- 生成されたファイルの確認
- ユーザーへの報告
```

## コマンドテンプレート

### Claude Code（メイン開発）
```bash
claude -p "${TASK_PROMPT}" \
  --output-format json \
  --permission-mode acceptEdits \
  --model sonnet
```

### Gemini CLI（簡単なタスク）
```bash
gemini "${TASK_PROMPT}" \
  --output-format json \
  --approval-mode auto_edit
```

### Codex CLI（コードレビュー）
```bash
codex exec review \
  --json \
  -s read-only
```

## コスト最適化戦略

### 優先順位
1. **Gemini CLI**: 無料枠（1,000リクエスト/日）を最大活用
2. **Codex CLI**: OpenAI料金、中程度のタスク
3. **Claude Code**: 高品質が必要な場合のみ

### 予算管理
```bash
# Claude Codeに予算上限を設定
claude -p "${PROMPT}" --max-budget-usd 0.10
```

## セッション管理

### 継続作業
```bash
# 前回のセッションを再開
claude -r ${SESSION_ID}
gemini -r latest
```

### プロジェクトコンテキスト
- `CLAUDE.md`: Claude Code用プロジェクト設定
- `GEMINI.md`: Gemini CLI用プロジェクト設定
- スキルファイル: `~/.claude/skills/`

## エラーハンドリング

### フォールバック戦略
1. Claude Code失敗 → Codex CLIで再試行
2. Gemini CLI失敗 → Claude Codeで再試行
3. 全CLI失敗 → Manusが直接対応（最終手段）

### タイムアウト設定
- 通常タスク: 60秒
- 大規模タスク: 300秒
- 無限ループ防止: 最大3回リトライ
