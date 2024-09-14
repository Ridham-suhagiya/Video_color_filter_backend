import base64
import cv2 as cv
import os
from constants import IMAGE_TYPES, VIDEO_TYPES

def form_response(resp, body):
	return  {'Status_Code': resp, 'body': body}

def file_saver(file):
	try:

		file_format,file = file.file.split(',')
		file_type = file_format.split('/')[-1].split(';')[0]
		decoded_data = base64.b64decode((file))
		save_file(file_type, decoded_data)
		dimensions = get_dimensions(file_type)
		body = {
		'file_type':file_type,
		'dimensions':dimensions
		}
		return form_response(200,body)
	except Exception as er:
	
		return form_response(500,er)

def save_file(file_type,decoded_data):
	image = open(f'./download_files/file.{file_type}','wb')
	image.write(decoded_data)
	image.close()
		
def get_dimensions(file_type):
	if file_type in IMAGE_TYPES:
		img = cv.imread(f'./download_files/file.{file_type}')
		return img.shape
	else:
		obj = cv.VideoCapture(f'./download_files/file.{file_type}')
		_, frame = obj.read()
		return frame.shape

def create_file_url(resp):
	file_type = resp['body'].get('file_type')
	if file_type in VIDEO_TYPES:
		path  = os.getenv('UPLOAD_FILE_FOLDER') + '.' + 'mp4'
	else:
		path  = os.getenv('UPLOAD_FILE_FOLDER') + '.' + file_type
	with open(path,'rb') as f:
		contents = f.read()
	contents = base64.b64encode(contents).decode('utf-8')
	if file_type in IMAGE_TYPES:
		file_url = f"data:image/{file_type};base64," + contents
	else:
		file_url = "data:video/mp4;base64," + contents
	resp = { "file_bytes": file_url}
	return resp




