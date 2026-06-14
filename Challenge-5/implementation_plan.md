# Automated Researcher Agent

This agent acts as a personal research assistant. It takes a topic, searches the web for relevant information, summarizes the findings, and automatically saves those notes into a designated folder on your local filesystem.

## Goal
Build an MCP-powered agent in `starter.py` that uses:
1. **DuckDuckGo Search MCP** (`@oevortex/ddg_search`) to search the web — **free, no API key required**.
2. **Filesystem MCP** (`@modelcontextprotocol/server-filesystem`) to create and write markdown files with the research notes.

## Implementation Details

### Architecture
- **Model**: Amazon Nova Pro (`us.amazon.nova-pro-v1:0`) — plain model string (same as Challenge 2), compatible with limited IAM profiles.
- **Tool Consent**: `BYPASS_TOOL_CONSENT = "true"` — same pattern as Challenge 2 for seamless tool execution.
- **MCP Server 1 — DuckDuckGo Search**: Runs via `npx -y @oevortex/ddg_search@1.2.2`. Provides web search capability with zero configuration.
- **MCP Server 2 — Filesystem**: Runs via `npx -y @modelcontextprotocol/server-filesystem`, restricted to the `research_notes/` directory for safe sandboxed file access. Only essential tools (`write_file`, `read_file`, `create_directory`) are exposed.
- **Interactive Chat Loop**: A `while True` input loop allows conversational interaction. Type `quit`, `exit`, or `q` to stop.

## Proposed Changes

### Challenge-5 Workspace

#### [MODIFY] [starter.py](file:///c:/Devopam/Engineering_CSE/SEM-4/VSC-CODING/GRIND/builders-skill-sprint-challenges/Challenge-5/starter.py)
✅ **COMPLETED** — The complete agent is implemented in this file. The code:
- Connects to the DuckDuckGo Search MCP server via `npx` (no API key needed).
- Connects to the Filesystem MCP server via `npx`, restricted to the `research_notes/` directory.
- Combines the tools from both servers (filtering filesystem tools to essentials only).
- Initializes the `Agent` from the Strands SDK with `BedrockModel` for `us.amazon.nova-pro-v1:0`.
- Runs a `while True` interactive chat loop in the terminal.

#### [NEW] [research_notes/](file:///c:/Devopam/Engineering_CSE/SEM-4/VSC-CODING/GRIND/builders-skill-sprint-challenges/Challenge-5/research_notes/)
✅ **COMPLETED** — This directory exists as the safe sandbox for the Filesystem MCP to save markdown notes.

## Setup & Usage

### Prerequisites
- **Python 3.10+** with `strands-agents` and `strands-agents-tools` installed.
- **Node.js** (required for `npx` to run the MCP servers): [https://nodejs.org/](https://nodejs.org/)
- **AWS credentials** configured for Amazon Bedrock access.
- **No additional API keys required!**

### Running
```bash
cd Challenge-5
python starter.py
```

### Example Prompts
- *"Research quantum computing for beginners and save notes."*
- *"Can you research the history of the Model Context Protocol and save a summary as mcp_history.md?"*
- *"What are the latest trends in AI agents? Save a summary."*

## Verification Plan

### Manual Verification
1. ✅ Code is written to `starter.py`.
2. Run `python starter.py` from the `Challenge-5` directory.
3. Ask the agent: *"Research quantum computing for beginners and save notes."*
4. The agent should search the web, generate a structured summary, and save a file into `research_notes/`.
5. Verify the markdown file was created and is well-formatted.

## Rules Satisfied
| Rule | Status |
|------|--------|
| Uses **Strands Agents SDK** | ✅ |
| Uses **at least one MCP server** | ✅ (Two: DuckDuckGo + Filesystem) |
| Uses **Amazon Nova Pro** (Bedrock model) | ✅ |
| Has an **interactive chat loop** | ✅ |
| Is an **original, creative idea** | ✅ |
| **BONUS**: Multiple MCP servers | ✅ |
