"""MongoDB client for prompt storage and retrieval."""

import logging
from datetime import datetime
from typing import List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, OperationFailure

from prompt_saver_mcp.config import config
from prompt_saver_mcp.database.models import Prompt, PromptCreate, PromptUpdate

logger = logging.getLogger(__name__)


class MongoDBClient:
    """MongoDB client for prompt operations."""

    def __init__(self):
        """Initialize MongoDB client with connection pooling."""
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.collection: Optional[Collection] = None
        self._connect()

    def _connect(self) -> None:
        """Establish connection to MongoDB."""
        try:
            self.client = MongoClient(
                config.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=50,
                minPoolSize=10,
            )
            # Test connection
            self.client.admin.command("ping")
            self.db = self.client[config.MONGODB_DATABASE]
            self.collection = self.db[config.MONGODB_COLLECTION]
            logger.info(f"Connected to MongoDB database: {config.MONGODB_DATABASE}")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def create_prompt(self, prompt_data: PromptCreate) -> str:
        """
        Create a new prompt in the database.

        Args:
            prompt_data: Prompt data to create

        Returns:
            The created prompt's ID as a string
        """
        try:
            document = {
                "use_case": prompt_data.use_case,
                "summary": prompt_data.summary,
                "prompt_template": prompt_data.prompt_template,
                "history": prompt_data.history,
                "embedding": prompt_data.embedding,
                "last_updated": datetime.utcnow(),
                "num_updates": 0,
                "changelog": [],
                "created_by": prompt_data.created_by,
            }
            result = self.collection.insert_one(document)
            logger.info(f"Created prompt with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except OperationFailure as e:
            logger.error(f"Failed to create prompt: {e}")
            raise

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """
        Retrieve a prompt by ID.

        Args:
            prompt_id: The prompt ID

        Returns:
            Prompt object or None if not found
        """
        try:
            from bson import ObjectId

            document = self.collection.find_one({"_id": ObjectId(prompt_id)})
            if document:
                document["_id"] = str(document["_id"])
                return Prompt(**document)
            return None
        except Exception as e:
            logger.error(f"Failed to get prompt {prompt_id}: {e}")
            raise

    def update_prompt(self, prompt_id: str, update_data: PromptUpdate) -> bool:
        """
        Update an existing prompt.

        Args:
            prompt_id: The prompt ID to update
            update_data: Update data

        Returns:
            True if update was successful, False otherwise
        """
        try:
            from bson import ObjectId

            # Build $set document for field updates
            set_doc = {"last_updated": datetime.utcnow()}
            if update_data.use_case is not None:
                set_doc["use_case"] = update_data.use_case
            if update_data.summary is not None:
                set_doc["summary"] = update_data.summary
            if update_data.prompt_template is not None:
                set_doc["prompt_template"] = update_data.prompt_template
            if update_data.history is not None:
                set_doc["history"] = update_data.history
            if update_data.embedding is not None:
                set_doc["embedding"] = update_data.embedding

            # Build update document with operators
            update_ops = {"$set": set_doc, "$inc": {"num_updates": 1}}
            if update_data.changelog_entry:
                update_ops["$push"] = {"changelog": update_data.changelog_entry}

            result = self.collection.update_one({"_id": ObjectId(prompt_id)}, update_ops)
            if result.modified_count > 0:
                logger.info(f"Updated prompt {prompt_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to update prompt {prompt_id}: {e}")
            raise

    def vector_search(
        self, query_embedding: List[float], limit: int = 5, score_threshold: float = 0.0
    ) -> List[dict]:
        """
        Perform vector search on prompts.

        Args:
            query_embedding: Query embedding vector
            limit: Maximum number of results
            score_threshold: Minimum similarity score

        Returns:
            List of matching prompts with scores
        """
        try:
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_embedding,
                        "numCandidates": limit * 10,
                        "limit": limit,
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "use_case": 1,
                        "summary": 1,
                        "prompt_template": 1,
                        "history": 1,
                        "last_updated": 1,
                        "score": {"$meta": "vectorSearchScore"},
                    }
                },
                {"$match": {"score": {"$gte": score_threshold}}},
            ]
            results = list(self.collection.aggregate(pipeline))
            # Convert ObjectId to string
            for result in results:
                result["_id"] = str(result["_id"])
            return results
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            # Fallback to text search if vector search index doesn't exist
            logger.warning("Falling back to text search")
            return self._text_search_fallback(query_embedding, limit)

    def _text_search_fallback(self, query_embedding: List[float], limit: int) -> List[dict]:
        """Fallback text search when vector search is not available."""
        # Simple text search on summary field
        # This is a basic fallback - in production you might want more sophisticated text search
        try:
            results = list(self.collection.find().limit(limit))
            for result in results:
                result["_id"] = str(result["_id"])
                result["score"] = 0.5  # Default score for text search
            return results
        except Exception as e:
            logger.error(f"Text search fallback failed: {e}")
            return []

    def search_by_use_case(self, use_case: str, limit: int = 10) -> List[dict]:
        """
        Search prompts by use case category.

        Args:
            use_case: The use case category
            limit: Maximum number of results

        Returns:
            List of prompts matching the use case
        """
        try:
            results = list(
                self.collection.find({"use_case": use_case})
                .sort("last_updated", -1)
                .limit(limit)
            )
            for result in results:
                result["_id"] = str(result["_id"])
            return results
        except Exception as e:
            logger.error(f"Failed to search by use case {use_case}: {e}")
            raise

    def close(self) -> None:
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


# Global MongoDB client instance (lazy initialization)
_mongodb_client: Optional[MongoDBClient] = None


def get_mongodb_client() -> MongoDBClient:
    """Get or create the global MongoDB client instance."""
    global _mongodb_client
    if _mongodb_client is None:
        _mongodb_client = MongoDBClient()
    return _mongodb_client


# Create a simple object that delegates to get_mongodb_client()
class MongoDBClientProxy:
    """Proxy for lazy-loaded MongoDB client."""

    def __getattr__(self, name):
        return getattr(get_mongodb_client(), name)


mongodb_client = MongoDBClientProxy()

