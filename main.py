# install pillow, beautifulsoup4tifulsoup4 in python
# install ffmpeg on os and add to PATH
from PIL import Image, ImageSequence
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import urllib.request,io
import xml.etree.ElementTree as etree
import os
import socket
import subprocess as sp
import shutil

i = 0

FFMPEG_PATH = "ffmpeg.exe"

socket.setdefaulttimeout(10)

def saveimg(url):
	extension = url.split('.')[-1];
	print(extension)
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

def callffmpeg():
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
			cmd = "ffmpeg -i temp/" + file + " -vf scale=320:240 temp/" + fname + ".png"
			print(cmd)
			sp.call(cmd);
	
	cmd = 'ffmpeg -framerate 1 -start_number 0 -i "temp/%0d.png" -vf scale=720x406 -vcodec mpeg4 -y movie.mp4'
	
	print(cmd)
	sp.call(cmd);

# open bbc news feed
tree = etree.parse(urllib.request.urlopen("http://feeds.bbci.co.uk/news/rss.xml?edition=int"));
root = tree.getroot()
#for num in range(9, 68):
for num in range(9, 10):
	if not os.path.exists('temp'):
		os.mkdir('temp')
	vtitle = root[0][num][0].text # title
	vdesc = root[0][num][1].text # description
	vurl = root[0][num][2].text # url
	print(vtitle)
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
			saveimg(img["src"])
	for div in divs:
		if div.has_attr('data-src'):
			saveimg(div["data-src"])
		
	# images saved - put in array
	callffmpeg();
	#  clear temp folder
	shutil.rmtree('./temp')


imageurl = "https://i.ytimg.com/vi_webp/XnnwYk4qq70/mqdefault.webp"
image = path = io.BytesIO(urllib.request.urlopen(imageurl).read())
im = Image.open(image)
#im.rotate(45).show()