# AIAgent On Line

**簡介**

AIAgent On Line 是一套能夠透過 **LINE Bot 集成** 進行實時 AI Agent 推論，整合 MCP（Model Context Protocol) 工具，支援多種工具與外部服務整合（Google Geoencoding API、Google Sheets、Sequential Thinking），採用 **LangChain 框架** 進行 Agent 編排、MCP 標準工具對接與 FastAPI 非同步服務。

## 核心功能與技術要點

- **多源 AI Agent 推論**：整合 OpenAI/Azure AI 模型，透過 LangChain 進行 Agentic 邏輯編排，支援複雜的決策鏈與工具調用。

- **MCP 工具標準化**：使用 `Model Context Protocol` 標準化工具接口，實現 Geoencoding、Google Sheets 等外部服務的無縫對接，降低耦合性。

- **Line Bot 實時互動**：整合 LINE Bot SDK，透過 WebhookHandler 即時接收與回應使用者訊息，支援多輪對話與上下文管理。

- **非同步串流架構**：使用 FastAPI `async` 與 `asynccontextmanager`，實現高效能的並發請求處理與流式回應（streaming）。

## 簡要工作流程（How it Works）

1. 使用者透過 LINE Bot 發送訊息
2. FastAPI Webhook Endpoint 接收訊息並驗證簽名
3. Agent 接受訊息並執行推論邏輯
4. Agent 可根據需要調用 MCP 工具（地理編碼、Google Sheets 查詢等）
5. 模型整合工具結果進行思考與決策
6. 最終結果透過 LINE Bot 回傳給使用者

## 快速開始（Code-Centric）

### 1. 環境準備

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

或直接使用：

```bash
pip install fastapi uvicorn langchain langchain-openai azure-ai-projects mcp line-bot-sdk python-dotenv
```

### 2. 環境變數設定

在專案根目錄建立 `.env` 檔案，設定以下變數：

```env
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
LINE_CHANNEL_SECRET=your_channel_secret
OPENAI_API_KEY=your_openai_api_key
# 或使用 Azure AI
AZURE_AI_PROJECT_CONNECTION_STRING=your_connection_string
```

### 3. 啟動 MCP Server（選用）

如需使用 Geoencoding 工具，先啟動 MCP Server：

```bash
python src/aiagent_on_line/mcp_server.py
```

### 4. 啟動 FastAPI 應用

**Windows (cmd):**

```cmd
python src\aiagent_on_line\main.py
```

**或使用 `uvicorn`：**

