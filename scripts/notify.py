#!/usr/bin/env python3
"""
Notify - 開発完了通知スクリプト

開発タスクの完了をLINEに通知します。
Manus MCP経由でLINE Messaging APIを使用します。

使い方:
    # シンプルな通知
    python3 notify.py "開発が完了しました"
    
    # 詳細な通知（タイトル付き）
    python3 notify.py "ログイン機能の実装が完了" --title "開発完了"
    
    # 成功/失敗ステータス付き
    python3 notify.py "テストが全て通過" --status success
    python3 notify.py "ビルドに失敗しました" --status error
    
    # Flex Message形式
    python3 notify.py "詳細レポート" --flex --title "日次レポート"
"""

import subprocess
import json
import sys
import argparse
from typing import Optional, Dict, Any
from datetime import datetime


def send_line_message(message: str, 
                      title: Optional[str] = None,
                      status: Optional[str] = None,
                      use_flex: bool = False) -> bool:
    """
    LINE MCPを使用してメッセージを送信
    
    Args:
        message: 送信するメッセージ
        title: メッセージのタイトル（オプション）
        status: ステータス（success, error, info）
        use_flex: Flex Messageを使用するか
    
    Returns:
        送信成功したかどうか
    """
    
    if use_flex:
        return send_flex_message(message, title, status)
    else:
        return send_text_message(message, title, status)


def send_text_message(message: str, 
                      title: Optional[str] = None,
                      status: Optional[str] = None) -> bool:
    """シンプルなテキストメッセージを送信"""
    
    # ステータスに応じた絵文字
    status_emoji = {
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "info": "ℹ️"
    }
    
    emoji = status_emoji.get(status, "📢")
    
    # メッセージ構築
    full_message = f"{emoji} "
    if title:
        full_message += f"【{title}】\n"
    full_message += message
    full_message += f"\n\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # LINE MCP経由で送信（broadcast_text_message）
    input_json = json.dumps({
        "message": {
            "type": "text",
            "text": full_message
        }
    })
    
    cmd = [
        "manus-mcp-cli", "tool", "call", "broadcast_text_message",
        "--server", "line",
        "--input", input_json
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✓ LINE通知を送信しました")
            return True
        else:
            print(f"✗ LINE通知の送信に失敗: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ タイムアウト")
        return False
    except FileNotFoundError:
        print("✗ manus-mcp-cli が見つかりません")
        return False
    except Exception as e:
        print(f"✗ エラー: {e}")
        return False


def send_flex_message(message: str,
                      title: Optional[str] = None,
                      status: Optional[str] = None) -> bool:
    """Flex Messageを送信"""
    
    # ステータスに応じた色
    status_colors = {
        "success": "#00C851",
        "error": "#ff4444",
        "warning": "#ffbb33",
        "info": "#33b5e5"
    }
    
    color = status_colors.get(status, "#1DB446")
    
    # Flex Message構築（header, body, footer全て必須）
    flex_content = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": color,
            "contents": [
                {
                    "type": "text",
                    "text": title or "通知",
                    "color": "#ffffff",
                    "weight": "bold",
                    "size": "lg"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": message,
                    "wrap": True,
                    "size": "md"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "color": "#aaaaaa",
                    "size": "xs",
                    "align": "end"
                }
            ]
        }
    }
    
    # LINE MCP経由で送信（broadcast_flex_message）
    input_json = json.dumps({
        "altText": title or "開発通知",
        "contents": flex_content
    })
    
    cmd = [
        "manus-mcp-cli", "tool", "call", "broadcast_flex_message",
        "--server", "line",
        "--input", input_json
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✓ LINE Flex通知を送信しました")
            return True
        else:
            print(f"✗ LINE通知の送信に失敗: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ エラー: {e}")
        return False


def send_development_report(
    task: str,
    cli: str,
    success: bool,
    duration: Optional[float] = None,
    cost: Optional[float] = None,
    files_changed: Optional[int] = None
) -> bool:
    """開発レポートを送信"""
    
    status = "success" if success else "error"
    
    # レポート内容構築
    lines = [
        f"タスク: {task}",
        f"実行AI: {cli.upper()}",
        f"結果: {'成功' if success else '失敗'}"
    ]
    
    if duration:
        lines.append(f"所要時間: {duration:.1f}秒")
    if cost:
        lines.append(f"コスト: ${cost:.4f}")
    if files_changed:
        lines.append(f"変更ファイル数: {files_changed}")
    
    message = "\n".join(lines)
    
    return send_flex_message(
        message=message,
        title="開発タスク完了",
        status=status
    )


def main():
    parser = argparse.ArgumentParser(
        description="開発完了通知をLINEに送信",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  # シンプルな通知
  python3 notify.py "開発が完了しました"
  
  # タイトル付き
  python3 notify.py "ログイン機能の実装が完了" --title "開発完了"
  
  # ステータス付き
  python3 notify.py "テストが全て通過" --status success
  
  # Flex Message形式
  python3 notify.py "詳細レポート" --flex --title "日次レポート"
"""
    )
    
    parser.add_argument("message", help="送信するメッセージ")
    parser.add_argument("--title", "-t", help="メッセージのタイトル")
    parser.add_argument("--status", "-s", 
                        choices=["success", "error", "warning", "info"],
                        help="ステータス")
    parser.add_argument("--flex", "-f", action="store_true",
                        help="Flex Message形式で送信")
    
    args = parser.parse_args()
    
    success = send_line_message(
        message=args.message,
        title=args.title,
        status=args.status,
        use_flex=args.flex
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
