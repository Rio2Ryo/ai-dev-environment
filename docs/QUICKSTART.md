# クイックスタートガイド

この環境を使い始めるための最短ルートです。

## 5分で始める

### Step 1: リポジトリをクローン

```bash
gh repo clone Rio2Ryo/ai-dev-environment
cd ai-dev-environment
```

### Step 2: 最初のタスクを実行

```bash
# Geminiに簡単な質問（無料）
python3 scripts/delegate.py gemini "Pythonでリストをソートする方法"
```

これだけで動作確認完了です！

## Manusから使う場合

Manusに以下のように指示してください：

> 「`ai-dev-environment`をクローンして、`delegate.py`を使って**Claude Codeに**ログイン機能を実装させてください」

## よく使うコマンド

### 開発タスク（Claude Code）

```bash
python3 scripts/delegate.py claude "Reactでダッシュボードを作成"
```

### 簡単な質問（Gemini - 無料）

```bash
python3 scripts/delegate.py gemini "TypeScriptの型定義の書き方"
```

### コードレビュー（Codex）

```bash
python3 scripts/delegate.py codex --review
```

### 自動選択

```bash
python3 scripts/delegate.py auto "タスク内容"
```

## スキルを使う

高品質な出力のためにスキルを指定：

```bash
python3 scripts/delegate.py claude "Reactコンポーネントを作成" \
  --skill frontend-design \
  --skill react-best-practices
```

利用可能なスキル一覧：

```bash
python3 scripts/delegate.py --list-skills
```

## 次のステップ

- [README.md](../README.md) - 詳細なドキュメント
- [examples/](../examples/) - サンプルプロジェクト
- [skills/](../skills/) - 利用可能なスキル
