"""Voyage AI client for embedding generation."""

import logging
from typing import List, Optional

import voyageai

from prompt_saver_mcp.config import config

logger = logging.getLogger(__name__)


class VoyageClient:
    """Voyage AI client for generating embeddings."""

    def __init__(self):
        """Initialize Voyage AI client."""
        if not config.VOYAGE_AI_API_KEY:
            raise ValueError("VOYAGE_AI_API_KEY is required")
        self.client = voyageai.Client(api_key=config.VOYAGE_AI_API_KEY)
        self.model = config.VOYAGE_AI_EMBEDDING_MODEL

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to generate embedding for

        Returns:
            List of floats representing the embedding vector
        """
        try:
            result = self.client.embed([text], model=self.model)
            if result.embeddings and len(result.embeddings) > 0:
                return result.embeddings[0]
            raise ValueError("No embedding generated")
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.

        Args:
            texts: List of texts to generate embeddings for

        Returns:
            List of embedding vectors
        """
        try:
            if not texts:
                return []
            result = self.client.embed(texts, model=self.model)
            if result.embeddings:
                return result.embeddings
            raise ValueError("No embeddings generated")
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise


# Global Voyage client instance (lazy initialization)
_voyage_client: Optional[VoyageClient] = None


def get_voyage_client() -> VoyageClient:
    """Get or create the global Voyage client instance."""
    global _voyage_client
    if _voyage_client is None:
        _voyage_client = VoyageClient()
    return _voyage_client


# Create a simple object that delegates to get_voyage_client()
class VoyageClientProxy:
    """Proxy for lazy-loaded Voyage client."""

    def __getattr__(self, name):
        return getattr(get_voyage_client(), name)


voyage_client = VoyageClientProxy()

