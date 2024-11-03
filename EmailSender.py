import smtplib
import cv2
import time
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class EmailSender:
	def __init__(self):
		self.imgCounter = 0
		self.photoInterval = 10
		self.lastPhotoTime = 0
		
	def send_email(self, to_email, frame):
		currentTime = time.time()
        
		if currentTime - self.lastPhotoTime >= self.photoInterval:	
			from_email = "buysal31@gmail.com"
			password = "tzddwwqwwmsaubku"

			subject = "Suspicious Situtition"
			body = "Suspicious Person was Detected"

			msg = MIMEMultipart()
			msg['From'] = from_email
			msg['To'] = to_email
			msg['Subject'] = subject
			msg.attach(MIMEText(body, 'plain'))
			self.lastPhotoTime = time.time()
			imgName = "/home/ncrxbatu/Desktop/doorobserveproject/temp_image{}.png".format(self.imgCounter)
			self.imgCounter += 1

			if frame is not None:
				 cv2.imwrite(imgName, frame)
			
			if os.path.exists(imgName):
				with open(imgName, "rb") as f:
					image = MIMEImage(f.read(), name="frame.jpg")
					msg.attach(image)

			try:
				server = smtplib.SMTP('smtp.gmail.com', 587)
				server.starttls()
				server.login(from_email, password)
				server.sendmail(from_email, to_email, msg.as_string())
				server.quit()
				print("E-posta başarıyla gönderildi.")
			except Exception as e:
				print("E-posta gönderirken hata oluştu:", str(e))
			
		else:
			print("time out email sender")

		
