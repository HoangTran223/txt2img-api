from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch
import base64
from io import BytesIO
from PIL import Image
import os
from fastapi.responses import FileResponse

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str


pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

GENERATED_DIR = "/workspace/txt2img-api/generated_images"
os.makedirs(GENERATED_DIR, exist_ok=True)

@app.post("/generate")
def generate_image(request: PromptRequest):
    try:
        image = pipe(request.prompt).images[0]
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return {"image_base64": img_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_and_save")
def generate_and_save(request: PromptRequest):
    try:
        image = pipe(request.prompt).images[0]
        filename = f"{request.prompt.replace(' ', '_')[:50]}_{torch.randint(0, 1_000_000, (1,)).item()}.png"
        save_path = os.path.join(GENERATED_DIR, filename)
        image.save(save_path, format="PNG")
        return {"file_path": save_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_image")
def get_image(filename: str):
    file_path = os.path.join(GENERATED_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="image/png")