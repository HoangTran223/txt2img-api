from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch
import base64
from io import BytesIO
from PIL import Image

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str


pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

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