# Landing Page - サンプルプロジェクト

このサンプルは、Claude Codeを使ってモダンなランディングページを作成する例です。

## 実行方法

### Manusへの指示

```
ai-dev-environmentをクローンして、examples/landing-pageディレクトリで
delegate.pyを使ってClaude Codeに以下のタスクを実行させてください：

「SaaSプロダクトのランディングページを作成してください。
frontend-designスキルを使用してください。」
```

### 直接実行

```bash
cd examples/landing-page
python3 ../../scripts/delegate.py claude \
  "SaaSプロダクトのランディングページを作成してください。
   要件：
   - ヒーローセクション（キャッチコピー + CTA）
   - 機能紹介セクション（3つの特徴）
   - 料金プランセクション
   - FAQ セクション
   - フッター
   - レスポンシブデザイン
   - ダークモード対応
   - アニメーション効果
   技術：
   - Next.js 14 (App Router)
   - Tailwind CSS
   - Framer Motion" \
  --skill frontend-design
```

## 期待される成果物

```
landing-page/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   ├── Hero.tsx
│   ├── Features.tsx
│   ├── Pricing.tsx
│   ├── FAQ.tsx
│   ├── Footer.tsx
│   └── ui/
│       ├── Button.tsx
│       └── Card.tsx
├── package.json
├── tailwind.config.ts
└── next.config.js
```

## 使用スキル

- **frontend-design**: モダンで美しいUIデザイン、アニメーション

## コスト目安

- Claude Code: 約$0.08〜0.15
