"""
Text processing utilities for the Sports Agent application.
"""

def clean_text(text: str) -> str:
    """
    Clean and normalize text input.
    
    Args:
        text: Input text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace and newlines
    text = ' '.join(text.split())
    
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

def truncate_text(text: str, max_length: int = 100, ellipsis: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Input text
        max_length: Maximum length of the output string
        ellipsis: String to append if text is truncated
        
    Returns:
        str: Truncated text with ellipsis if needed
    """
    if not text:
        return ""
        
    if len(text) <= max_length:
        return text
        
    return text[:max_length - len(ellipsis)] + ellipsis

if __name__ == "__main__":
    # Example usage
    sample = "   This is a test   string with   multiple   spaces.   "
    print(f"Original: '{sample}'")
    print(f"Cleaned: '{clean_text(sample)}'")
    print(f"Word count: {count_words(sample)}")
    print(f"Truncated: {truncate_text(sample, 20)}")
