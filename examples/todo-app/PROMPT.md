# Todo App - サンプルプロジェクト

このサンプルは、Claude Codeを使ってシンプルなTodoアプリを作成する例です。

## 実行方法

### Manusへの指示

```
ai-dev-environmentをクローンして、examples/todo-appディレクトリで
delegate.pyを使ってClaude Codeに以下のタスクを実行させてください：

「React + TypeScriptでシンプルなTodoアプリを作成してください。
frontend-designとreact-best-practicesスキルを使用してください。」
```

### 直接実行

```bash
cd examples/todo-app
python3 ../../scripts/delegate.py claude \
  "React + TypeScriptでシンプルなTodoアプリを作成してください。
   機能：
   - タスクの追加・削除・完了切り替え
   - ローカルストレージへの保存
   - フィルター（全て/未完了/完了）
   - モダンなUI（Tailwind CSS）" \
  --skill frontend-design \
  --skill react-best-practices
```

## 期待される成果物

```
todo-app/
├── src/
│   ├── App.tsx
│   ├── components/
│   │   ├── TodoItem.tsx
│   │   ├── TodoList.tsx
│   │   ├── TodoInput.tsx
│   │   └── TodoFilter.tsx
│   ├── hooks/
│   │   └── useTodos.ts
│   ├── types/
│   │   └── todo.ts
│   └── main.tsx
├── package.json
├── tailwind.config.js
└── vite.config.ts
```

## 使用スキル

- **frontend-design**: モダンで美しいUIデザイン
- **react-best-practices**: パフォーマンス最適化、適切なコンポーネント設計

## コスト目安

- Claude Code: 約$0.05〜0.10
