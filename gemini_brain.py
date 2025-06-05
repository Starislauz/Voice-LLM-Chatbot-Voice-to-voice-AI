import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

load_dotenv()

class GeminiBrain:
    def __init__(self):
        self.model = None
        self.chat_session = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize model with comprehensive error handling"""
        max_retries = 3
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise Exception("API key not found. Please set GOOGLE_API_KEY in your .env file.")

        for attempt in range(max_retries):
            try:
                genai.configure(api_key=api_key)
                
                # Verify API connection
                available_models = genai.list_models()
                if not available_models:
                    raise Exception("No models available - check API key")
                
                # Initialize model (using 1.5 Flash as default)
                self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
                self.chat_session = self.model.start_chat(history=[])
                print("✅ Gemini initialized successfully")
                return
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to initialize after {max_retries} attempts: {str(e)}")
                print(f"⚠️ Retrying initialization ({attempt+1}/{max_retries})...")
                time.sleep(2)
    
    def ask(self, query):
        """Send message with complete error protection"""
        if not self.chat_session:
            return "Error: Chat session not initialized"
        
        try:
            response = self.chat_session.send_message(query)
            return response.text
        except Exception as e:
            return f"⚠️ Error processing request: {str(e)}"
