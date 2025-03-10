from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
import os
import random
import numpy as np
import soundfile as sf

app = FastAPI()

# Ensure sounds folder exists
os.makedirs("sounds", exist_ok=True)

# Generate sound based on input
def generate_sound(effect_name):
    sample_rate = 44100  # CD-quality audio
    duration = 3  # 3 seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Different sound variations
    if "explosion" in effect_name.lower():
        sound = 0.5 * np.sin(2 * np.pi * 200 * t) * np.exp(-3 * t)
    elif "laser" in effect_name.lower():
        sound = 0.5 * np.sin(2 * np.pi * 1000 * t) * np.exp(-2 * t)
    elif "wind" in effect_name.lower():
        sound = np.random.uniform(-0.2, 0.2, size=t.shape)
    else:
        sound = np.sin(2 * np.pi * random.randint(200, 1000) * t)

    filename = f"sounds/{effect_name.replace(' ', '_')}.wav"
    sf.write(filename, sound, sample_rate)
    return filename

@app.post("/generate/")
async def generate_sound_effect(effect: str = Form(...)):
    file_path = generate_sound(effect)
    return JSONResponse({"audio_url": f"/download/{os.path.basename(file_path)}"})

@app.get("/download/{filename}")
async def download_sound(filename: str):
    file_path = f"sounds/{filename}"
    return FileResponse(file_path, media_type="audio/wav", filename=filename)

# ✅ Add this route to fix the "Not Found" issue
@app.get("/")
def home():
    return {"message": "AI Sound Generator is Running!"}
