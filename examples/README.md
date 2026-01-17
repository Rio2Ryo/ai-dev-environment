# サンプルプロジェクト

この環境を使って作成できるプロジェクトの例です。

## 一覧

| プロジェクト | 説明 | 推奨スキル | コスト目安 |
|-------------|------|-----------|-----------|
| [todo-app](./todo-app/) | React + TypeScript Todoアプリ | frontend-design, react-best-practices | $0.05〜0.10 |
| [api-server](./api-server/) | FastAPI RESTful API | systematic-debugging | $0.05〜0.10 |
| [landing-page](./landing-page/) | Next.js ランディングページ | frontend-design | $0.08〜0.15 |

## 使い方

各ディレクトリの `PROMPT.md` に、Manusへの指示方法と直接実行コマンドが記載されています。

### 基本的な流れ

1. プロジェクトディレクトリに移動
2. `PROMPT.md` の指示を参考にManusに依頼
3. Claude Codeが実際の開発を実行
4. 成果物を確認

### 例: Todo Appを作成

```bash
# Manusへの指示
「ai-dev-environmentをクローンして、examples/todo-appディレクトリで
delegate.pyを使ってClaude CodeにシンプルなTodoアプリを作成させてください」
```

## 新しいサンプルの追加

1. `examples/` に新しいディレクトリを作成
2. `PROMPT.md` を作成（テンプレートは既存のものを参考）
3. 必要に応じて初期ファイルを配置

## 注意事項

- 各プロジェクトは独立しており、他のプロジェクトに影響しません
- コスト目安は参考値です。タスクの複雑さにより変動します
- 生成されたコードは必ずレビューしてから使用してください
