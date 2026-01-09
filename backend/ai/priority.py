"""
Message Prioritization - Ranks messages by importance
"""

import logging
from typing import List, Dict, Any
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class MessagePrioritizer:
    """
    Ranks messages by importance using multiple factors
    """
    
    # Priority keywords
    URGENT_KEYWORDS = [
        "urgent", "asap", "immediately", "emergency", "critical",
        "important", "priority", "now", "right away"
    ]
    
    PROBLEM_KEYWORDS = [
        "error", "broken", "not working", "issue", "problem",
        "failed", "crash", "down", "outage"
    ]
    
    QUESTION_KEYWORDS = [
        "?", "how", "what", "why", "when", "where", "help"
    ]
    
    def __init__(self):
        logger.info("MessagePrioritizer initialized")
    
    def rank(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank messages by priority
        
        Args:
            messages: List of message dictionaries with at least 'body' field
            
        Returns:
            List of messages sorted by priority (highest first)
        """
        if not messages:
            return []
        
        # Score each message
        scored_messages = []
        for msg in messages:
            score = self._calculate_priority_score(msg)
            msg_copy = msg.copy()
            msg_copy["priority_score"] = score
            scored_messages.append(msg_copy)
        
        # Sort by score (descending)
        ranked = sorted(scored_messages, key=lambda x: x["priority_score"], reverse=True)
        
        logger.info(f"Ranked {len(ranked)} messages")
        return ranked
    
    def _calculate_priority_score(self, message: Dict[str, Any]) -> float:
        """
        Calculate priority score for a message
        
        Factors:
        - Message length (longer = more important)
        - Urgent keywords
        - Problem keywords
        - Question keywords
        - Timestamp (recent = more important)
        - User importance (if available)
        """
        score = 0.0
        body = message.get("body", "").lower()
        
        # Base score from length (normalized)
        body_length = len(body.split())
        score += min(body_length / 50.0, 2.0)  # Cap at 2.0
        
        # Urgent keywords
        urgent_count = sum(1 for keyword in self.URGENT_KEYWORDS if keyword in body)
        score += urgent_count * 3.0
        
        # Problem keywords
        problem_count = sum(1 for keyword in self.PROBLEM_KEYWORDS if keyword in body)
        score += problem_count * 2.0
        
        # Question keywords
        question_count = sum(1 for keyword in self.QUESTION_KEYWORDS if keyword in body)
        score += question_count * 1.0
        
        # Timestamp factor (if available)
        timestamp = message.get("timestamp") or message.get("origin_server_ts")
        if timestamp:
            try:
                # Convert to datetime if it's a timestamp
                if isinstance(timestamp, (int, float)):
                    msg_time = datetime.fromtimestamp(timestamp / 1000)
                else:
                    msg_time = datetime.fromisoformat(str(timestamp))
                
                # More recent = higher score
                now = datetime.now()
                hours_ago = (now - msg_time).total_seconds() / 3600
                if hours_ago < 24:
                    score += 2.0 - (hours_ago / 24.0)  # Decay over 24 hours
            except Exception as e:
                logger.warning(f"Error parsing timestamp: {e}")
        
        # User importance (if available)
        user_id = message.get("user_id", "")
        if "admin" in user_id.lower() or "support" in user_id.lower():
            score += 1.5
        
        # Mentions or @ symbols
        if "@" in body:
            score += 1.0
        
        # Exclamation marks (urgency indicator)
        exclamation_count = body.count("!")
        score += min(exclamation_count * 0.5, 2.0)
        
        return round(score, 2)
