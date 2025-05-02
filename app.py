import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from starlette.concurrency import run_in_threadpool # Import run_in_threadpool
import uvicorn
import os # Import the os module
from src.whisper import process_audio_sync
from constants import *
app = FastAPI()



@app.post("/transcribe")
async def transcribe_audio(
    audio_file: UploadFile = File(..., description="Audio file (WAV/MP3 format)")
):
    try:
        audio_data = await audio_file.read()
        audio_buffer = io.BytesIO(audio_data)
        transcription = await run_in_threadpool(process_audio_sync, audio_buffer)
        return transcription

    except Exception as e:
        raise HTTPException(500, f"Processing failed: {str(e)}")


if __name__ == "__main__":

    uvicorn.run("app:app", host=HOST, port=PORT, reload=True)