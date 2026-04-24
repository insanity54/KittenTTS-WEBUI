import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from kittentts import KittenTTS
import uvicorn

app = FastAPI(title="KittenTTS", version="1.0.0", description="High-quality text-to-speech API")

init_error = None
try:
    m = KittenTTS("KittenML/kitten-tts-mini-0.8")
except Exception as e:
    init_error = str(e)
    print(f"Error initializing KittenTTS: {init_error}")
    m = None

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


class GenerateRequest(BaseModel):
    text: str
    voice: str


class GenerateResponse(BaseModel):
    status: str
    filename: str


class Voice(BaseModel):
    name: str
    gender: str


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_audio(request: GenerateRequest):
    """Generate audio from text using the specified voice."""
    if not m:
        error_msg = f"TTS Model not initialized. {init_error if init_error else 'Please check console logs.'}"
        raise HTTPException(status_code=500, detail=error_msg)
    
    try:
        audio = m.generate(request.text, voice=request.voice)
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{request.voice}_{timestamp}.wav"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        counter = 1
        while os.path.exists(filepath):
            filename = f"{request.voice}_{timestamp}_{counter}.wav"
            filepath = os.path.join(OUTPUT_DIR, filename)
            counter += 1
            
        import soundfile as sf
        sf.write(filepath, audio, 24000)
        
        return {"status": "success", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/voices", response_model=list[Voice])
async def get_voices():
    """Get list of available voices."""
    return [
        {"name": "Bella", "gender": "Female"},
        {"name": "Kiki", "gender": "Female"},
        {"name": "Luna", "gender": "Female"},
        {"name": "Rosie", "gender": "Female"},
        {"name": "Bruno", "gender": "Male"},
        {"name": "Hugo", "gender": "Male"},
        {"name": "Jasper", "gender": "Male"},
        {"name": "Leo", "gender": "Male"}
    ]


@app.get("/output/{filename}")
async def download_file(filename: str):
    """Download a generated audio file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath, filename=filename)


app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7689)