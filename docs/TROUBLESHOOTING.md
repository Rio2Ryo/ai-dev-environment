# トラブルシューティング

よくある問題と解決方法です。

## CLI関連

### Claude Code が見つからない

**エラー**: `Claude CLI not found`

**解決方法**:
```bash
# インストール
curl -fsSL https://claude.ai/install.sh | bash

# PATHを通す
export PATH="$HOME/.local/bin:$PATH"

# 確認
claude --version
```

### Gemini CLI が見つからない

**エラー**: `Gemini CLI not found`

**解決方法**:
```bash
# インストール
npm install -g @google/gemini-cli

# 確認
gemini --version
```

### Codex CLI が見つからない

**エラー**: `Codex CLI not found`

**解決方法**:
```bash
# インストール
npm install -g @openai/codex

# 確認
codex --version
```

## 認証関連

### Claude Code の認証エラー

**エラー**: `Authentication required`

**解決方法**:
```bash
# 対話モードでログイン
claude

# または API キーを設定
export ANTHROPIC_API_KEY="your-api-key"
```

### Gemini の認証エラー

**解決方法**:
```bash
# 対話モードでログイン
gemini

# または API キーを設定
export GEMINI_API_KEY="your-api-key"
```

## タイムアウト

### タスクがタイムアウトする

**エラー**: `Timeout expired`

**解決方法**:
```bash
# タイムアウトを延長
python3 scripts/delegate.py claude "タスク" --timeout 600
```

### 複雑なタスクの場合

大きなタスクは分割して実行：

```bash
# 悪い例
python3 scripts/delegate.py claude "フルスタックアプリを作成"

# 良い例
python3 scripts/delegate.py claude "バックエンドAPIを作成"
python3 scripts/delegate.py claude "フロントエンドUIを作成"
```

## スキル関連

### スキルが見つからない

**エラー**: `Skill 'xxx' not found`

**解決方法**:
```bash
# 利用可能なスキル確認
python3 scripts/delegate.py --list-skills

# スキルをコピー
cp -r skills/* ~/.claude/skills/
```

### スキルが適用されない

Claude Codeの場合、スキルは `~/.claude/skills/` に配置する必要があります：

```bash
cp -r skills/* ~/.claude/skills/
```

## LINE通知関連

### 通知が送信されない

**原因**: LINE MCPが設定されていない

**解決方法**:
- Manus環境でのみLINE通知が利用可能です
- ローカル環境では通知機能をスキップしてください

```bash
# 通知なしで実行
python3 scripts/dev.py "タスク"  # --notify を付けない
```

## その他

### 予算超過

**エラー**: `Budget exceeded`

**解決方法**:
```bash
# 予算を設定
python3 scripts/delegate.py claude "タスク" --max-budget 0.50
```

### フォールバックを使う

一つのCLIが失敗した場合、自動で別のCLIを試す：

```bash
python3 scripts/delegate.py auto "タスク" --fallback
```

## サポート

問題が解決しない場合：

1. [GitHub Issues](https://github.com/Rio2Ryo/ai-dev-environment/issues) で報告
2. エラーメッセージと実行コマンドを含めてください
