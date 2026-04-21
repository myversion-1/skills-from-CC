#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skills 同步工具 - 监控并同步 anthropics/skills 更新

功能：
1. 检查 upstream (anthropics/skills) 是否有新 commit
2. 自动同步到本地并推送到 fork
3. 记录同步日志

使用方法：
    python sync_skills.py              # 检查并同步
    python sync_skills.py --check-only # 仅检查，不同步
    python sync_skills.py --force      # 强制同步（覆盖本地修改）
"""

import subprocess
import sys
import json
import os
from datetime import datetime
from pathlib import Path

# Windows 终端编码
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8")

# 配置
REPO_PATH = Path("D:/skills")
UPSTREAM_REPO = "anthropics/skills"
UPSTREAM_URL = f"https://github.com/{UPSTREAM_REPO}"
LOG_FILE = REPO_PATH / ".sync_log.json"


def run_git(args: list, check: bool = True) -> tuple[int, str, str]:
    """执行 git 命令"""
    result = subprocess.run(
        ["git"] + args,
        cwd=REPO_PATH,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def get_local_commit() -> str:
    """获取本地 HEAD commit"""
    _, stdout, _ = run_git(["rev-parse", "HEAD"])
    return stdout[:7] if stdout else "unknown"


def get_upstream_commit() -> str | None:
    """获取 upstream 最新 commit（不 fetch）"""
    # 使用 GitHub API 获取最新 commit
    import urllib.request
    try:
        url = f"https://api.github.com/repos/{UPSTREAM_REPO}/commits/main"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data["sha"][:7]
    except Exception as e:
        print(f"⚠️ 无法获取 upstream commit: {e}")
        return None


def fetch_upstream() -> bool:
    """Fetch upstream"""
    print("📥 Fetching upstream...")
    returncode, stdout, stderr = run_git(["fetch", "upstream"])
    if returncode != 0:
        print(f"❌ Fetch 失败: {stderr}")
        return False
    return True


def has_local_changes() -> bool:
    """检查是否有本地修改"""
    _, stdout, _ = run_git(["status", "--porcelain"])
    return bool(stdout)


def sync(check_only: bool = False, force: bool = False) -> bool:
    """
    同步 upstream 到本地

    Args:
        check_only: 仅检查，不执行同步
        force: 强制同步，覆盖本地修改

    Returns:
        bool: 是否有更新
    """
    print(f"🔍 检查 {UPSTREAM_REPO} 更新...")
    print(f"   本地路径: {REPO_PATH}")

    local_commit = get_local_commit()
    print(f"   本地 commit: {local_commit}")

    # 获取 upstream 最新 commit
    upstream_commit = get_upstream_commit()
    if not upstream_commit:
        print("❌ 无法获取 upstream 状态")
        return False

    print(f"   Upstream commit: {upstream_commit}")

    if local_commit == upstream_commit:
        print("✅ 已是最新版本，无需同步")
        return False

    print(f"\n🆕 发现新版本! {local_commit} → {upstream_commit}")

    if check_only:
        print("ℹ️ 仅检查模式，不执行同步")
        return True

    # 检查本地修改
    if has_local_changes():
        if force:
            print("⚠️ 本地有修改，强制同步将覆盖...")
            run_git(["stash"])
        else:
            print("❌ 本地有未提交的修改，请先处理或使用 --force")
            return False

    # 执行同步
    print("\n🚀 开始同步...")

    # 1. Fetch upstream
    if not fetch_upstream():
        return False

    # 2. Merge upstream/main
    print("🔀 Merging upstream/main...")
    returncode, stdout, stderr = run_git(["merge", "upstream/main", "--ff-only"])
    if returncode != 0:
        print(f"❌ Merge 失败: {stderr}")
        print("💡 尝试硬重置...")
        run_git(["reset", "--hard", "upstream/main"])

    # 3. Push to origin
    print("📤 Pushing to origin...")
    returncode, stdout, stderr = run_git(["push", "origin", "main"])
    if returncode != 0:
        print(f"⚠️ Push 失败: {stderr}")
    else:
        print("✅ Push 成功")

    # 记录日志
    log_sync(local_commit, upstream_commit)

    print(f"\n✅ 同步完成! {local_commit} → {upstream_commit}")
    return True


def log_sync(from_commit: str, to_commit: str):
    """记录同步日志"""
    logs = []
    if LOG_FILE.exists():
        try:
            logs = json.loads(LOG_FILE.read_text())
        except:
            logs = []

    logs.append({
        "timestamp": datetime.now().isoformat(),
        "from": from_commit,
        "to": to_commit,
        "repo": UPSTREAM_REPO
    })

    # 只保留最近 20 条记录
    logs = logs[-20:]
    LOG_FILE.write_text(json.dumps(logs, indent=2))


def show_log():
    """显示同步日志"""
    if not LOG_FILE.exists():
        print("暂无同步记录")
        return

    logs = json.loads(LOG_FILE.read_text())
    print(f"\n📜 最近 {len(logs)} 次同步记录:")
    print("-" * 60)
    for log in reversed(logs):
        ts = log["timestamp"][:19].replace("T", " ")
        print(f"  {ts} | {log['from']} → {log['to']}")


def main():
    check_only = "--check-only" in sys.argv
    force = "--force" in sys.argv
    show_logs = "--log" in sys.argv

    if show_logs:
        show_log()
        return

    if not REPO_PATH.exists():
        print(f"❌ 仓库路径不存在: {REPO_PATH}")
        sys.exit(1)

    print("=" * 60)
    print("🔄 Skills 同步工具")
    print("=" * 60)

    has_updates = sync(check_only=check_only, force=force)

    if check_only and has_updates:
        sys.exit(1)  # 有更新时返回非零退出码，便于脚本检测

    print("=" * 60)


if __name__ == "__main__":
    main()