#!/usr/bin/python3

import requests
import queue
import threading
import keyboard
import sys
from tqdm import tqdm
import getopt


x='-d' not in sys.argv
y='--domain' not in sys.argv
if (x and y):
	print('./probe.py -d domainList -t threads')
	sys.exit()

try:
	opts, args=getopt.getopt(sys.argv[1:],'hd:t:o:p',['domain=','threads=','output='])
except getopt.GetoptError:
	print('./probe.py -d domainList -t threads -o output -p')

domain_list=None
threads=10
out_list=None
bar=False
token='1289232303:AAHtYRO_3qPeYOVGQ2pHqCcD7wuzaEJOhOA'
message=[]
chat_id=689790739

for opt,arg in opts:
	if(opt=='-h'):
		print('./probe.py -d domainList -t threads -o output\n-d : File containing domains\n-t : No of threads (Default 10)\n-o : output file name\n-p : progress bar (Default False)')
		sys.exit()
	elif opt in ("-d","--domain"):
		domain_list=arg
	elif opt in ('-t','--threads'):
		threads=int(arg)
	elif opt in ('-o','--output'):
		out_list=arg
	elif(opt=='-p'):
		bar=True



def build_list(domain_file):
	fd=open(domain_file,'r')
	words=queue.Queue()

	for word in fd:
		word=word.rstrip()
		words.put(word)

	fd.close()
	return words


def httprobe(domain_queue):
	i=0
	size=domain_queue.qsize()
	if(out_list):
		out_file=open(out_list,'a+')
	if(bar):
		for z in tqdm(range(size),desc='Progress'):
			i+=1
			progress=float(i/size)*100
			if(keyboard.is_pressed('enter')):
				print("[%d/%d] : %f"%(i,size,progress))
			url=domain_queue.get()
			if 'http' not in url:
				url="https://"+url
			try:
				response = None
				response=requests.get(url,timeout=5)
				if(response.status_code==200 and len(response.content)):
					if(out_list):
						out_file.write("%s\n"%url)
						message.append(url)
					else:
						print(url)
			except Exception:
				pass
	else:
		for z in (range(size)):
			i+=1
			progress=float(i/size)*100
			if(keyboard.is_pressed('enter')):
				print("[%d/%d] : %f"%(i,size,progress))
			url=domain_queue.get()
			if 'http' not in url:
				url="https://"+url
			try:
				response = None
				response=requests.get(url,timeout=5)
				if(response.status_code==200 and len(response.content)):
					if(out_list):
						out_file.write("%s\n"%url)
					else:
						sys.displayhook(url)
			except Exception:
				pass
	if(out_list):
		out_file.close()

w=build_list(domain_list)

try:
	for i in range(threads):
		t=threading.Thread(target=httprobe(w)).start()
except KeyboardInterrupt:
	print('\nEscaped')


for mes in message:
	url=f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mes}"
	res=requests.get(url)