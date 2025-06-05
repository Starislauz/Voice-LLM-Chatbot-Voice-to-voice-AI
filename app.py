from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import speech_recognition as sr
from gemini_brain import GeminiBrain
import io

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.post("/ask")
async def ask(
    request: Request,
    message: str = Form(None),
    audio: UploadFile = File(None)
):
    ai = GeminiBrain()
    user_input = None

    # If JSON, get message from body
    if request.headers.get("content-type", "").startswith("application/json"):
        data = await request.json()
        user_input = data.get("message")
    # If audio is provided, transcribe it
    elif audio is not None:
        recognizer = sr.Recognizer()
        audio_bytes = await audio.read()
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = recognizer.record(source)
            try:
                user_input = recognizer.recognize_google(audio_data)
            except Exception as e:
                return JSONResponse(content={"error": f"Speech recognition failed: {e}"}, status_code=400)
    elif message:
        user_input = message
    else:
        return JSONResponse(content={"error": "No message or audio provided"}, status_code=400)

    if not user_input:
        return JSONResponse(content={"error": "No message provided"}, status_code=400)

    response = ai.ask(user_input)
    return {"response": response}