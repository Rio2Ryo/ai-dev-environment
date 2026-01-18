#!/usr/bin/env python3
"""
Review - 品質管理・レビュー支援スクリプト

Manusが成果物を確認し、Claude Codeにフィードバックを送るためのスクリプトです。

使い方:
    # 開発サーバーを起動してブラウザで確認
    python3 review.py serve ./project-dir
    
    # フィードバックを送信
    python3 review.py feedback "ボタンのホバー効果が動作しない" -C ./project-dir
    
    # チェックリストに基づく確認
    python3 review.py checklist ./project-dir
"""

import subprocess
import sys
import argparse
import os
import json
from typing import Optional, List
from pathlib import Path


# 品質チェックリスト
QUALITY_CHECKLIST = {
    "ui": [
        "UIが正しく表示されるか",
        "レスポンシブ対応（モバイル/タブレット/デスクトップ）",
        "ダークモード対応（必要な場合）",
        "アニメーション・トランジションが滑らか",
        "フォントサイズ・色のコントラストが適切",
    ],
    "functionality": [
        "主要機能が動作するか",
        "フォームのバリデーションが機能するか",
        "エラーメッセージが適切に表示されるか",
        "ローディング状態が表示されるか",
        "ボタン・リンクが正しく動作するか",
    ],
    "performance": [
        "ページの読み込みが速いか",
        "スクロールが滑らかか",
        "メモリリークがないか",
    ],
    "accessibility": [
        "キーボード操作が可能か",
        "スクリーンリーダー対応（alt属性等）",
        "フォーカス状態が視認できるか",
    ],
}


def find_package_json(directory: str) -> Optional[str]:
    """package.jsonを探す"""
    path = Path(directory)
    for parent in [path] + list(path.parents):
        pkg = parent / "package.json"
        if pkg.exists():
            return str(parent)
    return None


def find_python_app(directory: str) -> Optional[str]:
    """Pythonアプリのエントリーポイントを探す"""
    path = Path(directory)
    candidates = ["main.py", "app.py", "server.py", "run.py"]
    for candidate in candidates:
        if (path / candidate).exists():
            return str(path / candidate)
    # app/main.py パターン
    if (path / "app" / "main.py").exists():
        return str(path / "app" / "main.py")
    return None


def serve_project(directory: str, port: int = 3000) -> None:
    """開発サーバーを起動"""
    directory = os.path.abspath(directory)
    
    # Node.jsプロジェクトか確認
    node_dir = find_package_json(directory)
    if node_dir:
        print(f"📦 Node.jsプロジェクトを検出: {node_dir}")
        
        # package.jsonを読んでスクリプトを確認
        with open(os.path.join(node_dir, "package.json")) as f:
            pkg = json.load(f)
        
        scripts = pkg.get("scripts", {})
        
        if "dev" in scripts:
            cmd = ["npm", "run", "dev"]
        elif "start" in scripts:
            cmd = ["npm", "run", "start"]
        else:
            print("⚠️ dev/startスクリプトが見つかりません")
            print("手動で起動してください")
            return
        
        print(f"🚀 開発サーバーを起動: {' '.join(cmd)}")
        print(f"📍 URL: http://localhost:{port}")
        print("Ctrl+C で停止")
        
        try:
            subprocess.run(cmd, cwd=node_dir)
        except KeyboardInterrupt:
            print("\n⏹️ サーバーを停止しました")
        return
    
    # Pythonプロジェクトか確認
    python_app = find_python_app(directory)
    if python_app:
        print(f"🐍 Pythonアプリを検出: {python_app}")
        
        # FastAPIかFlaskか判定
        with open(python_app) as f:
            content = f.read()
        
        if "fastapi" in content.lower() or "FastAPI" in content:
            cmd = ["uvicorn", "app.main:app", "--reload", "--port", str(port)]
        elif "flask" in content.lower() or "Flask" in content:
            cmd = ["python3", python_app]
        else:
            cmd = ["python3", python_app]
        
        print(f"🚀 開発サーバーを起動: {' '.join(cmd)}")
        print(f"📍 URL: http://localhost:{port}")
        print("Ctrl+C で停止")
        
        try:
            subprocess.run(cmd, cwd=directory)
        except KeyboardInterrupt:
            print("\n⏹️ サーバーを停止しました")
        return
    
    # 静的ファイルの場合
    print(f"📄 静的ファイルサーバーを起動")
    print(f"📍 URL: http://localhost:{port}")
    print("Ctrl+C で停止")
    
    try:
        subprocess.run(
            ["python3", "-m", "http.server", str(port)],
            cwd=directory
        )
    except KeyboardInterrupt:
        print("\n⏹️ サーバーを停止しました")


