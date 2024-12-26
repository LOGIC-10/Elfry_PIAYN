from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
import uvicorn
import base64
from io import BytesIO
from PIL import Image
from typing import List
app = FastAPI()


class ImageRequest(BaseModel):
    google_api_key: str
    model_name: str
    prompt: str
    images: List[str]  # base64 encoded image
    temperature: float = 0.7
    max_tokens: int = 4096

@app.post("/generate")
async def generate_content(request: ImageRequest):
    try:
        client = genai.Client(api_key=request.google_api_key)
        # 添加输入验证
        if not request.images:
            raise HTTPException(status_code=400, detail="Image is required")
        if not request.prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")

        # 解码base64图片
        images = [base64.b64decode(image) for image in request.images]
        images = [Image.open(BytesIO(image)).resize((256, 256)) for image in images]

        # 发送请求到Gemini
        response = client.models.generate_content(
            model=request.model_name,
            contents=[
                *images,
                request.prompt
            ],
            config=types.GenerateContentConfig(
                temperature=request.temperature,
                max_output_tokens=request.max_tokens,
            )
        )
        # 返回结果
        return {
            "status": "success",
            "data": {
                "text": response.text,
                "candidates": response.candidates
            },
            "error": None
        }
    except ValueError as e:
        # return HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 添加日志记录
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)