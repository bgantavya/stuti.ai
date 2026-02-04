import os
import dotenv
from configs import SYSTEM_INSTRUCTIONS
from google import genai

class BotEngine:
    def __init__(self):
        dotenv.load_dotenv()
        self.apiKey = os.getenv('GOOGLE_API_KEY')
        self.client = None
        self.chatSession = None
        self.InitializeClient()

    def InitializeClient(self):
        '''Validate API key and setup a GENAI client'''
        if not self.apiKey or self.apiKey == 'YOUR_API_KEY_HERE':
            raise ValueError('Invalid API Key. Please check your environment variables. (.env)[file]')
        
        try:
            self.client = genai.Client(api_key=self.apiKey)
            self.chatSession = self.client.chats.create(
                model = 'gemini-3-flash-preview',
                config = genai.types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTIONS,
                    temperature=1,
                )
            )
        except Exception as e:
            raise ConnectionError(f'Failed to Establish connection: {e}')

    def getResponse(self, user_text):
        '''Sends text to AI and returns the response text.'''
        if not self.chatSession:
            return "Error: AI Client not initialized."
        
        try:
            response = self.chatSession.send_message(user_text)
            return response.text
        except Exception as e:
            return f'Error communicating with Stuti: {e}'
