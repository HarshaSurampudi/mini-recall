from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
import numpy as np
import torch
import open_clip
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from PIL import Image
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
client = QdrantClient(host="localhost", port=6333)

app.mount("/static", StaticFiles(directory="processed"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-g-14", pretrained="laion2B-s12B-b42K"
)
tokenizer = open_clip.get_tokenizer("ViT-g-14")

collection_name = "recall"
if not client.collection_exists(collection_name=collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": 1024, "distance": "Cosine"},
    )


class SearchRequest(BaseModel):
    text: str


@app.post("/get_image_embedding")
async def get_image_embedding(id: str = Form(...), image: UploadFile = File(...)):
    try:
        image_data = await image.read()
        image = Image.open(BytesIO(image_data))
        image = preprocess(image).unsqueeze(0)

        with torch.no_grad():
            image_features = model.encode_image(image)

        vector = np.array(image_features)[0]
        client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(id=id, vector=vector, payload={"image_path": f"{id}.png"})
            ],
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search")
async def search(request: SearchRequest):
    try:
        text = request.text
        with torch.no_grad():
            text_features = model.encode_text(tokenizer([text]))
            query_vector = np.array(text_features)[0]

        hits = client.search(
            collection_name=collection_name, query_vector=query_vector, limit=10
        )
        results = [
            {"id": hit.id, "score": hit.score, "image_path": hit.payload["image_path"]}
            for hit in hits
        ]
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
