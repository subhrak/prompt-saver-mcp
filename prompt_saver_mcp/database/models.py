"""Data models for prompt storage."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Prompt(BaseModel):
    """Prompt model for MongoDB storage."""

    use_case: str = Field(
        ...,
        description="Category of the prompt: code-gen, text-gen, data-analysis, creative, general",
    )
    summary: str = Field(..., description="Summary of the prompt and its use case")
    prompt_template: str = Field(..., description="Universal problem-solving prompt template")
    history: str = Field(..., description="Summary of steps taken and end result")
    embedding: Optional[List[float]] = Field(
        None, description="Vector embeddings of the summary (2048 dimensions)"
    )
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    num_updates: int = Field(default=0, description="Number of times this prompt has been updated")
    changelog: List[str] = Field(default_factory=list, description="List of changes made to this prompt")
    created_by: Optional[str] = Field(None, description="Creator identifier for team sharing")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "use_case": "code-gen",
                "summary": "Python CSV parser with error handling",
                "prompt_template": "# Task\n\nCreate a Python function...",
                "history": "Created parser function with error handling...",
                "embedding": [0.1, 0.2, ...],
                "last_updated": "2025-01-01T00:00:00Z",
                "num_updates": 0,
                "changelog": [],
                "created_by": "user123",
            }
        }


class PromptCreate(BaseModel):
    """Model for creating a new prompt."""

    use_case: str
    summary: str
    prompt_template: str
    history: str
    embedding: Optional[List[float]] = None
    created_by: Optional[str] = None


class PromptUpdate(BaseModel):
    """Model for updating an existing prompt."""

    use_case: Optional[str] = None
    summary: Optional[str] = None
    prompt_template: Optional[str] = None
    history: Optional[str] = None
    embedding: Optional[List[float]] = None
    changelog_entry: Optional[str] = None

