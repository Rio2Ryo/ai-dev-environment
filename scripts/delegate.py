#!/usr/bin/env python3
"""
Task Delegator - タスク委譲スクリプト

Manusからの指示を受けて、適切なAI CLI（Claude Code, Gemini, Codex）に
タスクを委譲し、結果を返します。

使い方:
    # Claude Codeに開発タスクを委譲
    python3 delegate.py claude "ログイン機能を実装してください"
    
    # Geminiに簡単な質問を委譲
    python3 delegate.py gemini "Pythonでリストをソートする方法"
    
    # Codexにコードレビューを委譲
    python3 delegate.py codex --review
    
    # 自動選択モード
    python3 delegate.py auto "タスク内容"
"""

import subprocess
import json
import sys
import os
import argparse
from typing import Optional, Dict, Any, Tuple
from enum import Enum
from dataclasses import dataclass


class CLI(Enum):
    CLAUDE = "claude"
    GEMINI = "gemini"
    CODEX = "codex"


class TaskType(Enum):
    DEVELOPMENT = "development"      # 新機能開発
    BUGFIX = "bugfix"               # バグ修正
    REVIEW = "review"               # コードレビュー
    REFACTOR = "refactor"           # リファクタリング
    QUESTION = "question"           # 簡単な質問
    DOCUMENTATION = "documentation"  # ドキュメント生成


@dataclass
class DelegationResult:
    """委譲結果"""
    success: bool
    cli: str
    output: str
    cost_usd: Optional[float] = None
    session_id: Optional[str] = None
    error: Optional[str] = None


