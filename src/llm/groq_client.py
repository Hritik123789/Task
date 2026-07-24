from groq import Groq
import config

class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=config.GROQ_API_KEY)
    
    def generate(self, prompt):
        """Send prompt to Groq API, return response text."""
        response = self.client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
