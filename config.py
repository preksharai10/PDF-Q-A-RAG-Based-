import os
from dotenv import load_dotenv                                  # Loads environment variables from a .env file
import google.generativeai as genai                             # Import Google Generative AI module

load_dotenv()                                                   # Loading environment variables from .env  

API_KEY = os.getenv("GOOGLE_API_KEY")                           # Retrieving the Gemini API key from env variables
UPLOAD_DIR = "uploads"                                          # Directory to save uploaded files 

genai.configure(api_key=API_KEY)                                # Configuring the Generative AI module with the API key
chat_model = genai.GenerativeModel("gemini-1.5-flash")          # Initializing the Gemini model 
