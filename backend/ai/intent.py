"""
Intent Parsing using NLP and Hugging Face models
"""

import logging
import re
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

logger = logging.getLogger(__name__)


class IntentParser:
    """
    Parses user intent from messages using DistilBERT and rule-based methods
    """
    
    # Intent categories
    INTENTS = [
        "question",
        "complaint",
        "order",
        "support",
        "general"
    ]
    
    def __init__(self):
        logger.info("Loading intent classification model...")
        try:
            # Use a fine-tuned model or base model with custom classification
            # For MVP, we'll use distilbert with custom logic
            self.classifier = pipeline(
                "text-classification",
                model="distilbert-base-uncased",
                device=-1 if not torch.cuda.is_available() else 0
            )
            logger.info("Intent model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading intent model: {e}")
            self.classifier = None
        
        # Keyword patterns for intent detection
        self.intent_patterns = {
            "question": [
                r"\?",
                r"how\s+(do|does|can|will|should)",
                r"what\s+(is|are|do|does|can|will)",
                r"why\s+(is|are|do|does|can|will)",
                r"when\s+(is|are|do|does|can|will)",
                r"where\s+(is|are|do|does|can|will)",
                r"help\s+(me|with)",
                r"can\s+you\s+(help|tell|explain)",
            ],
            "complaint": [
                r"problem",
                r"issue",
                r"error",
                r"broken",
                r"not\s+working",
                r"doesn't\s+work",
                r"bad",
                r"terrible",
                r"awful",
                r"disappointed",
                r"refund",
                r"cancel",
            ],
            "order": [
                r"order",
                r"purchase",
                r"buy",
                r"checkout",
                r"payment",
                r"delivery",
                r"shipping",
                r"track",
            ],
            "support": [
                r"support",
                r"help",
                r"assistance",
                r"contact",
                r"customer\s+service",
            ],
        }
    
    def parse(self, message: str) -> dict:
        """
        Parse intent from a message
        
        Args:
            message: Input message text
            
        Returns:
            Dictionary with intent, confidence, and entities
        """
        if not message or len(message.strip()) == 0:
            return {
                "intent": "general",
                "confidence": 0.0,
                "entities": []
            }
        
        message_lower = message.lower()
        
        # Rule-based intent detection (primary method for MVP)
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, message_lower, re.IGNORECASE))
                score += matches
            intent_scores[intent] = score
        
        # Find highest scoring intent
        if intent_scores and max(intent_scores.values()) > 0:
            detected_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[detected_intent] / 3.0, 1.0)  # Normalize
        else:
            detected_intent = "general"
            confidence = 0.5
        
        # Extract entities (simple keyword extraction)
        entities = self._extract_entities(message)
        
        logger.info(f"Detected intent: {detected_intent} (confidence: {confidence:.2f})")
        
        return {
            "intent": detected_intent,
            "confidence": confidence,
            "entities": entities
        }
    
    def _extract_entities(self, message: str) -> list:
        """
        Extract simple entities from message
        """
        entities = []
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, message)
        for email in emails:
            entities.append({"type": "email", "value": email})
        
        # URL pattern
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, message)
        for url in urls:
            entities.append({"type": "url", "value": url})
        
        # Phone number pattern (simple)
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, message)
        for phone in phones:
            entities.append({"type": "phone", "value": phone})
        
        return entities
