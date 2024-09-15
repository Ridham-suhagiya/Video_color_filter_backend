from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,HTTPException
from models import File as file
from helper import file_saver, create_file_url
from create_edit_file.filter_file import File_Filter
import json
from starlette.responses import StreamingResponse
import os
from constants import IMAGE_TYPES
from fastapi.staticfiles import StaticFiles



app = FastAPI()


origins = [
    "http://localhost:3000",
    "*"
]
PUBLIC_DIR = os.getenv("UPLOAD_FILE_FOLDER")
app.mount("/static", StaticFiles( directory = PUBLIC_DIR), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/health')
async def health(): 
    return {"status": 200}

@app.post("/")
async def download_file(file:file):
    resp = file_saver(file)
    if resp['Status_Code'] == 500:
        raise HTTPException(status_code=resp["Status_Code"], detail=resp['body'])
    file_obj = File_Filter(resp['body'])    
    file_status = file_obj.file_render(file.color.strip())
    if file_status['Status_Code'] == 500:  
        raise HTTPException(status_code=resp["Status_Code"], detail=resp['body'])
    # url_object = create_file_url(resp)
    file_type = resp['body'].get('file_type')
    if file_type in IMAGE_TYPES:
        path  = os.getenv('UPLOAD_FILE_FOLDER') + 'output' + '.' + file_type
        image = open(path, 'rb')
        return {'file':'image' , 'file_type': file_type}
    path  = os.getenv('UPLOAD_FILE_FOLDER') + 'output' + '.' + 'mp4'
    video = open(path, 'rb')
    return {'file':'video'}