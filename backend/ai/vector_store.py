"""
Vector Storage and Retrieval using FAISS
"""

import logging
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Manages vector embeddings and semantic search using FAISS
    """
    
    def __init__(self, store_path: str = "/app/vector_store"):
        self.store_path = store_path
        self.index = None
        self.metadata = []
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
        
        # Initialize embedding model
        logger.info("Loading sentence transformer model...")
        try:
            self.encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            raise
        
        # Create store directory if it doesn't exist
        os.makedirs(store_path, exist_ok=True)
        
        # Load existing index if available
        self._load_index()
    
    def _load_index(self):
        """Load existing FAISS index from disk"""
        index_path = os.path.join(self.store_path, "index.faiss")
        metadata_path = os.path.join(self.store_path, "metadata.json")
        
        if os.path.exists(index_path) and os.path.exists(metadata_path):
            try:
                self.index = faiss.read_index(index_path)
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                logger.info(f"Loaded existing index with {len(self.metadata)} entries")
            except Exception as e:
                logger.warning(f"Error loading existing index: {e}, creating new one")
                self._create_new_index()
        else:
            self._create_new_index()
    
    def _create_new_index(self):
        """Create a new FAISS index"""
        # Use L2 distance (Euclidean)
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []
        logger.info("Created new FAISS index")
    
    def _save_index(self):
        """Save FAISS index and metadata to disk"""
        try:
            index_path = os.path.join(self.store_path, "index.faiss")
            metadata_path = os.path.join(self.store_path, "metadata.json")
            
            faiss.write_index(self.index, index_path)
            with open(metadata_path, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            
            logger.info(f"Saved index with {len(self.metadata)} entries")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    def store_conversation(
        self,
        conversation_id: str,
        messages: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Store conversation embeddings in FAISS
        
        Args:
            conversation_id: Unique identifier for conversation
            messages: List of message dictionaries
            metadata: Additional metadata to store
        """
        if not messages:
            logger.warning("No messages to store")
            return
        
        # Combine messages into conversation text
        conversation_texts = []
        for msg in messages:
            body = msg.get("body", "")
            if body:
                conversation_texts.append(body)
        
        if not conversation_texts:
            logger.warning("No text content in messages")
            return
        
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(conversation_texts)} messages")
        embeddings = self.encoder.encode(conversation_texts, show_progress_bar=False)
        
        # Convert to numpy array
        embeddings = np.array(embeddings).astype('float32')
        
        # Add to index
        self.index.add(embeddings)
        
        # Store metadata for each message
        for i, msg in enumerate(messages):
            if msg.get("body"):
                self.metadata.append({
                    "conversation_id": conversation_id,
                    "message_id": msg.get("id", f"msg_{i}"),
                    "body": msg.get("body", ""),
                    "user_id": msg.get("user_id", ""),
                    "timestamp": msg.get("timestamp") or msg.get("origin_server_ts"),
                    "metadata": metadata or {}
                })
        
        # Save to disk
        self._save_index()
        logger.info(f"Stored conversation {conversation_id} with {len(conversation_texts)} messages")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Semantic search over stored conversations
        
        Args:
            query: Search query text
            top_k: Number of results to return
            
        Returns:
            List of matching conversations with similarity scores
        """
        if self.index.ntotal == 0:
            logger.warning("Index is empty, no results to return")
            return []
        
        # Generate query embedding
        query_embedding = self.encoder.encode([query], show_progress_bar=False)
        query_embedding = np.array(query_embedding).astype('float32')
        
        # Search in FAISS
        k = min(top_k, self.index.ntotal)
        distances, indices = self.index.search(query_embedding, k)
        
        # Build results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.metadata):
                metadata = self.metadata[idx].copy()
                # Convert L2 distance to similarity score (lower distance = higher similarity)
                distance = float(distances[0][i])
                similarity = 1.0 / (1.0 + distance)  # Convert distance to similarity
                metadata["similarity_score"] = round(similarity, 4)
                metadata["distance"] = round(distance, 4)
                results.append(metadata)
        
        logger.info(f"Search returned {len(results)} results for query: {query[:50]}")
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        return {
            "total_vectors": self.index.ntotal,
            "dimension": self.dimension,
            "conversations": len(set(m.get("conversation_id") for m in self.metadata))
        }
