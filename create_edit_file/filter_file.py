import cv2 as cv
import numpy as np
import time
import os
from helper import form_response

class File_Filter:
	def __init__(self,file_type):
		self.file_path = os.getenv('DOWNLOAD_FILE_FOLDER')
		self.write_file_path = os.getenv('UPLOAD_FILE_FOLDER')
		self.file_type = file_type
		self.video_saver = cv.VideoWriter(self.file_path + '.'+ 'MP4', 
	                         cv.VideoWriter_fourcc('m', 'p', '4', 'v'),
	                         60, (300,300) ,isColor = True)
		self.is_image = 0

	def file_render(self, color):
		try:
			status = True
			while status:
				if self.file_type in ['jpeg','png','jpg']:
					status = False
					frame = cv.imread(self.file_path +'.'+  self.file_type)
					self.is_image = 1
				else:
					vid = cv.VideoCapture(self.file_path +'.'+ self.file_type)
					status, frame= vid.read()
				b,g,r = cv.split(frame)
				max_pixel = np.max(frame,axis = 2)
				max_pixel_image = cv.merge([max_pixel, max_pixel, max_pixel])
				red = cv.merge([r,r,r])
				blue = cv.merge([b,b,b])
				green = cv.merge([g,g,g])

				if color == 'red':
					frame = np.where(red > blue, frame, max_pixel_image)
					frame = np.where(red > green , frame, max_pixel_image)
				elif color == 'green':
					frame = np.where(green > blue, frame, max_pixel_image)
					frame = np.where(green > red, frame, max_pixel_image)
				else:
					frame = np.where(blue > red, frame, max_pixel_image)
					frame = np.where(blue > green , frame, max_pixel_image)
				if self.is_image:
					cv.imwrite( self.write_file_path + '.' + self.file_type , frame)
				else:
					self.video_saver.write(frame)
			return form_response(200,"File created succesfully and saved")
		except Exception as err:
			print(err)
			return form_response(500,err)
			 


