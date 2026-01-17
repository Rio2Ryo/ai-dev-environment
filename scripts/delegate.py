#!/usr/bin/env python3
"""
Task Delegator - タスク委譲スクリプト

Manusからの指示を受けて、適切なAI CLI（Claude Code, Gemini, Codex）に
タスクを委譲し、結果を返します。

Manusは「司令塔」として機能し、実際の開発作業はClaude Code等の
外部AIに委譲することで、Manusのクレジット消費を抑えます。

使い方:
    # Claude Codeに開発タスクを委譲
    python3 delegate.py claude "ログイン機能を実装してください"
    
    # Geminiに簡単な質問を委譲
    python3 delegate.py gemini "Pythonでリストをソートする方法"
    
    # Codexにコードレビューを委譲
    python3 delegate.py codex --review
    
    # 自動選択モード
    python3 delegate.py auto "タスク内容"
    
    # スキルを指定して実行
    python3 delegate.py claude "Reactコンポーネントを作成" --skill react-best-practices
    
    # 利用可能なスキル一覧
    python3 delegate.py --list-skills
"""

import subprocess
import json
import sys
import os
import argparse
from typing import Optional, Dict, Any, Tuple, List
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path


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
    FRONTEND = "frontend"           # フロントエンド開発
    TESTING = "testing"             # テスト作成


@dataclass
class Skill:
    """スキル情報"""
    name: str
    description: str
    path: Path
    content: str = ""


@dataclass
class DelegationResult:
    """委譲結果"""
    success: bool
    cli: str
    output: str
    cost_usd: Optional[float] = None
    session_id: Optional[str] = None
    error: Optional[str] = None
    skills_used: List[str] = field(default_factory=list)


class SkillManager:
    """スキル管理クラス"""
    
    def __init__(self, skills_dir: Optional[Path] = None):
        # スキルディレクトリの検索順序
        self.skills_dirs = []
        
        # 1. 環境変数で指定されたディレクトリ
        if skills_dir:
            self.skills_dirs.append(skills_dir)
        
        # 2. プロジェクト内のskillsディレクトリ
        script_dir = Path(__file__).parent.parent
        self.skills_dirs.append(script_dir / "skills")
        
        # 3. ~/.claude/skills (Claude Code標準)
        self.skills_dirs.append(Path.home() / ".claude" / "skills")
        
        self._skills_cache: Dict[str, Skill] = {}
    
    def list_skills(self) -> List[Skill]:
        """利用可能なスキル一覧を取得"""
        skills = []
        seen = set()
        
        for skills_dir in self.skills_dirs:
            if not skills_dir.exists():
                continue
            
            # ディレクトリ形式のスキル
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir() and skill_dir.name not in seen:
                    skill_file = skill_dir / "SKILL.md"
                    if skill_file.exists():
                        skill = self._parse_skill(skill_file)
                        if skill:
                            skills.append(skill)
                            seen.add(skill_dir.name)
            
            # ファイル形式のスキル (.md)
            for skill_file in skills_dir.glob("*.md"):
                if skill_file.stem not in seen:
                    skill = self._parse_skill(skill_file)
                    if skill:
                        skills.append(skill)
                        seen.add(skill_file.stem)
        
        return skills
    
    def get_skill(self, name: str) -> Optional[Skill]:
        """スキルを名前で取得"""
        if name in self._skills_cache:
            return self._skills_cache[name]
        
        for skills_dir in self.skills_dirs:
            if not skills_dir.exists():
                continue
            
            # ディレクトリ形式
            skill_dir = skills_dir / name
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    skill = self._parse_skill(skill_file)
                    if skill:
                        self._skills_cache[name] = skill
                        return skill
            
            # ファイル形式
            skill_file = skills_dir / f"{name}.md"
            if skill_file.exists():
                skill = self._parse_skill(skill_file)
                if skill:
                    self._skills_cache[name] = skill
                    return skill
        
        return None
    
    def _parse_skill(self, path: Path) -> Optional[Skill]:
        """スキルファイルをパース"""
        try:
            content = path.read_text(encoding="utf-8")
            
            # フロントマターから名前と説明を抽出
            name = path.stem if path.name != "SKILL.md" else path.parent.name
            description = ""
            
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    for line in frontmatter.strip().split("\n"):
                        if line.startswith("name:"):
                            name = line.split(":", 1)[1].strip()
                        elif line.startswith("description:"):
                            description = line.split(":", 1)[1].strip()
            
            return Skill(
                name=name,
                description=description,
                path=path,
                content=content
            )
        except Exception as e:
            print(f"Warning: Failed to parse skill {path}: {e}", file=sys.stderr)
            return None
    
    def build_prompt_with_skills(self, prompt: str, skill_names: List[str]) -> str:
        """スキルを含むプロンプトを構築"""
        skill_contents = []
        
        for name in skill_names:
            skill = self.get_skill(name)
            if skill:
                skill_contents.append(f"## Skill: {skill.name}\n\n{skill.content}")
            else:
                print(f"Warning: Skill '{name}' not found", file=sys.stderr)
        
        if skill_contents:
            skills_section = "\n\n---\n\n".join(skill_contents)
            return f"""以下のスキル（ガイドライン）に従って作業してください：

{skills_section}

---

## タスク

{prompt}"""
        
        return prompt


