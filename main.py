# install pillow, beautifulsoup4, google-api-python-client in python
# install ffmpeg on os and add to PATH and have PYTHON in path
from PIL import Image, ImageSequence
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import urllib.request,io
import xml.etree.ElementTree as etree
import os
import socket
import subprocess as sp
import shutil
import re, string
import time

i = 0 # picture number

socket.setdefaulttimeout(10)

def UploadYouTubeVid(title, description, path):
	title = re.sub(r'([^\s\w]|_)+', '', title)
	description = re.sub(r'([^\s\w]|_)+', '', description)
	print(description)
	cmd = "python ytupload.py "
	cmd += '--file "' + path + '" '
	cmd += '--title "' + title + '" '
	cmd += '--description "' + description + '" '
	try:
		sp.call(cmd);
	except:
		pass

def SaveImg(url):
	extension = url.split('.')[-1];
	#print(extension)
	try:
		dest = "temp/" + str(i) + "." + extension;
		if extension != 'png' and extension != 'jpeg' and extension != 'jpg':
			dest = "del/temp"
		urllib.request.urlretrieve(url, dest);
		
		if dest != "del/temp":
			global i
			i +=1
	except:
		pass

def CallFfmpeg():
	# get files in dir
	files = os.listdir("temp")
	#cmd = "ffmpeg -f image2 -r 1/5 -i "
	#for file in files:
	#	extension = file.split('.')[-1]
	#	if extension != 'png' and extension != 'jpeg' and extension != 'jpg':
	#		continue
	#	cmd += "temp/" + file + " "
	#cmd += "-vcodec mpeg4 -y movie.mp4"
	
	
	for file in files:
		extension = file.split('.')[-1]
		fname = file.split('.')[0]
		if extension != "png":
			cmd = "ffmpeg -i temp/" + file + " -vf scale=320:240 temp/" + fname + ".png" #convert to png
			#print(cmd)
			sp.call(cmd);
	
	cmd = 'ffmpeg -framerate 1 -start_number 0 -i "temp/%0d.png" -vf scale=720x406 -vcodec mpeg4 -y movie.mp4'
	
	#print(cmd)
	sp.call(cmd);

# get settings
settings = etree.parse("settings.xml")
settings = settings.getroot()
#print(settings[0][0].text)
	
# open bbc news feed
while True:
	feed = etree.parse(urllib.request.urlopen("http://feeds.bbci.co.uk/news/rss.xml?edition=int"));
	feed = feed.getroot()
	for num in range(9, 68):
	#for num in range(9, 10):
		if not os.path.exists('temp'):
			os.mkdir('temp')
		vtitle = feed[0][num][0].text # title
		vdesc = feed[0][num][1].text # description
		vurl = feed[0][num][2].text # url
		if num == 9:
			# first
			f = open('lastupload.txt', "r")
			s = f.read()
			print(s)
			if s == vurl:
				break
			else:
				f = open('lastupload.txt', "w")
				f.write(vurl)
		#print(feed)
		# open link
		response = urllib.request.urlopen(vurl)
		html = response.read()
		html = html.decode("utf-8") 
		# parse html for images
		soup = BeautifulSoup(html, "html.parser")
		imgs = soup.findAll("img")
		divs = soup.findAll("div")
		for img in imgs:
			if img.has_attr('src'):
				SaveImg(img["src"])
		for div in divs:
			if div.has_attr('data-src'):
				SaveImg(div["data-src"])
			
		# images saved - put in array
		CallFfmpeg();
		#  clear temp folder
		shutil.rmtree('./temp')
		UploadYouTubeVid(vtitle, vdesc, "movie.mp4")
		global i
		i = 0
	time.sleep(1020)

#im.rotate(45).show()