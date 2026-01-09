# AI Module Documentation

This module contains all AI-powered features for conversation analysis.

## Components

### 1. Summarizer (`summarizer.py`)
- **Model**: `facebook/bart-large-cnn`
- **Purpose**: Condense long conversations into concise summaries
- **Usage**: 
  ```python
  from ai.summarizer import ConversationSummarizer
  summarizer = ConversationSummarizer()
  summary = summarizer.summarize(text, max_length=150, min_length=30)
  ```

### 2. Intent Parser (`intent.py`)
- **Model**: `distilbert-base-uncased` + rule-based patterns
- **Purpose**: Classify user intent from messages
- **Intents**: question, complaint, order, support, general
- **Usage**:
  ```python
  from ai.intent import IntentParser
  parser = IntentParser()
  result = parser.parse("I need help with my order")
  # Returns: {"intent": "order", "confidence": 0.85, "entities": []}
  ```

### 3. Message Prioritizer (`priority.py`)
- **Algorithm**: Multi-factor scoring
- **Factors**: 
  - Message length
  - Urgent keywords
  - Problem indicators
  - Timestamp recency
  - User importance
- **Usage**:
  ```python
  from ai.priority import MessagePrioritizer
  prioritizer = MessagePrioritizer()
  ranked = prioritizer.rank(messages)
  ```

### 4. Vector Store (`vector_store.py`)
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Storage**: FAISS (Facebook AI Similarity Search)
- **Purpose**: Semantic search over conversations
- **Usage**:
  ```python
  from ai.vector_store import VectorStore
  store = VectorStore()
  store.store_conversation(conversation_id, messages)
  results = store.search("user query", top_k=5)
  ```

## Model Loading

Models are downloaded automatically on first use. This may take several minutes:
- BART: ~1.6GB
- DistilBERT: ~250MB
- Sentence Transformers: ~90MB

Models are cached in Hugging Face cache directory.

## Performance

- **Summarization**: 2-5 seconds (first call), <1s (cached)
- **Intent Parsing**: <500ms
- **Prioritization**: <100ms
- **Vector Search**: <100ms (small dataset)

## Memory Requirements

- Minimum: 4GB RAM
- Recommended: 8GB+ RAM
- GPU: Optional (CUDA supported if available)

## Future Improvements

- [ ] Fine-tune models on domain-specific data
- [ ] Add more intent categories
- [ ] Implement conversation clustering
- [ ] Add sentiment analysis
- [ ] Support multiple languages
