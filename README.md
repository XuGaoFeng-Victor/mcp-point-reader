# MCP Point Reader

Expose [Point Reader] features to AI assistants (Claude Desktop, etc.) through the MCP protocol, enabling:

- Screenshot OCR
- Clipboard text capture
- Text-to-speech (offline / online TTS)
- Vocabulary management (add, list, search, mark learned, delete)
- Reading history query

## Prerequisites

- Python 3.10+
- [Point Reader] installed with `config.json` and `data.db` generated

## Installation

```bash
cd mcp-point-reader
pip install -e .
```

Dependencies: `mcp`, `PyQt5`, `edge-tts`, `pyttsx3`, `pyperclip`, `pytesseract`, `Pillow`, `pynput`

## Configuration

The MCP plugin reads Point Reader's config automatically. The default path is `D:\English`.

If Point Reader is installed elsewhere, set the environment variable:

```bash
set POINT_READER_DIR=D:\your-path\English
```

## Usage with Claude Desktop

Edit `claude_desktop_config.json` (located at `%APPDATA%\Claude\`):

```json
{
  "mcpServers": {
    "point-reader": {
      "command": "python",
      "args": ["-m", "server"],
      "cwd": "D:\\mcp-point-reader"
    }
  }
}
```

> Replace `cwd` with the actual project path.

Restart Claude Desktop. The AI can now use Point Reader's features in conversations.

## Available Tools

| Tool                | Description                                           |
| ------------------- | ----------------------------------------------------- |
| `screenshot_ocr`    | Full screenshot + OCR text recognition                |
| `capture_clipboard` | Read clipboard text                                   |
| `speak_text`        | Speak text aloud (auto-selects Chinese/English voice) |
| `add_vocab`         | Add a word to vocabulary                              |
| `list_vocab`        | List vocabulary (with filtering / search)             |
| `search_vocab`      | Search vocabulary by keyword                          |
| `mark_learned`      | Mark a word as learned                                |
| `delete_vocab`      | Delete a word from vocabulary                         |
| `get_history`       | View reading history                                  |

## Manual Test

```bash
python -m server
```

The server will wait for JSON-RPC messages from an MCP client. Claude Desktop connects automatically — no manual interaction needed.

## License

MIT
# MCP Point Reader

通过 MCP 协议向 AI 助手（Claude Desktop 等）暴露[点读助手]的功能，让 AI 可以：

- 截图识别文字（OCR）
- 读取剪贴板内容
- 朗读文本（离线 / 在线 TTS）
- 管理生词本（增删改查、标记已掌握）
- 查看朗读历史

## 前置条件

- Python 3.10+
- [点读助手]已安装，并已生成 `config.json` 和 `data.db`

## 安装

```bash
# 克隆或进入项目目录
cd mcp-point-reader

# 安装依赖
pip install -e .
```

> 国内网络慢可加镜像：`pip install -e . -i https://mirrors.aliyun.com/pypi/simple/`

依赖包括：`mcp`, `PyQt5`, `edge-tts`, `pyttsx3`, `pyperclip`, `pytesseract`, `Pillow`, `pynput`

## 配置

MCP 插件会自动读取点读助手的配置文件，默认路径为 `D:\English\`。

如果点读助手安装在其他位置，设置环境变量：

```bash
set POINT_READER_DIR=D:\your-path\English
```

## 在 Claude Desktop 中使用

编辑 `claude_desktop_config.json`（位于 `%APPDATA%\Claude\`）：

```json
{
  "mcpServers": {
    "point-reader": {
      "command": "python",
      "args": ["-m", "server"],
      "cwd": "D:\\mcp-point-reader"
    }
  }
}
```

> `cwd` 替换为实际的项目所在路径。

保存后重启 Claude Desktop，即可在对话中让 AI 使用点读助手的功能。

## 可用工具

| 工具                | 说明                               |
| ------------------- | ---------------------------------- |
| `screenshot_ocr`    | 全屏截图并识别文字                 |
| `capture_clipboard` | 读取剪贴板文本                     |
| `speak_text`        | 朗读指定文本（自动选择中英文语音） |
| `add_vocab`         | 添加单词到生词本                   |
| `list_vocab`        | 查看生词本（支持筛选/搜索）        |
| `search_vocab`      | 搜索生词本中的单词                 |
| `mark_learned`      | 标记单词为已掌握                   |
| `delete_vocab`      | 从生词本中删除单词                 |
| `get_history`       | 查看朗读历史                       |

## 手动测试

```bash
python -m server
```

启动后程序会等待 MCP 客户端的 JSON-RPC 消息。可配合 Claude Desktop 自动连接，无需手动操作。

## 许可证

MIT
