# Goodwill Michiana Copilot Intelligence Agent

A hackathon-ready skeleton for a Goodwill Michiana operating intelligence agent. It is based on the generic `SAMPLE` LangGraph codebase, with the connectors and tool surfaces reshaped around Microsoft Teams, Copilot Studio, Power BI, and nonprofit workforce/retail operations.

This repository intentionally contains no real credentials, tenant IDs, report IDs, Teams IDs, donor records, participant data, or private Goodwill information.

## Use Case

The agent is designed as a baseline for demos where a Teams or Copilot user asks questions such as:

- "How are stores performing today?"
- "Show me the Power BI retail operations dashboard."
- "What workforce program metrics need attention?"
- "Draft a Teams update for store managers."
- "Escalate this summary into Copilot Studio for follow-up."

## What Is Included

- LangGraph ReAct-style agent with tool calling
- FastAPI endpoint for invoking the agent from a bot, workflow, or demo UI
- Goodwill-oriented demo metrics for stores, donations, workforce programs, and incidents
- Microsoft Graph connector pattern for Teams channel messages and thread context
- Copilot Studio webhook handoff connector
- Power BI screenshot connector with REST image and Playwright browser modes
- Generic MCP stdio connector for hackathon extensions
- Side-channel screenshot/image collection so images are returned by the API without stuffing base64 into the LLM context

## Quick Start

```powershell
cd GOODWILL_MICHIANA_SAMPLE
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
copy .env.example .env
python -m sample_agent --reload
```

Invoke the local API:

```powershell
curl -X POST http://localhost:8000/agents/intelligence-agent/invoke `
  -H "Content-Type: application/json" `
  -d "{\"message\":\"Show me the Power BI store operations dashboard and summarize risks\"}"
```

## Microsoft Integration Points

Configure these only when connecting to real services:

- `MICROSOFT_TENANT_ID`
- `MICROSOFT_CLIENT_ID`
- `MICROSOFT_CLIENT_SECRET`
- `TEAMS_TEAM_ID`
- `TEAMS_CHANNEL_ID`
- `COPILOT_STUDIO_WEBHOOK_URL`
- `POWERBI_REPORT_WEB_URL`
- `POWERBI_IMAGE_EXPORT_URL`
- `POWERBI_BEARER_TOKEN`

For a hackathon, you can leave them blank. The agent will use deterministic demo data and placeholder screenshots.

## Project Layout

```text
sample_agent/
  agents/
    intelligence_agent/
      agent.py                  LangGraph builder
      prompt.py                 Goodwill Michiana-oriented system prompt
      tools/
        query_metrics.py        Goodwill demo metrics
        powerbi_snapshot.py     Power BI screenshot tool
        teams_message.py        Teams draft/send tool
        copilot_handoff.py      Copilot Studio handoff tool
        mcp_tool.py             Generic MCP tool bridge
  connectors/
    microsoft_graph.py          Teams/Graph helper
    copilot_studio.py           Copilot handoff webhook helper
    powerbi_connector.py        Power BI screenshot helper
    warehouse.py                SQL or demo metric source
```

## Demo Architecture

Teams or Copilot asks a question, FastAPI invokes the LangGraph agent, tools fetch metrics or screenshots, and the response returns both text and image artifacts. A production deployment can replace demo connectors one at a time without changing the agent loop.
