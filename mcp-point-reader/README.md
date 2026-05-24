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

| Tool | Description |
|------|-------------|
| `screenshot_ocr` | Full screenshot + OCR text recognition |
| `capture_clipboard` | Read clipboard text |
| `speak_text` | Speak text aloud (auto-selects Chinese/English voice) |
| `add_vocab` | Add a word to vocabulary |
| `list_vocab` | List vocabulary (with filtering / search) |
| `search_vocab` | Search vocabulary by keyword |
| `mark_learned` | Mark a word as learned |
| `delete_vocab` | Delete a word from vocabulary |
| `get_history` | View reading history |

## Manual Test

```bash
python -m server
```

The server will wait for JSON-RPC messages from an MCP client. Claude Desktop connects automatically — no manual interaction needed.

## License

MIT
