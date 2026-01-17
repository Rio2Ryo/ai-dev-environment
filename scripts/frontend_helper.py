#!/usr/bin/env python3
"""
Frontend Development Helper - フロントエンド開発支援スクリプト

Claude Code Skillsと連携し、高品質なフロントエンド開発を支援します。
"""

import os
import json
from typing import Optional
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ai_orchestrator import AIOrchestrator, TaskType, AIResponse


class FrontendHelper:
    """フロントエンド開発を支援するヘルパークラス"""
    
    def __init__(self):
        self.orchestrator = AIOrchestrator()
        self.skills_path = os.path.expanduser("~/.claude/skills")
        
        # フロントエンドスキルを読み込み
        self.frontend_skill = self._load_skill("frontend-design.md")
        self.react_skill = self._load_skill("react-best-practices.md")
    
    def _load_skill(self, filename: str) -> Optional[str]:
        """スキルファイルを読み込み"""
        filepath = os.path.join(self.skills_path, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return f.read()
        return None
    
    def _build_prompt(self, request: str, include_skills: bool = True) -> str:
        """スキルを含めたプロンプトを構築"""
        prompt_parts = []
        
        if include_skills:
            if self.frontend_skill:
                prompt_parts.append(f"<skill>\n{self.frontend_skill}\n</skill>")
            if self.react_skill:
                prompt_parts.append(f"<skill>\n{self.react_skill}\n</skill>")
        
        prompt_parts.append(f"<request>\n{request}\n</request>")
        
        return "\n\n".join(prompt_parts)
    
    def generate_component(self, description: str) -> AIResponse:
        """Reactコンポーネントを生成"""
        prompt = self._build_prompt(f"""
以下の要件に基づいて、高品質なReactコンポーネントを生成してください。

要件:
{description}

出力形式:
- TypeScriptで記述
- Tailwind CSSでスタイリング
- アクセシビリティ対応
- レスポンシブデザイン
- 必要なPropsの型定義を含める
""")
        return self.orchestrator.execute(prompt, TaskType.FRONTEND)
    
    def review_ui(self, code: str) -> AIResponse:
        """UIコードをレビュー"""
        prompt = self._build_prompt(f"""
以下のUIコードをレビューし、改善点を指摘してください。

```
{code}
```

レビュー観点:
1. デザイン品質（AI臭さがないか）
2. アクセシビリティ
3. レスポンシブ対応
4. パフォーマンス
5. コード品質
""")
        return self.orchestrator.execute(prompt, TaskType.CODE_REVIEW)
    
    def suggest_design(self, context: str) -> AIResponse:
        """デザイン提案を生成"""
        prompt = self._build_prompt(f"""
以下のコンテキストに基づいて、UIデザインの提案をしてください。

コンテキスト:
{context}

提案に含めるもの:
- カラーパレット
- タイポグラフィ
- レイアウト構造
- コンポーネント構成
- インタラクション設計
""")
        return self.orchestrator.execute(prompt, TaskType.FRONTEND)
    
    def convert_to_tailwind(self, css_code: str) -> AIResponse:
        """CSSをTailwind CSSに変換"""
        prompt = f"""
以下のCSSをTailwind CSSのユーティリティクラスに変換してください。

```css
{css_code}
```

変換ルール:
- 可能な限り標準のユーティリティクラスを使用
- 必要に応じてarbitrary valuesを使用
- @applyは最小限に
"""
        return self.orchestrator.execute(prompt, TaskType.SIMPLE_CODE)


def main():
    """CLIインターフェース"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Frontend Development Helper")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # generate コマンド
    gen_parser = subparsers.add_parser("generate", help="Generate a component")
    gen_parser.add_argument("description", help="Component description")
    
    # review コマンド
    review_parser = subparsers.add_parser("review", help="Review UI code")
    review_parser.add_argument("file", help="File to review")
    
    # design コマンド
    design_parser = subparsers.add_parser("design", help="Get design suggestions")
    design_parser.add_argument("context", help="Design context")
    
    args = parser.parse_args()
    helper = FrontendHelper()
    
    if args.command == "generate":
        response = helper.generate_component(args.description)
        print(response.content)
    
    elif args.command == "review":
        with open(args.file, "r") as f:
            code = f.read()
        response = helper.review_ui(code)
        print(response.content)
    
    elif args.command == "design":
        response = helper.suggest_design(args.context)
        print(response.content)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
