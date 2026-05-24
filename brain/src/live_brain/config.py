"""Runtime configuration — secrets from env / bw-env only."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_PKG_DIR = Path(__file__).parent
_CONFIG_YAML = _PKG_DIR / "config.yaml"


@lru_cache
def _yaml_defaults() -> dict:
    if not _CONFIG_YAML.is_file():
        return {}
    with _CONFIG_YAML.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    http_host: str = Field(default="0.0.0.0", alias="HTTP_HOST")
    http_port: int = Field(default=8000, alias="HTTP_PORT")
    mistral_api_key: str | None = Field(default=None, alias="MISTRAL_API_KEY")
    mistral_base_url: str = Field(default="https://api.mistral.ai/v1")
    mistral_model: str = Field(default="mistral-small-latest")
    redis_url: str = Field(default="redis://127.0.0.1:6379/0", alias="REDIS_URL")
    public_base_url: str = Field(default="https://live.kpihx-labs.com", alias="PUBLIC_BASE_URL")

    @classmethod
    def load(cls) -> Settings:
        defaults = _yaml_defaults()
        http = defaults.get("http") or {}
        mistral = defaults.get("mistral") or {}
        redis = defaults.get("redis") or {}
        return cls(
            http_host=http.get("host", "0.0.0.0"),
            http_port=int(http.get("port", 8000)),
            mistral_base_url=mistral.get("base_url", "https://api.mistral.ai/v1"),
            mistral_model=mistral.get("model", "mistral-small-latest"),
            redis_url=redis.get("url", "redis://127.0.0.1:6379/0"),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.load()
