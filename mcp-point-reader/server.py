"""MCP Point Reader Server - 通过 MCP 协议向 AI 助手暴露点读助手功能。"""

import asyncio
from mcp_point_reader import tools


def main():
    """启动 MCP 服务器（同步入口，供 `uv run` 或 `python` 直接调用）。"""
    asyncio.run(tools.main())


if __name__ == "__main__":
    main()
