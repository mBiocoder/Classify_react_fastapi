# backend/main.py (FastAPI Backend)
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
import tensorflow as tf
import numpy as np
from PIL import Image
from starlette.responses import JSONResponse

app = FastAPI()

# Enable CORS to allow requests from your React frontend
origins = ["http://localhost:3000", "http://localhost", "http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the pre-trained MobileNetV2 model
model = tf.keras.applications.MobileNetV2(weights="imagenet")

# Function to preprocess and classify the uploaded image
def classify_image(image_data):
    img = Image.open(BytesIO(image_data))
    img = img.resize((224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    predictions = model.predict(img)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions)
    return decoded_predictions[0][0][1]

@app.post("/classify/")
async def classify_uploaded_image(file: UploadFile):
    try:
        image_data = await file.read()
        result = classify_image(image_data)
        return JSONResponse(content={"classification": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
