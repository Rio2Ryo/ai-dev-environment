#!/usr/bin/env python3
"""
Debug Helper - 体系的デバッグ支援スクリプト

systematic-debuggingスキルと連携し、
4フェーズのデバッグプロセスを支援します。
"""

import os
from typing import Optional
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ai_orchestrator import AIOrchestrator, TaskType, AIResponse


class DebugHelper:
    """体系的デバッグを支援するヘルパークラス"""
    
    def __init__(self):
        self.orchestrator = AIOrchestrator()
        self.skills_path = os.path.expanduser("~/.claude/skills")
        self.debug_skill = self._load_skill("systematic-debugging.md")
    
    def _load_skill(self, filename: str) -> Optional[str]:
        """スキルファイルを読み込み"""
        filepath = os.path.join(self.skills_path, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return f.read()
        return None
    
    def _build_prompt(self, request: str) -> str:
        """スキルを含めたプロンプトを構築"""
        if self.debug_skill:
            return f"<skill>\n{self.debug_skill}\n</skill>\n\n<request>\n{request}\n</request>"
        return request
    
    def analyze_error(self, error_message: str, code_context: str = "") -> AIResponse:
        """エラーメッセージを分析"""
        prompt = self._build_prompt(f"""
以下のエラーを分析し、根本原因と解決策を提案してください。

エラーメッセージ:
```
{error_message}
```

{"コードコンテキスト:" if code_context else ""}
{"```" if code_context else ""}
{code_context}
{"```" if code_context else ""}

分析内容:
1. エラーの種類と意味
2. 考えられる原因（複数）
3. 各原因の検証方法
4. 推奨される修正方法
""")
        return self.orchestrator.execute(prompt, TaskType.DEBUGGING)
    
    def generate_hypothesis(self, symptom: str, context: str = "") -> AIResponse:
        """バグの仮説を生成"""
        prompt = self._build_prompt(f"""
以下の症状に対する仮説を生成してください。

症状:
{symptom}

{"コンテキスト:" if context else ""}
{context}

各仮説について:
1. 仮説の説明
2. この仮説が正しい場合に観察されるはずの現象
3. 検証方法
4. 確率の見積もり（高/中/低）
""")
        return self.orchestrator.execute(prompt, TaskType.DEBUGGING)
    
    def suggest_logging(self, code: str) -> AIResponse:
        """デバッグ用のログ追加を提案"""
        prompt = f"""
以下のコードにデバッグ用のログを追加する場所を提案してください。

```
{code}
```

提案内容:
1. ログを追加すべき場所
2. 各ログで記録すべき情報
3. ログレベル（debug/info/warn/error）
4. 実際のログ文の例
"""
        return self.orchestrator.execute(prompt, TaskType.DEBUGGING)
    
    def verify_fix(self, original_issue: str, fix_description: str, 
                   fixed_code: str) -> AIResponse:
        """修正の検証"""
        prompt = self._build_prompt(f"""
以下の修正が適切かどうか検証してください。

元の問題:
{original_issue}

修正内容:
{fix_description}

修正後のコード:
```
{fixed_code}
```

検証項目:
1. 元の問題は解決されているか
2. 新たな問題が発生していないか
3. エッジケースは考慮されているか
4. 同様の問題が他にないか
5. リグレッションテストの提案
""")
        return self.orchestrator.execute(prompt, TaskType.CODE_REVIEW)


def main():
    """CLIインターフェース"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Debug Helper")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # analyze コマンド
    analyze_parser = subparsers.add_parser("analyze", help="Analyze an error")
    analyze_parser.add_argument("error", help="Error message")
    analyze_parser.add_argument("--code", help="Code file for context")
    
    # hypothesis コマンド
    hypo_parser = subparsers.add_parser("hypothesis", help="Generate hypotheses")
    hypo_parser.add_argument("symptom", help="Bug symptom description")
    
    # logging コマンド
    log_parser = subparsers.add_parser("logging", help="Suggest logging")
    log_parser.add_argument("file", help="Code file")
    
    # verify コマンド
    verify_parser = subparsers.add_parser("verify", help="Verify a fix")
    verify_parser.add_argument("issue", help="Original issue")
    verify_parser.add_argument("fix", help="Fix description")
    verify_parser.add_argument("file", help="Fixed code file")
    
    args = parser.parse_args()
    helper = DebugHelper()
    
    if args.command == "analyze":
        code = ""
        if args.code:
            with open(args.code, "r") as f:
                code = f.read()
        response = helper.analyze_error(args.error, code)
        print(response.content)
    
    elif args.command == "hypothesis":
        response = helper.generate_hypothesis(args.symptom)
        print(response.content)
    
    elif args.command == "logging":
        with open(args.file, "r") as f:
            code = f.read()
        response = helper.suggest_logging(code)
        print(response.content)
    
    elif args.command == "verify":
        with open(args.file, "r") as f:
            code = f.read()
        response = helper.verify_fix(args.issue, args.fix, code)
        print(response.content)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
