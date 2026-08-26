"""
memory.py
----------
This module handles the "memory" of our self-learning agent.

Tasks:
1. Convert user's text into an embedding (a list of numbers)
2. Store that embedding in ChromaDB along with the user_id
3. Find related previous memories when a new query is received
   using similarity search
"""

import chromadb
from sentence_transformers import SentenceTransformer
import uuid


class MemoryManager:
    def __init__(self, db_path: str = "./chroma_data"):
        # Load the embedding model (runs locally, so there is no API cost)
        # 'all-MiniLM-L6-v2' is a small and fast model with good accuracy
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        # Create a ChromaDB client — persistent, so data is saved to disk
        self.client = chromadb.PersistentClient(path=db_path)

        # Create a collection (similar to a table in a traditional database)
        self.collection = self.client.get_or_create_collection(
            name="agent_memory"
        )

    def add_memory(self, user_id: str, text: str):
        """
        Store the user's text as a memory.
        Each memory is tagged with a user_id so that
        memories from different users do not get mixed.
        """
        embedding = self.embedder.encode(text).tolist()
        memory_id = str(uuid.uuid4())

        self.collection.add(
            ids=[memory_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{"user_id": user_id}],
        )

        print(f"[Memory Saved] {text}")

    def search_memory(self, user_id: str, query: str, top_k: int = 3):
        """
        Find the top related memories for a query
        only for the specified user_id.
        """
        query_embedding = self.embedder.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={"user_id": user_id},  # Search only this user's memories
        )

        # results['documents'] is a list of lists, so get the first element
        memories = results["documents"][0] if results["documents"] else []
        return memories


# --- Quick test (run this file directly to check if it works) ---
if __name__ == "__main__":
    mem = MemoryManager()

    user = "girish_test"

    # Store some facts
    mem.add_memory(user, "I like playing cricket")
    mem.add_memory(user, "I am learning AI/ML")
    mem.add_memory(user, "My favorite color is blue")

    # Search for related memories
    print("\n--- Searching related memories ---")
    results = mem.search_memory(user, "What should I do on the weekend?")

    for r in results:
        print("Found:", r)