def send_feedback(feedback: str, working_dir: str, skill: Optional[str] = None) -> None:
    """Claude Codeにフィードバックを送信"""
    
    # フィードバックをプロンプトに変換
    prompt = f"""以下の問題を修正してください：

{feedback}

修正後、変更内容を簡潔に説明してください。"""
    
    # delegate.pyを使ってClaude Codeに送信
    cmd = [
        "python3",
        os.path.join(os.path.dirname(__file__), "delegate.py"),
        "claude",
        prompt,
        "-C", working_dir
    ]
    
    if skill:
        cmd.extend(["--skill", skill])
    
    print(f"📤 Claude Codeにフィードバックを送信中...")
    print(f"📝 内容: {feedback[:100]}...")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ フィードバックを送信しました")
        print(result.stdout)
    else:
        print("❌ フィードバックの送信に失敗しました")
        print(result.stderr)


def show_checklist(directory: str) -> None:
    """品質チェックリストを表示"""
    
    print("=" * 60)
    print("📋 品質チェックリスト")
    print("=" * 60)
    print()
    print(f"プロジェクト: {os.path.abspath(directory)}")
    print()
    
    for category, items in QUALITY_CHECKLIST.items():
        print(f"【{category.upper()}】")
        for i, item in enumerate(items, 1):
            print(f"  [ ] {i}. {item}")
        print()
    
    print("=" * 60)
    print("使い方:")
    print("  1. 開発サーバーを起動: python3 review.py serve ./project-dir")
    print("  2. ブラウザで各項目を確認")
    print("  3. 問題があればフィードバック: python3 review.py feedback '問題内容'")
    print("=" * 60)


def generate_feedback_template(issues: List[str]) -> str:
    """フィードバックテンプレートを生成"""
    
    template = "以下の問題を修正してください：\n\n"
    
    for i, issue in enumerate(issues, 1):
        template += f"{i}. {issue}\n"
    
    return template


def main():
    parser = argparse.ArgumentParser(
        description="品質管理・レビュー支援スクリプト",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  # 開発サーバーを起動
  python3 review.py serve ./project-dir
  
  # フィードバックを送信
  python3 review.py feedback "ボタンのホバー効果が動作しない" -C ./project-dir
  
  # 複数の問題をフィードバック
  python3 review.py feedback "1. ボタンが動作しない\\n2. レイアウトが崩れる" -C ./project-dir
  
  # チェックリストを表示
  python3 review.py checklist ./project-dir
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="コマンド")
    
    # serve コマンド
    serve_parser = subparsers.add_parser("serve", help="開発サーバーを起動")
    serve_parser.add_argument("directory", help="プロジェクトディレクトリ")
    serve_parser.add_argument("--port", "-p", type=int, default=3000, help="ポート番号")
    
    # feedback コマンド
    feedback_parser = subparsers.add_parser("feedback", help="フィードバックを送信")
    feedback_parser.add_argument("message", help="フィードバック内容")
    feedback_parser.add_argument("-C", "--working-dir", default=".", help="作業ディレクトリ")
    feedback_parser.add_argument("--skill", help="使用するスキル")
    
    # checklist コマンド
    checklist_parser = subparsers.add_parser("checklist", help="チェックリストを表示")
    checklist_parser.add_argument("directory", nargs="?", default=".", help="プロジェクトディレクトリ")
    
    args = parser.parse_args()
    
    if args.command == "serve":
        serve_project(args.directory, args.port)
    elif args.command == "feedback":
        send_feedback(args.message, args.working_dir, args.skill)
    elif args.command == "checklist":
        show_checklist(args.directory)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
