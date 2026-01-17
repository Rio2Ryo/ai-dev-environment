# API Server - サンプルプロジェクト

このサンプルは、Claude Codeを使ってRESTful APIサーバーを作成する例です。

## 実行方法

### Manusへの指示

```
ai-dev-environmentをクローンして、examples/api-serverディレクトリで
delegate.pyを使ってClaude Codeに以下のタスクを実行させてください：

「Python FastAPIでユーザー管理APIを作成してください。」
```

### 直接実行

```bash
cd examples/api-server
python3 ../../scripts/delegate.py claude \
  "Python FastAPIでユーザー管理APIを作成してください。
   機能：
   - ユーザーCRUD（作成・取得・更新・削除）
   - JWT認証
   - Pydanticによるバリデーション
   - SQLiteデータベース
   - OpenAPI自動生成
   - 適切なエラーハンドリング"
```

## 期待される成果物

```
api-server/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   └── user.py
│   ├── schemas/
│   │   └── user.py
│   ├── routers/
│   │   ├── auth.py
│   │   └── users.py
│   ├── services/
│   │   └── user_service.py
│   └── utils/
│       ├── auth.py
│       └── database.py
├── requirements.txt
└── README.md
```

## 使用スキル

- **systematic-debugging**: エラーハンドリングとデバッグ

## コスト目安

- Claude Code: 約$0.05〜0.10
