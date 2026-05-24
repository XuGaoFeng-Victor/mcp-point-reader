"""MCP 工具定义。"""

from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server

from . import db, tts, capture

server = Server("point-reader")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="screenshot_ocr",
            description="全屏截图并识别文字（OCR），适合无法选中的屏幕文本。返回识别出的文本内容。",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="capture_clipboard",
            description="读取当前系统剪贴板中的选中文本。返回文本内容。",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="speak_text",
            description="朗读指定文本。支持中文和英文，自动选择语音。",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "要朗读的文字内容",
                    }
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="add_vocab",
            description="添加单词到点读助手的生词本。",
            inputSchema={
                "type": "object",
                "properties": {
                    "word": {"type": "string", "description": "单词"},
                    "source_sentence": {
                        "type": "string",
                        "description": "单词所在的原文句子（可选）",
                    },
                    "notes": {"type": "string", "description": "备注（可选）"},
                },
                "required": ["word"],
            },
        ),
        types.Tool(
            name="list_vocab",
            description="查看生词本中的单词列表。",
            inputSchema={
                "type": "object",
                "properties": {
                    "learned": {
                        "type": "boolean",
                        "description": "筛选已掌握/学习中，不填则全部显示",
                    },
                    "keyword": {
                        "type": "string",
                        "description": "搜索关键词",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "返回数量上限，默认 50",
                        "default": 50,
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="search_vocab",
            description="在生词本中搜索包含关键词的单词。",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "搜索关键词"},
                },
                "required": ["keyword"],
            },
        ),
        types.Tool(
            name="mark_learned",
            description="标记单词为已掌握。",
            inputSchema={
                "type": "object",
                "properties": {
                    "word_id": {
                        "type": "integer",
                        "description": "单词 ID（通过 list_vocab 获取）",
                    },
                    "learned": {
                        "type": "boolean",
                        "description": "True=已掌握，False=学习中",
                    },
                },
                "required": ["word_id"],
            },
        ),
        types.Tool(
            name="delete_vocab",
            description="从生词本中删除单词。",
            inputSchema={
                "type": "object",
                "properties": {
                    "word_id": {
                        "type": "integer",
                        "description": "要删除的单词 ID",
                    },
                },
                "required": ["word_id"],
            },
        ),
        types.Tool(
            name="get_history",
            description="查看点读助手的朗读历史记录。",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "返回数量上限，默认 20",
                        "default": 20,
                    },
                    "keyword": {
                        "type": "string",
                        "description": "搜索关键词",
                    },
                },
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.EmbeddedResource]:
    if arguments is None:
        arguments = {}

    if name == "screenshot_ocr":
        text = capture.screenshot_ocr()
        if text:
            return [types.TextContent(type="text", text=text)]
        return [types.TextContent(type="text", text="未识别到文字")]

    elif name == "capture_clipboard":
        text = capture.capture_clipboard()
        if text:
            return [types.TextContent(type="text", text=text)]
        return [types.TextContent(type="text", text="剪贴板中没有文本")]

    elif name == "speak_text":
        text = arguments.get("text", "")
        if not text:
            return [types.TextContent(type="text", text="请提供要朗读的文字")]
        result = tts.speak(text)
        return [types.TextContent(type="text", text=result)]

    elif name == "add_vocab":
        word = arguments.get("word", "")
        source = arguments.get("source_sentence", "")
        notes = arguments.get("notes", "")
        if db.add_vocab(word, source, notes):
            return [types.TextContent(type="text", text=f"已添加单词: {word}")]
        return [types.TextContent(type="text", text=f"添加失败（可能已存在）: {word}")]

    elif name == "list_vocab":
        learned = arguments.get("learned")
        keyword = arguments.get("keyword", "")
        limit = arguments.get("limit", 50)
        words = db.list_vocab(learned, keyword, limit)
        if not words:
            return [types.TextContent(type="text", text="生词本为空")]
        lines = []
        for w in words:
            status = "✅" if w["learned"] else "📖"
            lines.append(f"{status} #{w['id']} **{w['word']}**")
            if w["source_sentence"]:
                lines.append(f"   → {w['source_sentence']}")
            lines.append(f"   {w['added_at']}")
        return [types.TextContent(type="text", text="\n".join(lines))]

    elif name == "search_vocab":
        keyword = arguments.get("keyword", "")
        words = db.list_vocab(keyword=keyword)
        if not words:
            return [types.TextContent(type="text", text=f"未找到包含「{keyword}」的单词")]
        lines = []
        for w in words:
            status = "✅" if w["learned"] else "📖"
            lines.append(f"{status} #{w['id']} **{w['word']}**")
            if w["source_sentence"]:
                lines.append(f"   → {w['source_sentence']}")
        return [types.TextContent(type="text", text="\n".join(lines))]

    elif name == "mark_learned":
        word_id = arguments.get("word_id", 0)
        learned = arguments.get("learned", True)
        if db.mark_learned(word_id, learned):
            status = "已掌握" if learned else "学习中"
            return [types.TextContent(type="text", text=f"已将 #{word_id} 标记为{status}")]
        return [types.TextContent(type="text", text="标记失败")]

    elif name == "delete_vocab":
        word_id = arguments.get("word_id", 0)
        if db.delete_vocab(word_id):
            return [types.TextContent(type="text", text=f"已删除 #{word_id}")]
        return [types.TextContent(type="text", text="删除失败")]

    elif name == "get_history":
        limit = arguments.get("limit", 20)
        keyword = arguments.get("keyword", "")
        records = db.list_history(limit, keyword)
        if not records:
            return [types.TextContent(type="text", text="暂无朗读历史")]
        lines = []
        for r in records:
            lines.append(f"🕐 {r['read_at']} [{r['engine_used']}]")
            lines.append(f"   {r['text'][:100]}")
            lines.append("")
        return [types.TextContent(type="text", text="\n".join(lines))]

    else:
        raise ValueError(f"未知工具: {name}")


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="point-reader",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
