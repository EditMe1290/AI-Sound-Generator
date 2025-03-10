from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
import torch
import torchaudio
import io
import uvicorn
import os
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

# Mount static files (Ensure the 'static' folder exists)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 template engine (Ensure 'templates' folder exists)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/generate_sound")
def generate_sound():
    sample_rate = 22050
    waveform = torch.randn(1, sample_rate * 3)  # 3-second random noise

    # Define file path
    output_path = "generated_sound.wav"
    
    # Save the waveform to a file
    torchaudio.save(output_path, waveform, sample_rate, format="wav")
    
    return FileResponse(output_path, media_type="audio/wav", filename="generated_sound.wav")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