class TaskDelegator:
    """タスク委譲を管理するクラス"""
    
    def __init__(self, working_dir: Optional[str] = None, skills_dir: Optional[Path] = None):
        self.working_dir = working_dir or os.getcwd()
        self.skill_manager = SkillManager(skills_dir)
        
        # タスクタイプとCLIのマッピング
        self.task_cli_map = {
            TaskType.DEVELOPMENT: CLI.CLAUDE,
            TaskType.BUGFIX: CLI.CLAUDE,
            TaskType.REVIEW: CLI.CODEX,
            TaskType.REFACTOR: CLI.CLAUDE,
            TaskType.QUESTION: CLI.GEMINI,
            TaskType.DOCUMENTATION: CLI.GEMINI,
            TaskType.FRONTEND: CLI.CLAUDE,
            TaskType.TESTING: CLI.CLAUDE,
        }
        
        # タスクタイプと推奨スキルのマッピング
        self.task_skill_map = {
            TaskType.DEVELOPMENT: [],
            TaskType.BUGFIX: ["systematic-debugging"],
            TaskType.REVIEW: ["code-review"],
            TaskType.REFACTOR: ["react-best-practices"],
            TaskType.QUESTION: [],
            TaskType.DOCUMENTATION: [],
            TaskType.FRONTEND: ["frontend-design", "react-best-practices"],
            TaskType.TESTING: ["webapp-testing"],
        }
    
    def analyze_task(self, prompt: str) -> Tuple[TaskType, List[str]]:
        """プロンプトからタスクタイプと推奨スキルを判定"""
        prompt_lower = prompt.lower()
        
        # タスクタイプ判定
        if any(kw in prompt_lower for kw in ["review", "レビュー", "チェック"]):
            task_type = TaskType.REVIEW
        elif any(kw in prompt_lower for kw in ["bug", "バグ", "エラー", "修正", "fix", "debug"]):
            task_type = TaskType.BUGFIX
        elif any(kw in prompt_lower for kw in ["refactor", "リファクタ", "整理", "改善"]):
            task_type = TaskType.REFACTOR
        elif any(kw in prompt_lower for kw in ["doc", "ドキュメント", "readme", "説明"]):
            task_type = TaskType.DOCUMENTATION
        elif any(kw in prompt_lower for kw in ["?", "？", "how", "what", "why", "どう", "なぜ"]):
            task_type = TaskType.QUESTION
        elif any(kw in prompt_lower for kw in ["test", "テスト", "spec", "jest", "playwright"]):
            task_type = TaskType.TESTING
        elif any(kw in prompt_lower for kw in ["ui", "frontend", "フロントエンド", "react", "component", "コンポーネント", "デザイン", "css", "tailwind"]):
            task_type = TaskType.FRONTEND
        else:
            task_type = TaskType.DEVELOPMENT
        
        # 推奨スキル取得
        recommended_skills = self.task_skill_map.get(task_type, [])
        
        return task_type, recommended_skills
    
    def delegate_to_claude(self, prompt: str, 
                           permission_mode: str = "acceptEdits",
                           max_budget: Optional[float] = None,
                           timeout: int = 300,
                           skills: List[str] = None) -> DelegationResult:
        """Claude Codeにタスクを委譲"""
        
        # スキルを含むプロンプトを構築
        if skills:
            prompt = self.skill_manager.build_prompt_with_skills(prompt, skills)
        
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
                        session_id=data.get("session_id"),
                        skills_used=skills or []
                    )
                except json.JSONDecodeError:
                    return DelegationResult(
                        success=True,
                        cli="claude",
                        output=result.stdout,
                        skills_used=skills or []
                    )
            else:
                return DelegationResult(
                    success=False,
                    cli="claude",
                    output=result.stdout,
                    error=result.stderr,
                    skills_used=skills or []
                )
        except subprocess.TimeoutExpired:
            return DelegationResult(
                success=False,
                cli="claude",
                output="",
                error="Timeout expired",
                skills_used=skills or []
            )
        except FileNotFoundError:
            return DelegationResult(
                success=False,
                cli="claude",
                output="",
                error="Claude CLI not found. Install with: curl -fsSL https://claude.ai/install.sh | bash",
                skills_used=skills or []
            )
        except Exception as e:
            return DelegationResult(
                success=False,
                cli="claude",
                output="",
                error=str(e),
                skills_used=skills or []
            )
    
    def delegate_to_gemini(self, prompt: str,
                           approval_mode: str = "auto_edit",
                           timeout: int = 120,
                           skills: List[str] = None) -> DelegationResult:
        """Gemini CLIにタスクを委譲"""
        
        # スキルを含むプロンプトを構築
        if skills:
            prompt = self.skill_manager.build_prompt_with_skills(prompt, skills)
        
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
                error=result.stderr if result.returncode != 0 else None,
                skills_used=skills or []
            )
        except subprocess.TimeoutExpired:
            return DelegationResult(
                success=False,
                cli="gemini",
                output="",
                error="Timeout expired",
                skills_used=skills or []
            )
        except FileNotFoundError:
            return DelegationResult(
                success=False,
                cli="gemini",
                output="",
                error="Gemini CLI not found. Install with: npm install -g @google/gemini-cli",
                skills_used=skills or []
            )
        except Exception as e:
            return DelegationResult(
                success=False,
                cli="gemini",
                output="",
                error=str(e),
                skills_used=skills or []
            )
    
    def delegate_to_codex(self, prompt: str = "",
                          review: bool = False,
                          sandbox: str = "read-only",
                          timeout: int = 180,
                          skills: List[str] = None) -> DelegationResult:
        """Codex CLIにタスクを委譲"""
        
        # スキルを含むプロンプトを構築
        if skills and prompt:
            prompt = self.skill_manager.build_prompt_with_skills(prompt, skills)
        
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
                error=result.stderr if result.returncode != 0 else None,
                skills_used=skills or []
            )
        except subprocess.TimeoutExpired:
            return DelegationResult(
                success=False,
                cli="codex",
                output="",
                error="Timeout expired",
                skills_used=skills or []
            )
        except FileNotFoundError:
            return DelegationResult(
                success=False,
                cli="codex",
                output="",
                error="Codex CLI not found. Install with: npm install -g @openai/codex",
                skills_used=skills or []
            )
        except Exception as e:
            return DelegationResult(
                success=False,
                cli="codex",
                output="",
                error=str(e),
                skills_used=skills or []
            )
    
    def delegate(self, prompt: str, 
                 cli: Optional[CLI] = None,
                 skills: List[str] = None,
                 auto_skills: bool = True,
                 **kwargs) -> DelegationResult:
        """タスクを適切なCLIに委譲"""
        
        # CLI未指定の場合は自動選択
        task_type = None
        recommended_skills = []
        
        if cli is None:
            task_type, recommended_skills = self.analyze_task(prompt)
            cli = self.task_cli_map[task_type]
            print(f"[Auto] Task type: {task_type.value} -> CLI: {cli.value}")
        
        # スキルの決定
        final_skills = skills or []
        if auto_skills and not skills and recommended_skills:
            final_skills = recommended_skills
            print(f"[Auto] Recommended skills: {', '.join(final_skills)}")
        
        # 委譲実行
        if cli == CLI.CLAUDE:
            return self.delegate_to_claude(prompt, skills=final_skills, **kwargs)
        elif cli == CLI.GEMINI:
            return self.delegate_to_gemini(prompt, skills=final_skills, **kwargs)
        elif cli == CLI.CODEX:
            return self.delegate_to_codex(prompt, skills=final_skills, **kwargs)
        else:
            return DelegationResult(
                success=False,
                cli="unknown",
                output="",
                error=f"Unknown CLI: {cli}"
            )
    
    def delegate_with_fallback(self, prompt: str,
                               fallback_chain: list = None,
                               skills: List[str] = None) -> DelegationResult:
        """フォールバック付きで委譲"""
        if fallback_chain is None:
            fallback_chain = [CLI.CLAUDE, CLI.GEMINI, CLI.CODEX]
        
        for cli in fallback_chain:
            print(f"[Trying] {cli.value}...")
            result = self.delegate(prompt, cli=cli, skills=skills, auto_skills=False)
            
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
  
  # 自動選択モード（タスクタイプとスキルを自動判定）
  python3 delegate.py auto "タスク内容"
  
  # スキルを指定して実行
  python3 delegate.py claude "Reactコンポーネントを作成" --skill react-best-practices
  
  # フォールバック付き
  python3 delegate.py auto "タスク内容" --fallback
  
  # 利用可能なスキル一覧
  python3 delegate.py --list-skills
