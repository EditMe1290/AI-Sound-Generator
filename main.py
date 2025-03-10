from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
import torch
import torchaudio
import io
import uvicorn
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/generate_sound")
def generate_sound():
    sample_rate = 22050
    waveform = torch.randn(1, sample_rate * 3)  # 3-second random noise
    buffer = io.BytesIO()
    torchaudio.save(buffer, waveform, sample_rate, format="wav")
    buffer.seek(0)
    return FileResponse(buffer, media_type="audio/wav", filename="generated_sound.wav")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
