from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,HTTPException
from models import File as file
from helper import file_saver
from create_edit_file.filter_file import File_Filter

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

@app.post("/")
async def download_file(file:file):
    resp = file_saver(file)
    if resp['Status_Code'] == 500:
        raise HTTPException(status_code=resp["Status_Code"], detail=resp['body'])
    file_obj = File_Filter(resp['body'])    
    resp = file_obj.file_render("green")
    if resp['Status_Code'] == 500:  
        raise HTTPException(status_code=resp["Status_Code"], detail=resp['body'])

    return resp