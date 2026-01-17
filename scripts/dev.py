#!/usr/bin/env python3
"""
Dev - 統合開発ワークフロースクリプト

Manusを司令塔として、Claude Code等のAI CLIに開発タスクを委譲し、
完了時にLINE通知を送信する統合ワークフローを提供します。

使い方:
    # 基本的な開発タスク
    python3 dev.py "ログイン機能を実装してください"
    
    # CLI指定
    python3 dev.py "コードをレビュー" --cli claude
    
    # スキル指定
    python3 dev.py "Reactコンポーネントを作成" --skill frontend-design
    
    # 通知付き
    python3 dev.py "API実装" --notify
    
    # フルオプション
    python3 dev.py "ダッシュボードを作成" \\
        --cli claude \\
        --skill frontend-design \\
        --skill react-best-practices \\
        --notify \\
        --max-budget 1.0
"""

import subprocess
import json
import sys
import os
import argparse
import time
from typing import Optional, List
from pathlib import Path
from datetime import datetime

# 同じディレクトリのモジュールをインポート
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from delegate import TaskDelegator, CLI, DelegationResult
from notify import send_development_report


class DevWorkflow:
    """統合開発ワークフロー"""
    
    def __init__(self, working_dir: Optional[str] = None):
        self.working_dir = working_dir or os.getcwd()
        self.delegator = TaskDelegator(working_dir=self.working_dir)
        self.start_time = None
    
    def run(self, 
            prompt: str,
            cli: Optional[str] = None,
            skills: List[str] = None,
            notify: bool = False,
            max_budget: Optional[float] = None,
            timeout: int = 300,
            verbose: bool = True) -> DelegationResult:
        """
        開発ワークフローを実行
        
        Args:
            prompt: タスクの説明
            cli: 使用するCLI (claude, gemini, codex, auto)
            skills: 使用するスキル
            notify: LINE通知を送信するか
            max_budget: 最大予算 (USD)
            timeout: タイムアウト秒数
            verbose: 詳細出力
        
        Returns:
            DelegationResult
        """
        
        self.start_time = time.time()
        
        if verbose:
            print("=" * 60)
            print("🚀 開発ワークフロー開始")
            print("=" * 60)
            print(f"📋 タスク: {prompt[:100]}...")
            print(f"📁 作業ディレクトリ: {self.working_dir}")
            print()
        
        # CLI選択
        cli_enum = None
        if cli:
            cli_map = {
                "claude": CLI.CLAUDE,
                "gemini": CLI.GEMINI,
                "codex": CLI.CODEX,
                "auto": None
            }
            cli_enum = cli_map.get(cli)
        
        # 委譲実行
        kwargs = {
            "timeout": timeout,
            "auto_skills": skills is None
        }
        if max_budget:
            kwargs["max_budget"] = max_budget
        if skills:
            kwargs["skills"] = skills
        
        if verbose:
            print("🔄 AIに委譲中...")
            print()
        
        result = self.delegator.delegate(prompt, cli=cli_enum, **kwargs)
        
        duration = time.time() - self.start_time
        
        # 結果表示
        if verbose:
            print()
            print("=" * 60)
            if result.success:
                print("✅ 完了")
            else:
                print("❌ 失敗")
            print("=" * 60)
            print(f"⏱️  所要時間: {duration:.1f}秒")
            print(f"🤖 使用AI: {result.cli}")
            if result.skills_used:
                print(f"📚 使用スキル: {', '.join(result.skills_used)}")
            if result.cost_usd:
                print(f"💰 コスト: ${result.cost_usd:.4f}")
            print()
        
        # LINE通知
        if notify:
            if verbose:
                print("📱 LINE通知を送信中...")
            
            send_development_report(
                task=prompt[:50],
                cli=result.cli,
                success=result.success,
                duration=duration,
                cost=result.cost_usd
            )
        
        return result
    
    def run_with_git(self,
                     prompt: str,
                     branch: Optional[str] = None,
                     commit: bool = True,
                     push: bool = False,
                     **kwargs) -> DelegationResult:
        """
        Git連携付きで開発ワークフローを実行
        
        Args:
            prompt: タスクの説明
            branch: 作業ブランチ名（指定しない場合は現在のブランチ）
            commit: 完了後にコミットするか
            push: コミット後にプッシュするか
            **kwargs: run()に渡す追加引数
        
        Returns:
            DelegationResult
        """
        
        # ブランチ作成/切り替え
        if branch:
            print(f"🌿 ブランチ '{branch}' に切り替え...")
            subprocess.run(
                ["git", "checkout", "-B", branch],
                cwd=self.working_dir,
                capture_output=True
            )
        
        # 開発実行
        result = self.run(prompt, **kwargs)
        
        if result.success and commit:
            # 変更をステージング
            subprocess.run(
                ["git", "add", "-A"],
                cwd=self.working_dir,
                capture_output=True
            )
            
            # 変更があるか確認
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.working_dir,
                capture_output=True,
                text=True
            )
            
            if status.stdout.strip():
                # コミット
                commit_msg = f"feat: {prompt[:50]}\n\nGenerated by AI ({result.cli})"
                subprocess.run(
                    ["git", "commit", "-m", commit_msg],
                    cwd=self.working_dir,
                    capture_output=True
                )
                print("📝 変更をコミットしました")
                
                if push:
                    # プッシュ
                    subprocess.run(
                        ["git", "push", "-u", "origin", "HEAD"],
                        cwd=self.working_dir,
                        capture_output=True
                    )
                    print("🚀 プッシュしました")
            else:
                print("📝 コミットする変更がありません")
        
        return result


