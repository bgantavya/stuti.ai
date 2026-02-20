import os
import dotenv
from google import genai
from configs import SYSTEM_INSTRUCTIONS
from tools import GS
from memoryDB import MemoryDB

# TODO: need to ad exception so if we lack model availability we transfer calls to a lower val model
# or figure out ollama endpoint

class BotEngine:
    def __init__(self):
        dotenv.load_dotenv()
        self.apiKey = os.getenv('GOOGLE_API_KEY')
        self.client = None
        self.chatSession = None
        self.memory = MemoryDB()
        self.InitializeClient()

    def InitializeClient(self):
        '''Validate API key and setup a GENAI client'''
        if not self.apiKey or self.apiKey == 'YOUR_API_KEY_HERE':
            raise ValueError('Invalid API Key. Please check your environment variables. (.env)[file]')
        
        try:
            self.client = genai.Client(api_key=self.apiKey)
            history = self._format_history(self.memory.load_history())
            self.chatSession = self.client.chats.create(
                model='gemini-2.5-flash',
                config=genai.types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTIONS,
                    temperature=1,
                    thinking_config=genai.types.ThinkingConfig(
                        include_thoughts=True,
                    ),
                    tools=[GS.grounding_tool],
                ),
                history=history,
            )
        except Exception as e:
            raise ConnectionError(f'Failed to Establish connection: {e}')

    def _format_history(self, history_rows):
        formatted = []
        for role, message, _timestamp in history_rows:
            if not message:
                continue
            formatted.append({"role": role, "parts": [{"text": message}]})
        return formatted

    def getResponse(self, user_text):
        '''Sends text to AI and returns the response text.'''
        if not self.chatSession:
            return "Error: AI Client not initialized."
        
        try:
            self.memory.save_message("user", user_text)
            response = self.chatSession.send_message(user_text)
            response_text = getattr(response, "text", "") or ""
            self.memory.save_message("model", response_text)
            return response_text
        except Exception as e:
            return f'Error communicating with Stuti: {e}'
