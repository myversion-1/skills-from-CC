# CLAUDE.md

## Project Overview
Anthropic 的 Claude 技能示例仓库，展示了 Claude Code 技能系统的各种用法，包括文档创建（docx/pdf/pptx/xlsx）、MCP 服务器构建、API 调用等。

## Tech Stack
- **主要语言**: Markdown (SKILL.md), Python, PowerShell
- **关键依赖**: 无 Node.js 依赖，纯技能定义仓库

## Key Files
- `skills/` - 技能文件夹（17 个子目录）
- `spec/agent-skills-spec.md` - Agent Skills 规范
- `template/SKILL.md` - 技能创建模板
- `sync_skills.py` - 同步脚本

## Commands
- 无标准 npm 命令，技能通过 Claude Code 加载

## Architecture
每个技能是一个独立文件夹，包含 SKILL.md 文件定义指令和元数据。部分技能有子文件夹存放参考文档或模板。

## Skills List
- algorithmic-art - 算法艺术生成
- brand-guidelines - 品牌指南
- canvas-design - Canvas 设计
- claude-api - Claude API 使用指南
- doc-coauthoring - 文档协作
- docx - Word 文档创建
- frontend-design - 前端设计
- internal-comms - 内部通讯
- mcp-builder - MCP 服务器构建
- pdf - PDF 处理
- pptx - PPT 创建
- skill-creator - 技能创建器
- slack-gif-creator - Slack GIF 创建
- theme-factory - 主题工厂
- web-artifacts-builder - Web 产物构建
- webapp-testing - Web 应用测试
- xlsx - Excel 表格处理
