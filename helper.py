import base64
import cv2 as cv


def form_response(resp, body):
	return  {'Status_Code': resp, 'body': body}




def file_saver(file):
	try:
		print(file.file[:40])
		file_format,file = file.file.split(',')
		file_type = file_format.split('/')[-1].split(';')[0]
		decoded_data = base64.b64decode((file))
		image = open(f'./download_files/file.{file_type}','wb')
		image.write(decoded_data)
		image.close()
		return form_response(200,file_type)
	except Exception as er:
		print(er)
		return form_response(500,er)