"""
    )
    
    parser.add_argument("cli", nargs="?", choices=["claude", "gemini", "codex", "auto"],
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
    parser.add_argument("--skill", action="append", dest="skills",
                        help="使用するスキル（複数指定可）")
    parser.add_argument("--no-auto-skills", action="store_true",
                        help="スキルの自動選択を無効化")
    parser.add_argument("--list-skills", action="store_true",
                        help="利用可能なスキル一覧を表示")
    
    args = parser.parse_args()
    
    delegator = TaskDelegator(working_dir=args.working_dir)
    
    # スキル一覧表示
    if args.list_skills:
        skills = delegator.skill_manager.list_skills()
        if skills:
            print("利用可能なスキル:\n")
            for skill in skills:
                print(f"  {skill.name}")
                if skill.description:
                    print(f"    {skill.description[:80]}...")
                print()
        else:
            print("スキルが見つかりません")
        return
    
    # CLI未指定の場合はヘルプ表示
    if not args.cli:
        parser.print_help()
        return
    
    # CLI選択
    cli_map = {
        "claude": CLI.CLAUDE,
        "gemini": CLI.GEMINI,
        "codex": CLI.CODEX,
        "auto": None
    }
    cli = cli_map[args.cli]
    
    # 委譲実行
    kwargs = {
        "timeout": args.timeout,
        "auto_skills": not args.no_auto_skills
    }
    if args.max_budget:
        kwargs["max_budget"] = args.max_budget
    if args.review:
        kwargs["review"] = True
    if args.skills:
        kwargs["skills"] = args.skills
    
    if args.fallback:
        result = delegator.delegate_with_fallback(args.prompt, skills=args.skills)
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
            "error": result.error,
            "skills_used": result.skills_used
        }, indent=2, ensure_ascii=False))
    else:
        if result.success:
            print(f"\n✓ [{result.cli}] 成功")
            if result.cost_usd:
                print(f"  コスト: ${result.cost_usd:.4f}")
            if result.session_id:
                print(f"  セッションID: {result.session_id}")
            if result.skills_used:
                print(f"  使用スキル: {', '.join(result.skills_used)}")
            print(f"\n{result.output}")
        else:
            print(f"\n✗ [{result.cli}] 失敗")
            print(f"  エラー: {result.error}")
    
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
