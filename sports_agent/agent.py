import os
from typing import Optional
from .providers.rule_based import RuleBasedProvider

try:
    from .providers.openai_provider import OpenAIProvider
except Exception:
    OpenAIProvider = None  # type: ignore

try:
    from .providers.gemini_provider import GeminiProvider
except Exception as e:
    GeminiProvider = None  # type: ignore


class SportsAgent:
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize the Sports Agent with the specified provider.
        
        Args:
            provider: The provider to use ('gemini', 'openai', or 'rule')
            model: The model to use (provider-specific)
            api_key: API key for the provider (if required)
        """
        selected = (provider or os.getenv("SPORTS_AGENT_PROVIDER") or "rule").lower()
        
        if selected == "gemini":
            if GeminiProvider is None:
                raise ImportError("Gemini provider is not available. Make sure to install required dependencies.")
            self.provider = GeminiProvider(api_key=api_key or os.getenv("GOOGLE_API_KEY"), model=model or "gemini-pro")
        elif selected == "openai" and OpenAIProvider is not None:
            self.provider = OpenAIProvider(model=model)
        else:
            self.provider = RuleBasedProvider()

    def respond(self, query: str) -> str:
        """Generate a response to the given query.
        
        Args:
            query: The user's query about sports
            
        Returns:
            str: The generated response
        """
        return self.provider.generate(query)
