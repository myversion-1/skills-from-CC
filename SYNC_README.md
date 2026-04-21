# Skills 自动同步系统

> 监控 anthropics/skills 更新，确保本地 Skill 始终运行在最新版本

---

## 快速使用

### 手动检查更新
```bash
# 双击运行
D:\skills\check_update.bat

# 或命令行
cd D:/skills
python sync_skills.py --check-only  # 仅检查
python sync_skills.py               # 检查并同步
```

### 设置定时任务（每日 9:00 自动检查）
```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
D:\skills\setup_schedule.ps1
```

### 查看同步日志
```bash
python sync_skills.py --log
```

---

## 文件说明

| 文件 | 用途 |
|------|------|
| `sync_skills.py` | 主同步脚本 |
| `check_update.bat` | Windows 快捷检查脚本 |
| `setup_schedule.ps1` | 创建 Windows 定时任务 |
| `.sync_log.json` | 同步记录（自动生成） |

---

## 同步流程

```
1. 检查 GitHub API 获取 anthropics/skills 最新 commit
2. 对比本地 commit
3. 如有更新:
   - git fetch upstream
   - git merge upstream/main
   - git push origin main
4. 记录同步日志
```

---

## 注意事项

- 本地修改会被 stash（使用 `--force` 时）
- 同步记录保留最近 20 条
- 需要网络连接访问 GitHub API