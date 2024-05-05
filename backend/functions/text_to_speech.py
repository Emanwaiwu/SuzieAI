import requests
from decouple import config
from dotenv import load_dotenv
import os

load_dotenv()

ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

#eleven labs 
#convert Text to speech 
def convert_to_speech(message):
    body={
        "text": message,
        "voice_settings":{
        "stability": 0,
        "similarity_boost": 0,
        }
    }

    #define voice
    voice_rachel = "21m00Tcm4TlvDq8ikWAM"
    
    #constructing headers and endpoints
    headers = {"xi-api-key":ELEVEN_LABS_API_KEY, "Content-Type": "application/json", "accept": "audio/mpeg"}
    endpoints = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"
    
    #send request
    try:
        response = requests.post(endpoints, json=body, headers = headers)
    except Exception as e:
        return
    
    #handle response
    if response.status_code == 200:
        return response.content
    else:
        return