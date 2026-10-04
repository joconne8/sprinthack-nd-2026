"""Application settings loaded from environment variables."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the sample agent."""

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

    http_host: str = "0.0.0.0"
    http_port: int = 8000

    litellm_proxy_api_base: str = "http://localhost:4000"
    litellm_proxy_api_key: str = ""
    agent_model: str = "litellm_proxy/openai/gpt-4.1-mini"
    agent_temperature: float = 0.2

    warehouse_dsn: str = ""

    microsoft_tenant_id: str = ""
    microsoft_client_id: str = ""
    microsoft_client_secret: str = ""
    teams_team_id: str = ""
    teams_channel_id: str = ""

    copilot_studio_webhook_url: str = ""
    copilot_studio_api_key: str = ""

    powerbi_image_export_url: str = ""
    powerbi_report_web_url: str = ""
    powerbi_bearer_token: str = ""
    powerbi_report_name: str = "Goodwill Michiana Operations Dashboard"

    mcp_server_command: str = ""
    mcp_server_args: str = "[]"
    mcp_server_env: str = "{}"
