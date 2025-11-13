import os
import google.generativeai as genai
from typing import Optional

class GeminiProvider:
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro"):
        """Initialize the Gemini provider.
        
        Args:
            api_key: Google Gemini API key. If not provided, will look for GOOGLE_API_KEY environment variable.
            model: The model to use (default: gemini-pro)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is required. Please set the GOOGLE_API_KEY environment variable or pass it to the constructor.")
            
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)
        
    def generate(self, query: str) -> str:
        """Generate a response using the Gemini model.
        
        Args:
            query: The user's query about sports
            
        Returns:
            str: The generated response
        """
        try:
            # Create a more specific prompt for sports-related queries
            prompt = f"""You are a knowledgeable sports analyst. Provide a detailed, accurate response to the following sports-related query.
            
            Query: {query}
            
            Guidelines:
            - Focus on facts and analysis
            - If the query is about rules, explain them clearly
            - For player/team comparisons, provide balanced analysis
            - For predictions, clearly state they are speculative
            - Keep the response professional and informative
            - If the query is not sports-related, politely decline to answer
            
            Response:"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error generating response: {str(e)}"

# Example usage:
if __name__ == "__main__":
    # Test the provider
    import os
    provider = GeminiProvider(api_key=os.getenv("GOOGLE_API_KEY"))
    print(provider.generate("Explain the rules of cricket"))