```bash
uvicorn src.aiagent_on_line.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. 連接 LINE Bot Webhook

將 FastAPI 應用的公開 URL（例如透過 ngrok）設定到 LINE Bot 開發者控制台的 Webhook URL，格式為：

```
https://your-domain/callback
```

## 關鍵檔案（快速連結）

- [src/aiagent_on_line/main.py](src/aiagent_on_line/main.py) - FastAPI 應用主程式，LINE Bot Webhook 處理與消息路由。
- [src/aiagent_on_line/main_async.py](src/aiagent_on_line/main_async.py) - 非同步版本主程式。
- [src/aiagent_on_line/nodes/agent0.py](src/aiagent_on_line/nodes/agent0.py) - AI Agent 核心邏輯，包含工具調用與推論流程。
- [src/aiagent_on_line/nodes/agent_with_mcp_tools.py](src/aiagent_on_line/nodes/agent_with_mcp_tools.py) - 集成 MCP 工具的 Agent 實現。
- [src/aiagent_on_line/tools/geoencoding.py](src/aiagent_on_line/tools/geoencoding.py) - 地理編碼工具，支援地址轉坐標。
- [src/aiagent_on_line/tools/gspread.py](src/aiagent_on_line/tools/gspread.py) - Google Sheets 整合工具，支援資料查詢與更新。
- [src/aiagent_on_line/mcp_server.py](src/aiagent_on_line/mcp_server.py) - MCP Server 實現，標準化工具接口。
- [mcp_servers/sequentialthinking/](mcp_servers/sequentialthinking/) - Sequential Thinking MCP Server 實現，支援複雜推理流程。

---

# AIAgent On Line

**Introduction**

AIAgent On Line is a system capable of performing real-time AI Agent inference through **LINE Bot integration** integrating MCP (Model Context Protocol) tools, and supporting multiple tool integrations and external services (Google Geoencoding API, Google Sheets, Sequential Thinking). It leverages the **LangChain framework** for Agent orchestration, MCP standard tool interfaces, and FastAPI asynchronous services.

## Core Features & Technical Highlights

- **Multi-source AI Agent Inference**: Integrates OpenAI/Azure AI models with LangChain for Agentic logic orchestration, supporting complex decision chains and tool invocation.

- **MCP Tool Standardization**: Uses the `Model Context Protocol` standard to normalize tool interfaces, enabling seamless integration of external services like Geoencoding and Google Sheets while reducing coupling.

- **LINE Bot Real-time Interaction**: Integrates LINE Bot SDK with WebhookHandler for instant message reception and response, supporting multi-turn conversations and context management.

- **Asynchronous Streaming Architecture**: Employs FastAPI's `async` and `asynccontextmanager` for efficient concurrent request handling and streaming responses.

## Workflow (How It Works)

1. **User Input**: User sends a message via LINE Bot.
2. **Webhook Reception**: FastAPI Webhook Endpoint receives the message and verifies the signature.
3. **Agent Processing**: Agent receives the message and executes inference logic.
4. **Tool Invocation**: Agent may invoke MCP tools as needed (geoencoding queries, Google Sheets lookups, etc.).
5. **Reasoning**: Model integrates tool results for thinking and decision-making.
6. **Response**: Final result is returned to the user via LINE Bot.

## Quick Start (Code-Centric)

### 1. Environment Setup

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Or directly install:

```bash
pip install fastapi uvicorn langchain langchain-openai azure-ai-projects mcp line-bot-sdk python-dotenv
```

### 2. Environment Variables Configuration

Create a `.env` file in the project root with the following variables:

```env
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
LINE_CHANNEL_SECRET=your_channel_secret
OPENAI_API_KEY=your_openai_api_key
# Or use Azure AI
AZURE_AI_PROJECT_CONNECTION_STRING=your_connection_string
```

### 3. Start MCP Server (Optional)

If using the Geoencoding tool, start the MCP Server first:

```bash
python src/aiagent_on_line/mcp_server.py
```

### 4. Start FastAPI Application

**Windows (cmd):**

```cmd
python src\aiagent_on_line\main.py
```

**Or using `uvicorn`:**

```bash
uvicorn src.aiagent_on_line.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Configure LINE Bot Webhook

Set the public URL of your FastAPI application (e.g., via ngrok) in the LINE Bot Developer Console's Webhook URL setting, formatted as:

```
https://your-domain/callback
```

## Key Files (Quick Links)

- [src/aiagent_on_line/main.py](src/aiagent_on_line/main.py) - FastAPI main application handling LINE Bot Webhook and message routing.
- [src/aiagent_on_line/main_async.py](src/aiagent_on_line/main_async.py) - Asynchronous version of the main application.
- [src/aiagent_on_line/nodes/agent0.py](src/aiagent_on_line/nodes/agent0.py) - Core AI Agent logic including tool invocation and inference workflows.
- [src/aiagent_on_line/nodes/agent_with_mcp_tools.py](src/aiagent_on_line/nodes/agent_with_mcp_tools.py) - Agent implementation with integrated MCP tools.
- [src/aiagent_on_line/tools/geoencoding.py](src/aiagent_on_line/tools/geoencoding.py) - Geoencoding tool supporting address-to-coordinates conversion.
- [src/aiagent_on_line/tools/gspread.py](src/aiagent_on_line/tools/gspread.py) - Google Sheets integration tool supporting data querying and updates.
- [src/aiagent_on_line/mcp_server.py](src/aiagent_on_line/mcp_server.py) - MCP Server implementation with standardized tool interfaces.
- [mcp_servers/sequentialthinking/](mcp_servers/sequentialthinking/) - Sequential Thinking MCP Server implementation supporting complex reasoning workflows.
