"""
Conversation Summarization using Hugging Face BART model
"""

import logging
# Note: transformers and torch are installed in Docker container
# For local IDE support, install: pip install -r requirements.txt
from transformers import pipeline
import torch

logger = logging.getLogger(__name__)


class ConversationSummarizer:
    """
    Summarizes conversations using facebook/bart-large-cnn model
    """
    
    def __init__(self):
        logger.info("Loading BART summarization model...")
        try:
            # Use pipeline for easier usage
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1 if not torch.cuda.is_available() else 0
            )
            logger.info("BART model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading BART model: {e}")
            # Fallback to a smaller model if BART fails
            logger.info("Falling back to distilbart model...")
            self.summarizer = pipeline(
                "summarization",
                model="sshleifer/distilbart-cnn-12-6",
                device=-1
            )
    
    def summarize(self, text: str, max_length: int = 150, min_length: int = 30) -> str:
        """
        Summarize the input text
        
        Args:
            text: Input conversation text
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            
        Returns:
            Summarized text
        """
        if not text or len(text.strip()) == 0:
            return "No text to summarize."
        
        # BART has token limit, truncate if needed
        max_input_length = 1024
        if len(text) > max_input_length:
            text = text[:max_input_length]
            logger.warning(f"Text truncated to {max_input_length} characters")
        
        try:
            result = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            
            summary = result[0]["summary_text"]
            logger.info(f"Generated summary of length {len(summary)}")
            return summary
            
        except Exception as e:
            logger.error(f"Error during summarization: {e}")
            # Fallback: return first sentence or truncated text
            sentences = text.split(". ")
            if sentences:
                return sentences[0] + "."
            return text[:200] + "..."
