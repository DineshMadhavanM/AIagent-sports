"""
Enhanced Text Processing Utilities for the Sports Agent Application.

This module provides various text processing functions including cleaning, formatting,
validation, and analysis of text data with a focus on sports-related content.
"""
import re
import string
from typing import List, Dict, Union, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TextStats:
    """Statistics about a text block."""
    word_count: int
    char_count: int
    sentence_count: int
    avg_word_length: float
    reading_time: float  # in minutes (assuming 200 words per minute)
    keywords: List[Tuple[str, int]]  # (word, frequency)
    sentiment: float  # -1.0 to 1.0 (negative to positive)

def clean_text(text: str, 
              remove_punctuation: bool = True,
              to_lower: bool = True) -> str:
    """
    Clean and normalize text input with configurable options.
    
    Args:
        text: Input text to clean
        remove_punctuation: Whether to remove punctuation
        to_lower: Whether to convert text to lowercase
        
    Returns:
        str: Cleaned and normalized text
    """
    if not text:
        return ""
    
    # Remove extra whitespace and newlines
    text = ' '.join(text.split())
    
    if remove_punctuation:
        # Remove punctuation using string.punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
    
    if to_lower:
        text = text.lower()
    
    return text.strip()

def count_words(text: str) -> int:
    """
    Count the number of words in the text.
    
    Args:
        text: Input text
        
    Returns:
        int: Word count
    """
    if not text:
        return 0
    return len(text.split())

def truncate_text(text: str, 
                 max_length: int = 100, 
                 ellipsis: str = "...",
                 whole_words: bool = True) -> str:
    """
    Truncate text to a maximum length, optionally at word boundaries.
    
    Args:
        text: Input text
        max_length: Maximum length of the output string
        ellipsis: String to append if text is truncated
        whole_words: If True, won't truncate in the middle of a word
        
    Returns:
        str: Truncated text with ellipsis if needed
    """
    if not text or len(text) <= max_length:
        return text
        
    if whole_words:
        # Find the last space before max_length
        truncated = text[:max_length - len(ellipsis)].rsplit(' ', 1)[0]
        return truncated + ellipsis if truncated else text[:max_length - len(ellipsis)] + ellipsis
    else:
        return text[:max_length - len(ellipsis)] + ellipsis

def extract_hashtags(text: str) -> List[str]:
    """
    Extract hashtags from text.
    
    Args:
        text: Input text containing hashtags
        
    Returns:
        List[str]: List of found hashtags (without the # symbol)
    """
    return re.findall(r'#(\w+)', text)

def extract_mentions(text: str) -> List[str]:
    """
    Extract @mentions from text.
    
    Args:
        text: Input text containing mentions
        
    Returns:
        List[str]: List of found mentions (without the @ symbol)
    """
    return re.findall(r'@(\w+)', text)

def analyze_text(text: str) -> TextStats:
    """
    Perform comprehensive text analysis.
    
    Args:
        text: Input text to analyze
        
    Returns:
        TextStats: Object containing various text statistics
    """
    if not text:
        return TextStats(0, 0, 0, 0.0, 0.0, [], 0.0)
    
    # Basic counts
    word_count = count_words(text)
    char_count = len(text)
    sentence_count = len(re.split(r'[.!?]+', text)) - 1
    
    # Calculate average word length
    words = text.split()
    avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
    
    # Estimate reading time (200 words per minute)
    reading_time = word_count / 200
    
    # Simple keyword extraction (top 5 most common words)
    word_freq: Dict[str, int] = {}
    for word in words:
        word = word.lower().strip(string.punctuation)
        if len(word) > 3:  # Only consider words longer than 3 characters
            word_freq[word] = word_freq.get(word, 0) + 1
    
    keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Very basic sentiment analysis (placeholder)
    positive_words = {'good', 'great', 'excellent', 'amazing', 'love', 'like', 'best'}
    negative_words = {'bad', 'poor', 'terrible', 'awful', 'hate', 'worst'}
    
    sentiment = 0
    word_list = [w.lower() for w in words]
    sentiment += sum(1 for w in word_list if w in positive_words)
    sentiment -= sum(1 for w in word_list if w in negative_words)
    sentiment = max(-1.0, min(1.0, sentiment / 10))  # Normalize to -1.0 to 1.0
    
    return TextStats(
        word_count=word_count,
        char_count=char_count,
        sentence_count=sentence_count,
        avg_word_length=round(avg_word_length, 2),
        reading_time=round(reading_time, 2),
        keywords=keywords,
        sentiment=round(sentiment, 2)
    )

def format_timestamp(timestamp: Union[str, int, float], 
                   format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a timestamp into a human-readable string.
    
    Args:
        timestamp: Unix timestamp or ISO format string
        format_str: Format string for datetime
        
    Returns:
        str: Formatted date string
    """
    if isinstance(timestamp, (int, float)):
        dt = datetime.fromtimestamp(timestamp)
    else:
        # Try to parse as ISO format
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return str(timestamp)
    
    return dt.strftime(format_str)

def generate_slug(text: str, max_length: int = 50) -> str:
    """
    Generate a URL-friendly slug from text.
    
    Args:
        text: Input text
        max_length: Maximum length of the generated slug
        
    Returns:
        str: Generated slug
    """
    if not text:
        return ""
    
    # Convert to lowercase and replace spaces with hyphens
    slug = text.lower()
    
    # Remove special characters
    slug = re.sub(r'[^\w\s-]', '', slug)
    
    # Replace spaces with hyphens
    slug = re.sub(r'[\s_-]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-').strip('_')
    
    # Truncate to max_length
    if len(slug) > max_length:
        slug = slug[:max_length].rsplit('-', 1)[0]
    
    return slug

if __name__ == "__main__":
    # Example usage
    sample = "   This is a test string with multiple spaces and #hashtags! @user123"
    print(f"Original: '{sample}'")
    print(f"Cleaned: '{clean_text(sample)}'")
    print(f"Word count: {count_words(sample)}")
    print(f"Truncated: {truncate_text(sample, 20, whole_words=True)}")
    print(f"Hashtags: {extract_hashtags(sample)}")
    print(f"Mentions: {extract_mentions(sample)}")
    
    # Advanced analysis
    analysis = analyze_text(sample)
    print(f"\nText Analysis:")
    print(f"- Words: {analysis.word_count}")
    print(f"- Characters: {analysis.char_count}")
    print(f"- Sentences: {analysis.sentence_count}")
    print(f"- Avg. Word Length: {analysis.avg_word_length}")
    print(f"- Reading Time: {analysis.reading_time} minutes")
    print(f"- Keywords: {analysis.keywords}")
    print(f"- Sentiment: {analysis.sentiment}")
    
    # Generate slug
    title = "This is a Sample Blog Post Title!"
    print(f"\nGenerated slug: {generate_slug(title)}")
    
    # Format timestamp
    print(f"Current time: {format_timestamp(datetime.now().timestamp())}")
