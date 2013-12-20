import urllib2
#import zlib
from Tkinter import *

no_of_series = 5
current_episodes = ["","","","",""] # arrow , Shield , bbt , atlantis , himym
latest_episodes = ["","","","",""]
files = ["arrow.txt","Shield.txt","bbt.txt","atlantis.txt","himym.txt"]

def get_page_code(page):
	url = urllib2.urlopen(page)   #get a page manipulatable object
	page_html = url.read()        #read page's HTML content and save it as a string
	url.close()                   #close the file after reading from the object
	#must add a branching so that only gzip encoded pages get through decompression
	#page_decompressed=zlib.decompress(page_html,16+zlib.MAX_WBITS) #decodes the gzip encoded HTML string
	return page_html

def get_latest_episodes(page):
	latest_episode = ""
	flag = 2
	page_html = get_page_code(page)
	page_html = page_html[page_html.find("Latest Episode"):] #trim the input code
	#get only name of latest episode
	for char in page_html:
		if flag == 0:
			if char == "<":
				break
			else:
				latest_episode = latest_episode + char
		if char == ">":
			flag = flag - 1
	return latest_episode

def read_current_episodes():
	for i in range(no_of_series):
		f=open(files[i],'r')
		current_episodes[i]=f.readline().strip()
		f.close()

def store_latest_episodes(urls):
	for i in range(no_of_series):
		latest_episodes[i]=get_latest_episodes(urls[i]).strip()

def write_latest_episodes(file_index):
	if file_index != -1:
		f=open(files[file_index],'w')
		f.write(latest_episodes[file_index])
		f.close()
	else:
		for i in range(no_of_series):
			f=open(files[i],'w')
			f.write(latest_episodes[file_index])
			f.close()
	if file_index == 0:
		lat0.config(bg='orange')
	elif file_index == 1:
		lat1.config(bg='orange')
	elif file_index == 2:
		lat2.config(bg='orange')
	elif file_index == 3:
		lat3.config(bg='orange')
	elif file_index == 4:
		lat4.config(bg='orange')
	else:
		lat0.config(bg='orange')
		lat1.config(bg='orange')
		lat2.config(bg='orange')
		lat3.config(bg='orange')
		lat4.config(bg='orange')


if __name__ == '__main__':
	page_himym = "http://www.watchseries.to/serie/how_i_met_your_mother"
	page_arrow = "http://www.watchseries.to/serie/arrow"
	page_shield = "http://www.watchseries.to/serie/Agents_of_S_H_I_E_L_D"
	page_bbt = "http://www.watchseries.to/serie/big_bang_theory"
	page_atlantis = "http://www.watchseries.to/serie/atlantis_2013"
	#list of all urls
	page_urls = [page_arrow,page_shield,page_bbt,page_atlantis,page_himym]

	read_current_episodes()           #get current episode list
	store_latest_episodes(page_urls)  #get latest episode list

	root = Tk()
	root.title("Get Series")

	firstframe = Frame(root)
	firstframe.pack()
	#pack 3 frames on main root frame and last frame for buttons
	titleframe = Frame(firstframe)
	titleframe.pack(side=LEFT)
	currentframe = Frame(firstframe)
	currentframe.pack(side=LEFT)
	latestframe = Frame(firstframe)
	latestframe.pack(side=LEFT)
	buframe = Frame(firstframe)
	buframe.pack(side=LEFT)

	#populate title frame with titles
	emptylable = Label(titleframe,text="",bg="aqua")
	emptylable.pack(fill=X,expand=1)
	arrowlable = Label(titleframe,text="Arrow :",bg="aqua")
	arrowlable.pack(fill=X,expand=1)
	shieldlable = Label(titleframe,text="S.H.I.E.L.D :",bg="aqua")
	shieldlable.pack(fill=X,expand=1)
	bbtlable = Label(titleframe,text="Big Bang Theory :",bg="aqua")
	bbtlable.pack(fill=X,expand=1)
	atlantislable = Label(titleframe,text="Atlantis :",bg="aqua")
	atlantislable.pack(fill=X,expand=1)
	himymlable = Label(titleframe,text="How I Met Your Mother :",bg="aqua")
	himymlable.pack(fill=X,expand=1)

	#populate current episode list
	titlelabel = Label(currentframe,text="Current",bg="aqua")
	titlelabel.pack(fill=X,expand=1)
	lab0 = Label(currentframe,text=current_episodes[0],bg="yellow")
	lab0.pack(fill=X,expand=1)
	lab1 = Label(currentframe,text=current_episodes[1],bg="yellow")
	lab1.pack(fill=X,expand=1)
	lab2 = Label(currentframe,text=current_episodes[2],bg="yellow")
	lab2.pack(fill=X,expand=1)
	lab3 = Label(currentframe,text=current_episodes[3],bg="yellow")
	lab3.pack(fill=X,expand=1)
	lab4 = Label(currentframe,text=current_episodes[4],bg="yellow")
	lab4.pack(fill=X,expand=1)

	#populate latest episode list
	latlabel = Label(latestframe,text="Latest",bg="aqua")
	latlabel.pack(fill=X,expand=1)
	lat0 = Label(latestframe,text=latest_episodes[0],bg='orange')
	lat0.pack(fill=X,expand=1)
	lat1 = Label(latestframe,text=latest_episodes[1],bg='orange')
	lat1.pack(fill=X,expand=1)
	lat2 = Label(latestframe,text=latest_episodes[2],bg='orange')
	lat2.pack(fill=X,expand=1)
	lat3 = Label(latestframe,text=latest_episodes[3],bg='orange')
	lat3.pack(fill=X,expand=1)
	lat4 = Label(latestframe,text=latest_episodes[4],bg='orange')
	lat4.pack(fill=X,expand=1)

	latest_list=[lat0,lat1,lat2,lat3,lat4]

	for i in range(no_of_series):
		if current_episodes[i].strip() != latest_episodes[i].strip():
			latest_list[i].config(bg='red')

	#add Buttons to update content
	bu0 = Button(buframe,text="Update all",command=lambda:write_latest_episodes(-1))
	bu0.pack(fill=X,expand=1)
	bu1 = Button(buframe,text="arrow +",command=lambda:write_latest_episodes(0))
	bu1.pack(fill=X,expand=1)
	bu2 = Button(buframe,text="Shield +",command=lambda:write_latest_episodes(1))
	bu2.pack(fill=X,expand=1)
	bu3 = Button(buframe,text="BBT +",command=lambda:write_latest_episodes(2))
	bu3.pack(fill=X,expand=1)
	bu4 = Button(buframe,text="Atlantis +",command=lambda:write_latest_episodes(3))
	bu4.pack(fill=X,expand=1)
	bu5 = Button(buframe,text="himym +",command=lambda:write_latest_episodes(4))
	bu5.pack(fill=X,expand=1)

	root.geometry("1000x209+300+300")  #Set starting window size
	root.mainloop()        #starts event loop of the program
	#root.destroy()




