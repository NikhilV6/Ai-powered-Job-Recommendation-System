from typing import List, Dict
from datetime import datetime

from app.core.database import db


_collection = db["chat_messages"]


class MongoChatMemory:
    """
    Simple MongoDB-based chat memory:
    Stores one document per message:
    {
      session_id: str,
      role: "user"|"assistant",
      content: str,
      timestamp: datetime
    }
    """

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        cursor = (
            _collection
            .find({"session_id": session_id})
            .sort("timestamp", 1)
        )
        history: List[Dict[str, str]] = []
        for doc in cursor:
            history.append(
                {
                    "role": doc.get("role", "user"),
                    "content": doc.get("content", ""),
                }
            )
        return history

    def add_message(self, session_id: str, role: str, content: str) -> None:
        _collection.insert_one(
            {
                "session_id": session_id,
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow(),
            }
        )


chat_memory = MongoChatMemory()