def main():
    parser = argparse.ArgumentParser(
        description="統合開発ワークフロー",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  # 基本的な開発タスク
  python3 dev.py "ログイン機能を実装してください"
  
  # CLI指定
  python3 dev.py "コードをレビュー" --cli claude
  
  # スキル指定
  python3 dev.py "Reactコンポーネントを作成" --skill frontend-design
  
  # 通知付き
  python3 dev.py "API実装" --notify
  
  # Git連携
  python3 dev.py "新機能を追加" --branch feature/new-feature --commit --push
  
  # フルオプション
  python3 dev.py "ダッシュボードを作成" \\
      --cli claude \\
      --skill frontend-design \\
      --skill react-best-practices \\
      --notify \\
      --max-budget 1.0
"""
    )
    
    parser.add_argument("prompt", help="タスクの説明")
    parser.add_argument("--cli", "-c", 
                        choices=["claude", "gemini", "codex", "auto"],
                        default="auto",
                        help="使用するCLI (デフォルト: auto)")
    parser.add_argument("--skill", action="append", dest="skills",
                        help="使用するスキル（複数指定可）")
    parser.add_argument("--notify", "-n", action="store_true",
                        help="完了時にLINE通知を送信")
    parser.add_argument("--max-budget", type=float,
                        help="最大予算 (USD)")
    parser.add_argument("--timeout", type=int, default=300,
                        help="タイムアウト秒数")
    parser.add_argument("-C", "--working-dir",
                        help="作業ディレクトリ")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="詳細出力を抑制")
    parser.add_argument("--json", action="store_true",
                        help="JSON形式で出力")
    
    # Git連携オプション
    parser.add_argument("--branch", "-b",
                        help="作業ブランチ名")
    parser.add_argument("--commit", action="store_true",
                        help="完了後にコミット")
    parser.add_argument("--push", action="store_true",
                        help="コミット後にプッシュ")
    
    args = parser.parse_args()
    
    workflow = DevWorkflow(working_dir=args.working_dir)
    
    # Git連携の有無で実行方法を分岐
    if args.branch or args.commit or args.push:
        result = workflow.run_with_git(
            prompt=args.prompt,
            cli=args.cli,
            skills=args.skills,
            notify=args.notify,
            max_budget=args.max_budget,
            timeout=args.timeout,
            verbose=not args.quiet,
            branch=args.branch,
            commit=args.commit,
            push=args.push
        )
    else:
        result = workflow.run(
            prompt=args.prompt,
            cli=args.cli,
            skills=args.skills,
            notify=args.notify,
            max_budget=args.max_budget,
            timeout=args.timeout,
            verbose=not args.quiet
        )
    
    # 結果出力
    if args.json:
        print(json.dumps({
            "success": result.success,
            "cli": result.cli,
            "output": result.output,
            "cost_usd": result.cost_usd,
            "session_id": result.session_id,
            "error": result.error,
            "skills_used": result.skills_used
        }, indent=2, ensure_ascii=False))
    elif not args.quiet:
        if result.output:
            print("\n📄 出力:")
            print("-" * 40)
            print(result.output)
    
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
