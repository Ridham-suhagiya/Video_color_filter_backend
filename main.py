from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,UploadFile,Request,File
from pydantic import BaseModel
import cv2 as cv
import base64
import requests
from PIL import Image
import numpy as np

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:*",
    "http://localhost:3000",
]

app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=['*'],
allow_headers=['*']
)


class Item(BaseModel):
    file : str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/")
async def create_upload_file(item:Item):
    img = item.file.split(',')[-1]
    decoded_data=base64.b64decode((img))
    image = open('image.png','wb')
    image.write(decoded_data)
    return None