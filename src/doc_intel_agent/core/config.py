from enum import Enum
from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    LOCAL = "local"
    TEST = "test"
    PRODUCTION = "production"


class FrozenModel(BaseModel):
    """Base class for nested settings groups so they inherit immutability
    instead of each needing model_config repeated."""

    model_config = ConfigDict(frozen=True)


class QdrantSettings(FrozenModel):
    url: str = "http://localhost:6333"
    collection_text: str = "doc_chunks_text"
    collection_image: str = "doc_chunks_image"


class HuggingFaceSettings(FrozenModel):
    token: SecretStr = SecretStr("")


class LLMProviderSettings(FrozenModel):
    anthropic_api_key: SecretStr = SecretStr("")
    openai_api_key: SecretStr = SecretStr("")


class SecEdgarSettings(FrozenModel):
    user_agent: str = "doc-intel-agent contact@example.com"


class APISettings(FrozenModel):
    host: str = "0.0.0.0"
    port: int = 8000


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
        frozen=True,
    )

    environment: Environment = Environment.LOCAL
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    json_logs: bool = False

    qdrant: QdrantSettings = Field(default_factory=QdrantSettings)
    huggingface: HuggingFaceSettings = Field(default_factory=HuggingFaceSettings)
    llm: LLMProviderSettings = Field(default_factory=LLMProviderSettings)
    sec_edgar: SecEdgarSettings = Field(default_factory=SecEdgarSettings)
    api: APISettings = Field(default_factory=APISettings)

    @property
    def is_production(self) -> bool:
        return self.environment is Environment.PRODUCTION


@lru_cache
def get_settings() -> Settings:
    return Settings()