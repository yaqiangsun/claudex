# 05 - 查询循环

对应 TypeScript: `src/query.ts`

## 5.1 查询循环核心

```python
# pyclaude/core/query.py
from typing import AsyncIterator, Optional
import json
from pyclaude.services.api import APIClient
from pyclaude.tools.registry import ToolRegistry
from pyclaude.engine import QueryEngineConfig


class QueryLoop:
    """查询循环 - 处理与 Claude API 的交互"""

    def __init__(
        self,
        api_client: APIClient,
        tool_registry: ToolRegistry,
        config: QueryEngineConfig,
    ):
        self.api_client = api_client
        self.tool_registry = tool_registry
        self.config = config

    async def execute(
        self,
        messages: list[dict],
        tools: list[dict],
        session_id: Optional[str] = None,
    ) -> AsyncIterator[dict]:
        """执行查询循环，返回流式响应"""

        # 1. 构建请求
        request = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "messages": messages,
            "system": self.config.system_prompt,
        }

        if tools:
            request["tools"] = tools

        # 2. 发送请求并处理流
        async for chunk in self.api_client.stream(request):
            yield chunk

    async def execute_with_tools(
        self,
        messages: list[dict],
        tools: list[dict],
    ) -> tuple[list[dict], list[dict]]:
        """执行一次查询，处理工具调用，返回消息和工具结果"""

        # 1. 发送请求
        response = await self.api_client.chat.completions.create(**{
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "messages": messages,
            "tools": tools,
            "stream": False,
        })

        # 2. 提取响应内容
        content_blocks = []
        tool_uses = []

        for block in response.content:
            if block.type == "text":
                content_blocks.append({
                    "type": "content_block",
                    "text": block.text,
                })
            elif block.type == "tool_use":
                tool_uses.append({
                    "type": "tool_use",
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                })

        # 3. 执行工具调用
        tool_results = []
        for tool_use in tool_uses:
            result = await self._execute_tool(tool_use)
            tool_results.append(result)

        # 4. 构建最终消息
        assistant_message = {
            "role": "assistant",
            "content": content_blocks,
        }
        if tool_uses:
            assistant_message["tool_calls"] = tool_uses

        user_messages = [
            {"role": "tool", "tool_call_id": r["tool_id"], "content": r["content"]}
            for r in tool_results
        ]

        return assistant_message, user_messages

    async def _execute_tool(self, tool_use: dict) -> dict:
        """执行单个工具调用"""
        tool_name = tool_use["name"]
        tool_input = tool_use["input"]
        tool_id = tool_use["id"]

        tool = self.tool_registry.get(tool_name)
        if not tool:
            return {
                "tool_id": tool_id,
                "content": f"Tool not found: {tool_name}",
                "is_error": True,
            }

        try:
            result = await tool.execute(tool_input)
            return {
                "tool_id": tool_id,
                "content": json.dumps(result),
                "is_error": False,
            }
        except Exception as e:
            return {
                "tool_id": tool_id,
                "content": str(e),
                "is_error": True,
            }
```

## 5.2 API 客户端

对应 TypeScript: `src/services/api/`

```python
# pyclaude/services/api.py
from typing import AsyncIterator, Optional
import httpx
from pydantic import BaseModel


class Message(BaseModel):
    """消息模型"""
    role: str
    content: str


class ToolUse(BaseModel):
    """工具调用"""
    id: str
    name: str
    input: dict


class ContentBlock(BaseModel):
    """内容块"""
    type: str
    text: Optional[str] = None
    tool_use: Optional[ToolUse] = None


class CompletionRequest(BaseModel):
    """完成请求"""
    model: str
    messages: list[Message]
    max_tokens: int = 8192
    system: Optional[str] = None
    tools: Optional[list[dict]] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None


class APIClient:
    """API 客户端"""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.anthropic.com",
        max_retries: int = 3,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.max_retries = max_retries
        self.client = httpx.AsyncClient(
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            timeout=httpx.Timeout(60.0, connect=10.0),
        )

    async def stream(
        self,
        request: dict,
    ) -> AsyncIterator[dict]:
        """流式请求"""
        async with self.client.stream(
            "POST",
            f"{self.base_url}/v1/messages",
            json=request,
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    yield json.loads(data)

    async def create_completion(
        self,
        request: dict,
    ) -> dict:
        """同步请求"""
        response = await self.client.post(
            f"{self.base_url}/v1/messages",
            json=request,
        )
        response.raise_for_status()
        return response.json()

    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
```

## 5.3 上下文压缩

对应 TypeScript: `src/services/compact/`

```python
# pyclaude/services/compact.py
from typing import Optional
from pyclaude.services.api import APIClient


class ContextCompactor:
    """上下文压缩器"""

    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    async def compress(
        self,
        messages: list[dict],
        max_tokens: int = 100000,
    ) -> list[dict]:
        """压缩消息列表"""

        # 1. 计算当前 token 数
        current_tokens = self._estimate_tokens(messages)
        if current_tokens <= max_tokens:
            return messages

        # 2. 保留系统提示和最近的消息
        system_message = None
        if messages and messages[0].get("role") == "system":
            system_message = messages[0]
            messages = messages[1:]

        # 3. 计算需要保留的消息数
        target_messages = messages[-50:]  # 保留最近 50 条

        # 4. 如果还是太大，调用 AI 总结
        if self._estimate_tokens(target_messages) > max_tokens:
            target_messages = await self._summarize(messages[:-50])

        # 5. 重组消息
        result = []
        if system_message:
            result.append(system_message)
        result.extend(target_messages)

        return result

    async def _summarize(self, old_messages: list[dict]) -> list[dict]:
        """使用 AI 总结旧消息"""
        summary_prompt = {
            "role": "user",
            "content": f"""请总结以下对话的要点，保留关键信息和上下文：

{self._format_messages(old_messages)}

请提供一个简洁的总结，包括：
1. 主要讨论的话题
2. 做出的决定
3. 未完成的任务
4. 重要的上下文信息"""
        }

        response = await self.api_client.create_completion({
            "model": "claude-sonnet-4-20250514",
            "messages": [summary_prompt],
            "max_tokens": 2000,
        })

        summary = response["content"][0]["text"]

        return [{
            "role": "system",
            "content": f"[对话摘要]\n{summary}"
        }]

    def _estimate_tokens(self, messages: list[dict]) -> int:
        """估算 token 数量"""
        total = 0
        for msg in messages:
            content = msg.get("content", "")
            # 简单估算: ~4 字符 = 1 token
            total += len(content) // 4
        return total

    def _format_messages(self, messages: list[dict]) -> str:
        """格式化消息"""
        return "\n".join([
            f"{msg.get('role')}: {msg.get('content', '')}"
            for msg in messages
        ])
```

## 5.4 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `query.ts` | `class QueryLoop` | `pyclaude/core/query.py` |
| `APIClient` | `class APIClient` | `pyclaude/services/api.py` |
| `ContextCompactor` | `class ContextCompactor` | `pyclaude/services/compact.py` |