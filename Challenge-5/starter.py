"""
Challenge 5 (Innovate): Build Your Own MCP-Powered Agent

AGENT: The Automated Researcher
  
  A personal research assistant that searches the web for any topic you 
  want to learn about and automatically saves neatly formatted Markdown 
  notes to your local `research_notes/` folder.

  Give it a topic, and it will:
  1. Search the web using the DuckDuckGo MCP server (FREE, no API key!).
  2. Summarize the best findings into a structured study guide.
  3. Save the guide as a Markdown file using the Filesystem MCP server.

RULES SATISFIED:
  Uses Strands Agents SDK
  Uses two MCP servers (DuckDuckGo Search + Filesystem)
  Uses Amazon Nova Pro on Amazon Bedrock
  Has an interactive chat loop
  Is an original, creative idea
  BONUS: Multiple MCP servers simultaneously

SETUP:
  1. Install Node.js (required for npx to run the MCP servers): https://nodejs.org/
  2. Run this script: python starter.py
  (No API keys required!)
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from pathlib import Path
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import StdioServerParameters, stdio_client


# ─────────────────────────── Configuration ───────────────────────────────────

MODEL = "us.amazon.nova-pro-v1:0"
NOTES_DIR = Path(__file__).parent / "research_notes"
NOTES_DIR_STR = str(NOTES_DIR.resolve()).replace("\\", "/")

SYSTEM_PROMPT = f"""You are The Automated Researcher, a research assistant.

Help users learn about topics by:
1. Search the web using web-search tool.
2. Synthesize information into a structured summary.
3. Save the summary as a Markdown file using write_file tool.

When saving notes, save files to: {NOTES_DIR_STR}
Use kebab-case filenames like "topic-name.md".
Format with title, sections, bullet points, and a Sources section.
After saving, confirm the filename."""


# ─────────────────────────── Startup Checks ──────────────────────────────────

def check_prerequisites():
    """Create the notes directory if it doesn't exist."""
    NOTES_DIR.mkdir(exist_ok=True)
    print(f"[DIR] Research notes will be saved to: {NOTES_DIR.resolve()}")


# ─────────────────────────── Main Application ────────────────────────────────

def main():
    print("=" * 60)
    print("   [*] The Automated Researcher -- Powered by AI")
    print("=" * 60)
    print("  I search the web, synthesize knowledge, and save")
    print("  beautiful Markdown study guides to your local files.")
    print("  Type 'quit' or 'exit' to stop.\n")

    check_prerequisites()

    # --- MCP Server 1: DuckDuckGo Search (free, no API key required!) ---
    ddg_mcp = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(
                command="npx",
                args=["-y", "@oevortex/ddg_search@1.2.2"],
            )
        )
    )

    # --- MCP Server 2: Filesystem (for saving markdown notes) ---
    filesystem_mcp = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(
                command="npx",
                args=[
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    str(NOTES_DIR.resolve()),  # Restrict access to notes dir only
                ],
            )
        )
    )

    # --- Start both MCP clients and combine their tools ---
    print("[...] Connecting to MCP servers (DuckDuckGo Search + Filesystem)...")
    with ddg_mcp, filesystem_mcp:
        search_tools  = ddg_mcp.list_tools_sync()
        all_fs_tools  = filesystem_mcp.list_tools_sync()

        # Keep only essential filesystem tools (write, read, mkdir)
        ESSENTIAL_FS_TOOLS = {"write_file", "create_directory", "read_file"}
        filesystem_tools = [t for t in all_fs_tools if t.tool_name in ESSENTIAL_FS_TOOLS]

        all_tools = search_tools + filesystem_tools
        print(f"[OK]  Connected! {len(all_tools)} tools available.\n")

        # --- Initialize the Strands Agent ---
        agent = Agent(
            model=MODEL,
            tools=all_tools,
            system_prompt=SYSTEM_PROMPT,
        )

        # --- Interactive Chat Loop ---
        print('[TIP] Try: "Research quantum computing for beginners and save notes."')
        print("-" * 60)

        while True:
            try:
                user_input = input("\nYou: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\nGoodbye! Your notes are saved in:", NOTES_DIR.resolve())
                break

            if not user_input:
                continue

            if user_input.lower() in ("quit", "exit", "q"):
                print("\nGoodbye! Your notes are saved in:", NOTES_DIR.resolve())
                break

            try:
                response = agent(user_input)
                print(f"\nResearcher: {response}")
            except Exception as e:
                print(f"\n[ERROR] Agent call failed: {e}")
                print("[INFO]  Please try again or rephrase your query.\n")


if __name__ == "__main__":
    main()
