#!/usr/bin/env python3
"""
AI Orchestrator - スマホ完結型AI開発環境の中核スクリプト

複数のAIモデル（Claude, GPT, Gemini, Grok）を統合し、
タスクに応じて最適なモデルを選択・実行します。
"""

import os
import json
import subprocess
from typing import Optional, Dict, Any, Literal
from dataclasses import dataclass
from enum import Enum

# SDKインポート
import anthropic
import openai
from google import genai


class TaskType(Enum):
    """タスクの種類を定義"""
    SIMPLE_CODE = "simple_code"          # 簡単なコード生成
    COMPLEX_ALGORITHM = "complex_algorithm"  # 複雑なアルゴリズム
    CODE_REVIEW = "code_review"          # コードレビュー
    DEBUGGING = "debugging"              # デバッグ
    DOCUMENTATION = "documentation"      # ドキュメント作成
    RESEARCH = "research"                # 調査・検索
    FRONTEND = "frontend"                # フロントエンド開発


@dataclass
class AIResponse:
    """AIからのレスポンスを格納"""
    model: str
    content: str
    tokens_used: Optional[int] = None
    cost_estimate: Optional[float] = None


class AIOrchestrator:
    """複数のAIモデルを統合管理するオーケストレーター"""
    
    def __init__(self):
        # APIキーを環境変数から取得
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.xai_key = os.getenv("XAI_API_KEY")
        
        # クライアント初期化
        self._init_clients()
        
        # タスクタイプとモデルのマッピング
        self.task_model_map = {
            TaskType.SIMPLE_CODE: ["gemini", "grok-code-fast"],
            TaskType.COMPLEX_ALGORITHM: ["gpt-5", "claude-opus"],
            TaskType.CODE_REVIEW: ["grok-code-fast", "codex"],
            TaskType.DEBUGGING: ["claude", "gemini"],
            TaskType.DOCUMENTATION: ["gemini", "gpt-4o"],
            TaskType.RESEARCH: ["grok-web", "gemini-search"],
            TaskType.FRONTEND: ["claude", "gpt-5"],
        }
    
    def _init_clients(self):
        """各AIサービスのクライアントを初期化"""
        self.clients = {}
        
        if self.anthropic_key:
            self.clients["anthropic"] = anthropic.Anthropic(
                api_key=self.anthropic_key
            )
        
        if self.openai_key:
            base_url = os.getenv("OPENAI_API_BASE")
            if base_url:
                self.clients["openai"] = openai.OpenAI(
                    api_key=self.openai_key,
                    base_url=base_url
                )
            else:
                self.clients["openai"] = openai.OpenAI(
                    api_key=self.openai_key
                )
        
        if self.gemini_key:
            self.clients["gemini"] = genai.Client(
                api_key=self.gemini_key
            )
    
    def analyze_task(self, prompt: str) -> TaskType:
        """プロンプトを分析してタスクタイプを判定"""
        prompt_lower = prompt.lower()
        
        # キーワードベースの簡易判定
        if any(kw in prompt_lower for kw in ["review", "レビュー", "チェック"]):
            return TaskType.CODE_REVIEW
        elif any(kw in prompt_lower for kw in ["debug", "バグ", "エラー", "修正"]):
            return TaskType.DEBUGGING
        elif any(kw in prompt_lower for kw in ["frontend", "ui", "react", "css", "デザイン"]):
            return TaskType.FRONTEND
        elif any(kw in prompt_lower for kw in ["algorithm", "アルゴリズム", "最適化", "複雑"]):
            return TaskType.COMPLEX_ALGORITHM
        elif any(kw in prompt_lower for kw in ["doc", "ドキュメント", "説明", "readme"]):
            return TaskType.DOCUMENTATION
        elif any(kw in prompt_lower for kw in ["search", "調査", "検索", "最新"]):
            return TaskType.RESEARCH
        else:
            return TaskType.SIMPLE_CODE
    
    def call_claude(self, prompt: str, model: str = "claude-sonnet-4-20250514") -> AIResponse:
        """Claude APIを呼び出し"""
        if "anthropic" not in self.clients:
            raise ValueError("Anthropic API key not configured")
        
        response = self.clients["anthropic"].messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return AIResponse(
            model=model,
            content=response.content[0].text,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens
        )
    
    def call_openai(self, prompt: str, model: str = "gpt-4o") -> AIResponse:
        """OpenAI APIを呼び出し"""
        if "openai" not in self.clients:
            raise ValueError("OpenAI API key not configured")
        
        response = self.clients["openai"].chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return AIResponse(
            model=model,
            content=response.choices[0].message.content,
            tokens_used=response.usage.total_tokens if response.usage else None
        )
    
    def call_gemini(self, prompt: str, model: str = "gemini-2.5-flash") -> AIResponse:
        """Gemini APIを呼び出し"""
        if "gemini" not in self.clients:
            raise ValueError("Gemini API key not configured")
        
        response = self.clients["gemini"].models.generate_content(
            model=model,
            contents=prompt
        )
        
        return AIResponse(
            model=model,
            content=response.text
        )
    
    def call_gemini_cli(self, prompt: str) -> AIResponse:
        """Gemini CLIを非対話モードで呼び出し"""
        result = subprocess.run(
            ["gemini", "-p", prompt, "--output-format", "json"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Gemini CLI error: {result.stderr}")
        
        return AIResponse(
            model="gemini-cli",
            content=result.stdout
        )
    
    def execute(self, prompt: str, task_type: Optional[TaskType] = None) -> AIResponse:
        """タスクを実行し、最適なAIモデルを選択して呼び出し"""
        if task_type is None:
            task_type = self.analyze_task(prompt)
        
        preferred_models = self.task_model_map.get(task_type, ["gemini"])
        
        # 最初の利用可能なモデルを使用
        for model_hint in preferred_models:
            try:
                if "gemini" in model_hint:
                    return self.call_gemini(prompt)
                elif "claude" in model_hint:
                    return self.call_claude(prompt)
                elif "gpt" in model_hint or "codex" in model_hint:
                    return self.call_openai(prompt)
            except Exception as e:
                print(f"Model {model_hint} failed: {e}, trying next...")
                continue
        
        # フォールバック: Gemini CLI
        return self.call_gemini_cli(prompt)
    
    def get_available_models(self) -> Dict[str, bool]:
        """利用可能なモデルを確認"""
        return {
            "anthropic": "anthropic" in self.clients,
            "openai": "openai" in self.clients,
            "gemini": "gemini" in self.clients,
            "gemini_cli": subprocess.run(
                ["which", "gemini"], capture_output=True
            ).returncode == 0,
            "codex_cli": subprocess.run(
                ["which", "codex"], capture_output=True
            ).returncode == 0,
            "claude_cli": subprocess.run(
                ["which", "claude"], capture_output=True
            ).returncode == 0,
        }


def main():
    """メイン関数 - CLIインターフェース"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Orchestrator")
    parser.add_argument("prompt", nargs="?", help="Prompt to send to AI")
    parser.add_argument("--task", choices=[t.value for t in TaskType], 
                        help="Specify task type")
    parser.add_argument("--model", help="Force specific model")
    parser.add_argument("--check", action="store_true", 
                        help="Check available models")
    
    args = parser.parse_args()
    
    orchestrator = AIOrchestrator()
    
    if args.check:
        models = orchestrator.get_available_models()
        print("Available Models:")
        for model, available in models.items():
            status = "✓" if available else "✗"
            print(f"  {status} {model}")
        return
    
    if not args.prompt:
        parser.print_help()
        return
    
    task_type = TaskType(args.task) if args.task else None
    response = orchestrator.execute(args.prompt, task_type)
    
    print(f"\n[Model: {response.model}]")
    print("-" * 40)
    print(response.content)
    
    if response.tokens_used:
        print(f"\n[Tokens used: {response.tokens_used}]")


if __name__ == "__main__":
    main()
