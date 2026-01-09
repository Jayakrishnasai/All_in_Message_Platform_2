"""
Dailyfix AI Backend - FastAPI Service
Provides AI-powered conversation analysis features
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import logging

from ai.summarizer import ConversationSummarizer
from ai.intent import IntentParser
from ai.priority import MessagePrioritizer
from ai.vector_store import VectorStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Dailyfix AI Backend",
    description="AI-powered conversation analysis API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI components
logger.info("Initializing AI components...")
summarizer = ConversationSummarizer()
intent_parser = IntentParser()
prioritizer = MessagePrioritizer()
vector_store = VectorStore()
logger.info("AI components initialized successfully")


# Request/Response Models
class SummarizeRequest(BaseModel):
    text: str
    max_length: Optional[int] = 150
    min_length: Optional[int] = 30


class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    compression_ratio: float


class IntentRequest(BaseModel):
    message: str


class IntentResponse(BaseModel):
    intent: str
    confidence: float
    entities: List[Dict[str, Any]]


class PriorityRequest(BaseModel):
    messages: List[Dict[str, Any]]


class PriorityResponse(BaseModel):
    ranked_messages: List[Dict[str, Any]]


class VectorStoreRequest(BaseModel):
    conversation_id: str
    messages: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None


class VectorSearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5


class VectorSearchResponse(BaseModel):
    results: List[Dict[str, Any]]


class DailyReportRequest(BaseModel):
    user_id: str
    date: str  # YYYY-MM-DD format
    conversations: Optional[List[Dict[str, Any]]] = None


class DailyReportResponse(BaseModel):
    user_id: str
    date: str
    total_conversations: int
    total_messages: int
    summary: str
    priority_messages: List[Dict[str, Any]]
    intent_distribution: Dict[str, int]
    key_insights: List[str]


# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "Dailyfix AI Backend",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


# Summarization endpoint
@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    """
    Summarize a conversation using BART model
    """
    try:
        logger.info(f"Summarizing text of length {len(request.text)}")
        summary = summarizer.summarize(
            request.text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        
        original_length = len(request.text.split())
        summary_length = len(summary.split())
        compression_ratio = summary_length / original_length if original_length > 0 else 0
        
        return SummarizeResponse(
            summary=summary,
            original_length=original_length,
            summary_length=summary_length,
            compression_ratio=compression_ratio
        )
    except Exception as e:
        logger.error(f"Error in summarization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")


# Intent parsing endpoint
@app.post("/intent", response_model=IntentResponse)
async def parse_intent(request: IntentRequest):
    """
    Parse user intent from a message
    """
    try:
        logger.info(f"Parsing intent for message: {request.message[:50]}...")
        result = intent_parser.parse(request.message)
        
        return IntentResponse(
            intent=result["intent"],
            confidence=result["confidence"],
            entities=result.get("entities", [])
        )
    except Exception as e:
        logger.error(f"Error in intent parsing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Intent parsing failed: {str(e)}")


# Priority ranking endpoint
@app.post("/priority", response_model=PriorityResponse)
async def prioritize_messages(request: PriorityRequest):
    """
    Rank messages by importance/priority
    """
    try:
        logger.info(f"Prioritizing {len(request.messages)} messages")
        ranked = prioritizer.rank(request.messages)
        
        return PriorityResponse(ranked_messages=ranked)
    except Exception as e:
        logger.error(f"Error in prioritization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prioritization failed: {str(e)}")


# Vector storage endpoint
@app.post("/vector/store")
async def store_vectors(request: VectorStoreRequest):
    """
    Store conversation embeddings in FAISS
    """
    try:
        logger.info(f"Storing vectors for conversation {request.conversation_id}")
        vector_store.store_conversation(
            conversation_id=request.conversation_id,
            messages=request.messages,
            metadata=request.metadata
        )
        
        return {
            "status": "success",
            "conversation_id": request.conversation_id,
            "messages_stored": len(request.messages)
        }
    except Exception as e:
        logger.error(f"Error storing vectors: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Vector storage failed: {str(e)}")


# Vector search endpoint
@app.post("/vector/search", response_model=VectorSearchResponse)
async def search_vectors(request: VectorSearchRequest):
    """
    Semantic search over stored conversations
    """
    try:
        logger.info(f"Searching vectors for query: {request.query[:50]}...")
        results = vector_store.search(request.query, top_k=request.top_k)
        
        return VectorSearchResponse(results=results)
    except Exception as e:
        logger.error(f"Error in vector search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Vector search failed: {str(e)}")


# Daily report endpoint
@app.post("/daily-report", response_model=DailyReportResponse)
async def generate_daily_report(request: DailyReportRequest):
    """
    Generate a comprehensive daily report for a user
    """
    try:
        logger.info(f"Generating daily report for user {request.user_id} on {request.date}")
        
        # If conversations not provided, return template
        if not request.conversations:
            return DailyReportResponse(
                user_id=request.user_id,
                date=request.date,
                total_conversations=0,
                total_messages=0,
                summary="No conversations found for this date.",
                priority_messages=[],
                intent_distribution={},
                key_insights=["No data available"]
            )
        
        # Aggregate data
        total_conversations = len(request.conversations)
        total_messages = sum(len(conv.get("messages", [])) for conv in request.conversations)
        
        # Combine all messages for summarization
        all_text = []
        all_messages = []
        intents = []
        
        for conv in request.conversations:
            messages = conv.get("messages", [])
            for msg in messages:
                text = msg.get("body", "")
                if text:
                    all_text.append(text)
                    all_messages.append(msg)
                    # Parse intent for each message
                    intent_result = intent_parser.parse(text)
                    intents.append(intent_result["intent"])
        
        # Generate summary
        combined_text = " ".join(all_text)
        if combined_text:
            summary = summarizer.summarize(combined_text, max_length=200, min_length=50)
        else:
            summary = "No messages to summarize."
        
        # Prioritize messages
        ranked_messages = prioritizer.rank(all_messages)[:5]  # Top 5
        
        # Intent distribution
        intent_dist = {}
        for intent in intents:
            intent_dist[intent] = intent_dist.get(intent, 0) + 1
        
        # Key insights
        insights = []
        if total_messages > 50:
            insights.append("High message volume detected - may need attention")
        if "complaint" in intent_dist and intent_dist["complaint"] > 0:
            insights.append(f"{intent_dist['complaint']} complaint(s) require follow-up")
        if "question" in intent_dist and intent_dist["question"] > 5:
            insights.append("Multiple questions detected - consider FAQ or documentation")
        if not insights:
            insights.append("Normal activity level")
        
        return DailyReportResponse(
            user_id=request.user_id,
            date=request.date,
            total_conversations=total_conversations,
            total_messages=total_messages,
            summary=summary,
            priority_messages=ranked_messages,
            intent_distribution=intent_dist,
            key_insights=insights
        )
        
    except Exception as e:
        logger.error(f"Error generating daily report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
