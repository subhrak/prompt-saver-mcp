"""Configuration management for the MCP server."""

import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for environment variables."""

    # MongoDB Configuration
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "prompt_saver")
    MONGODB_COLLECTION: str = os.getenv("MONGODB_COLLECTION", "prompts")

    # Voyage AI Configuration
    VOYAGE_AI_API_KEY: Optional[str] = os.getenv("VOYAGE_AI_API_KEY")
    VOYAGE_AI_EMBEDDING_MODEL: str = os.getenv("VOYAGE_AI_EMBEDDING_MODEL", "voyage-3-large")

    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    @classmethod
    def validate(cls) -> None:
        """Validate that required configuration is present."""
        if not cls.MONGODB_URI:
            raise ValueError("MONGODB_URI environment variable is required")
        if not cls.VOYAGE_AI_API_KEY:
            raise ValueError("VOYAGE_AI_API_KEY environment variable is required")
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")


# Global config instance
config = Config()

