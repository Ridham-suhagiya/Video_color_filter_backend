import cv2 as cv
import numpy as np
import time
import os
from helper import form_response
from constants import IMAGE_TYPES, VIDEO_TYPES

class File_Filter:
	def __init__(self,file):
		print(file)
		self.file_path = os.getenv('DOWNLOAD_FILE_FOLDER')
		self.write_file_path = os.getenv('UPLOAD_FILE_FOLDER')
		self.file_type = file.get('file_type')
		self.video_saver = cv.VideoWriter(self.write_file_path, 
	                         cv.VideoWriter_fourcc('m','p','4','v'),
	                         60, file.get('dimensions')[-2::-1])
		self.is_image = 0

	def file_render(self, color):
		try:

			reader_object = self.get_reader_obj()
			while True:
				status, frame = self.get_file_frame(reader_object)
				if not status:
					self.video_saver.release()
					reader_object.release()
					return form_response(200,"File created succesfully and saved")
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
		except Exception as err:
			print(err)
			return form_response(500,err)

	def get_reader_obj(self):
		if self.file_type in IMAGE_TYPES:
			obj =  cv.imread(self.file_path +'.'+  self.file_type)
			self.is_image = 1
		elif self.file_type in VIDEO_TYPES:
			obj =  cv.VideoCapture(self.file_path +'.'+ self.file_type)
			self.is_image = 0
		return obj

	def get_file_frame(self, reader_object):
		if type(reader_object) is np.ndarray:
			return False, reader_object
		return reader_object.read()
			

	

			