class TaskDelegator:
    """タスク委譲を管理するクラス"""
    
    def __init__(self, working_dir: Optional[str] = None):
        self.working_dir = working_dir or os.getcwd()
        
        # タスクタイプとCLIのマッピング
        self.task_cli_map = {
            TaskType.DEVELOPMENT: CLI.CLAUDE,
            TaskType.BUGFIX: CLI.CLAUDE,
            TaskType.REVIEW: CLI.CODEX,
            TaskType.REFACTOR: CLI.CLAUDE,
            TaskType.QUESTION: CLI.GEMINI,
            TaskType.DOCUMENTATION: CLI.GEMINI,
        }
    
    def analyze_task(self, prompt: str) -> TaskType:
        """プロンプトからタスクタイプを判定"""
        prompt_lower = prompt.lower()
        
        if any(kw in prompt_lower for kw in ["review", "レビュー", "チェック"]):
            return TaskType.REVIEW
        elif any(kw in prompt_lower for kw in ["bug", "バグ", "エラー", "修正", "fix"]):
            return TaskType.BUGFIX
        elif any(kw in prompt_lower for kw in ["refactor", "リファクタ", "整理", "改善"]):
            return TaskType.REFACTOR
        elif any(kw in prompt_lower for kw in ["doc", "ドキュメント", "readme", "説明"]):
            return TaskType.DOCUMENTATION
        elif any(kw in prompt_lower for kw in ["?", "？", "how", "what", "why", "どう", "なぜ"]):
            return TaskType.QUESTION
        else:
            return TaskType.DEVELOPMENT
    
    def delegate_to_claude(self, prompt: str, 
                           permission_mode: str = "acceptEdits",
                           max_budget: Optional[float] = None,
                           timeout: int = 300) -> DelegationResult:
        """Claude Codeにタスクを委譲"""
        cmd = [
            "claude", "-p", prompt,
            "--output-format", "json",
            "--permission-mode", permission_mode,
        ]
        
        if max_budget:
            cmd.extend(["--max-budget-usd", str(max_budget)])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.working_dir,
                env={**os.environ, "PATH": f"{os.environ['HOME']}/.local/bin:{os.environ.get('PATH', '')}"}
            )
            
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    return DelegationResult(
                        success=data.get("type") == "result" and not data.get("is_error"),
                        cli="claude",
                        output=data.get("result", result.stdout),
                        cost_usd=data.get("total_cost_usd"),
                        session_id=data.get("session_id")
                    )
                except json.JSONDecodeError:
                    return DelegationResult(
                        success=True,
                        cli="claude",
                        output=result.stdout
                    )
            else:
                return DelegationResult(
                    success=False,
                    cli="claude",
                    output=result.stdout,
                    error=result.stderr
                )
        except subprocess.TimeoutExpired:
            return DelegationResult(
                success=False,
                cli="claude",
                output="",
                error="Timeout expired"
            )
        except Exception as e:
            return DelegationResult(
                success=False,
                cli="claude",
                output="",
                error=str(e)
            )
    
    def delegate_to_gemini(self, prompt: str,
                           approval_mode: str = "auto_edit",
                           timeout: int = 120) -> DelegationResult:
        """Gemini CLIにタスクを委譲"""
        cmd = [
            "gemini", prompt,
            "--output-format", "json",
            "--approval-mode", approval_mode,
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.working_dir
            )
            
            return DelegationResult(
                success=result.returncode == 0,
                cli="gemini",
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None
            )
        except subprocess.TimeoutExpired:
            return DelegationResult(
                success=False,
                cli="gemini",
                output="",
                error="Timeout expired"
            )
        except Exception as e:
            return DelegationResult(
                success=False,
                cli="gemini",
                output="",
                error=str(e)
            )
    
    def delegate_to_codex(self, prompt: str = "",
                          review: bool = False,
                          sandbox: str = "read-only",
                          timeout: int = 180) -> DelegationResult:
        """Codex CLIにタスクを委譲"""
        if review:
            cmd = ["codex", "exec", "review", "--json", "-s", sandbox]
        else:
            cmd = ["codex", "exec", prompt, "--json", "-s", sandbox]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.working_dir
            )
            
            return DelegationResult(
                success=result.returncode == 0,
                cli="codex",
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None
            )
        except subprocess.TimeoutExpired:
            return DelegationResult(
                success=False,
                cli="codex",
                output="",
                error="Timeout expired"
            )
        except Exception as e:
            return DelegationResult(
                success=False,
                cli="codex",
                output="",
                error=str(e)
            )
    
    def delegate(self, prompt: str, 
                 cli: Optional[CLI] = None,
                 **kwargs) -> DelegationResult:
        """タスクを適切なCLIに委譲"""
        
        # CLI未指定の場合は自動選択
        if cli is None:
            task_type = self.analyze_task(prompt)
            cli = self.task_cli_map[task_type]
            print(f"[Auto] Task type: {task_type.value} -> CLI: {cli.value}")
        
        # 委譲実行
        if cli == CLI.CLAUDE:
            return self.delegate_to_claude(prompt, **kwargs)
        elif cli == CLI.GEMINI:
            return self.delegate_to_gemini(prompt, **kwargs)
        elif cli == CLI.CODEX:
            return self.delegate_to_codex(prompt, **kwargs)
        else:
            return DelegationResult(
                success=False,
                cli="unknown",
                output="",
                error=f"Unknown CLI: {cli}"
            )
    
    def delegate_with_fallback(self, prompt: str,
                               fallback_chain: list = None) -> DelegationResult:
        """フォールバック付きで委譲"""
        if fallback_chain is None:
            fallback_chain = [CLI.CLAUDE, CLI.GEMINI, CLI.CODEX]
        
        for cli in fallback_chain:
            print(f"[Trying] {cli.value}...")
            result = self.delegate(prompt, cli=cli)
            
            if result.success:
                return result
            else:
                print(f"[Failed] {cli.value}: {result.error}")
        
        return DelegationResult(
            success=False,
            cli="all",
            output="",
            error="All CLIs failed"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Task Delegator - AI CLIへのタスク委譲",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  # Claude Codeに開発タスクを委譲
  python3 delegate.py claude "ログイン機能を実装してください"
  
  # Geminiに簡単な質問を委譲
  python3 delegate.py gemini "Pythonでリストをソートする方法"
  
  # Codexにコードレビューを委譲
  python3 delegate.py codex --review
  
  # 自動選択モード
  python3 delegate.py auto "タスク内容"
  
  # フォールバック付き
  python3 delegate.py auto "タスク内容" --fallback
"""
    )
    
    parser.add_argument("cli", choices=["claude", "gemini", "codex", "auto"],
                        help="使用するCLI (auto: 自動選択)")
    parser.add_argument("prompt", nargs="?", default="",
                        help="タスクのプロンプト")
    parser.add_argument("--review", action="store_true",
                        help="コードレビューモード (codexのみ)")
    parser.add_argument("--fallback", action="store_true",
                        help="失敗時に他のCLIにフォールバック")
    parser.add_argument("--max-budget", type=float,
                        help="最大予算 (USD, claudeのみ)")
    parser.add_argument("--timeout", type=int, default=300,
                        help="タイムアウト秒数")
    parser.add_argument("-C", "--working-dir",
                        help="作業ディレクトリ")
    parser.add_argument("--json", action="store_true",
                        help="JSON形式で出力")
    
    args = parser.parse_args()
    
    delegator = TaskDelegator(working_dir=args.working_dir)
    
    # CLI選択
    cli_map = {
        "claude": CLI.CLAUDE,
        "gemini": CLI.GEMINI,
        "codex": CLI.CODEX,
        "auto": None
    }
    cli = cli_map[args.cli]
    
    # 委譲実行
    kwargs = {"timeout": args.timeout}
    if args.max_budget:
        kwargs["max_budget"] = args.max_budget
    if args.review:
        kwargs["review"] = True
    
    if args.fallback:
        result = delegator.delegate_with_fallback(args.prompt)
    else:
        result = delegator.delegate(args.prompt, cli=cli, **kwargs)
    
    # 結果出力
    if args.json:
        print(json.dumps({
            "success": result.success,
            "cli": result.cli,
            "output": result.output,
            "cost_usd": result.cost_usd,
            "session_id": result.session_id,
            "error": result.error
        }, indent=2, ensure_ascii=False))
    else:
        if result.success:
            print(f"\n✓ [{result.cli}] 成功")
            if result.cost_usd:
                print(f"  コスト: ${result.cost_usd:.4f}")
            if result.session_id:
                print(f"  セッションID: {result.session_id}")
            print(f"\n{result.output}")
        else:
            print(f"\n✗ [{result.cli}] 失敗")
            print(f"  エラー: {result.error}")
    
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
