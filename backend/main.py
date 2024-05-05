#fastapi dev main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config 
import openai
from fastapi.responses import JSONResponse
import asyncio
from dotenv import load_dotenv
import os


#custom function imports
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages
from functions.text_to_speech import convert_to_speech

load_dotenv()


#initiate app
app = FastAPI()

#cors-origin
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
]

#Cors - middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


#check_health
@app.get("/health")
async def check_health():
    return {"message": "Healthy"}

#reset messages 
@app.get("/reset")
async def reset_conversation():
    reset_conversation()
    response = JSONResponse(content={"message": "Conversation Reset"})
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    return response

#Get Audio
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):

    #Get saved audio
    #audio_input = open("voice.mp3", "rb")

    #SAVE File from frontend
    with open (file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    #decode audio
    message_decoded = convert_audio_to_text(audio_input)

    #Ensure Message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")
    
    #get chat-GPT response
    chat_response = get_chat_response(message_decoded)

    #no chat response
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    #store messages 
    store_messages(message_decoded, chat_response)

    #convert chat response to audio 
    audio_output = convert_to_speech(chat_response)

    #no audio output
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get Eleven Labs audio response")
    
    #create a generator that yeilds data 
    def iterfile():
        yield audio_output

    #return audio file 
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

