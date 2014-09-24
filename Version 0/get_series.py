import urllib2
import zlib
from Tkinter import *
import webbrowser as wb

no_of_series = 8
current_episodes = ["","","","","","","",""] # arrow , Shield , bbt , atlantis , GOT , Svally , Davinci
latest_episodes = ["","","","","","","",""]
files = ["arrow.txt","Shield.txt","bbt.txt","atlantis.txt","himym.txt","walkingdead.txt","svally.txt","davinci.txt"]

def get_page_code(page):
	"""
	Get page object and decode if needed to get string HTML file
	I/p : (String) page url
	O/p : (String) page HTML
	"""
	url = urllib2.urlopen(page)   #get a page manipulatable object
	page_html = url.read()        #read page's HTML content and save it as a string
	page_info = url.info()
	url.close()                   #close the file after reading from the object
	#only gzip encoded pages get through decompression
	if 'gzip' in page_info.values():
		page_decompressed=zlib.decompress(page_html,16+zlib.MAX_WBITS) #decodes the gzip encoded HTML string
		return page_decompressed
	return page_html

def get_latest_episodes(page):
	"""
	Returns the name of Latest Episode after parsing the html
	I/p : (String) page url
	O/p : (String) Name of Latest Episode
	"""
	latest_episode = ""
	flag = 2
	page_html = get_page_code(page)
	page_html = page_html[page_html.find("<h3>Name:</h3>")+25:] #trim the input code
	#get only name of latest episode
	for char in page_html:
		if char == "<":
			break
		if flag == 1:
			latest_episode = latest_episode + char
		if char == ">":
			flag = flag - 1

	flag = 2
	page_html = page_html[page_html.find("Episode:</div>")+15:]
	#get only number of latest episode
	num = ""
	for char in page_html:
		if char == "<":
			break
		if flag == 1:
			num = num + char
		if char == ">":
			flag = flag - 1
	return num + ' ' + latest_episode

def read_current_episodes():
	"""
	Reads From file and stores current episode data to list
	"""
	for i in range(no_of_series):
		try:
			#file exists
			f=open(files[i],'r')
			current_episodes[i]=f.readline().strip()
		except Exception, e:
			#file does not exist
			f=open(files[i],'a')
			f.write("New Season Tracking")
			current_episodes[i] = "New Season Tracking"
		f.close()

def store_latest_episodes(urls):
	"""
	Go to each URL and get list of latest episodes in list
	I/p : List of urls to query
	"""
	for i in range(no_of_series):
		latest_episodes[i]=get_latest_episodes(urls[i]).strip()

def write_latest_episodes(file_index):
	"""
	Updates Index episode in file
	I/p : Index which episode to update
	"""
	if file_index != -1:
		f=open(files[file_index],'w')
		f.write(latest_episodes[file_index])
		f.close()
	else:
		for i in range(no_of_series):
			f=open(files[i],'w')
			f.write(latest_episodes[i])
			f.close()
	if file_index == 0:
		lat0.config(bg='orange')
		wb.open('http://kickass.to/arrow-tv30715/')
	elif file_index == 1:
		lat1.config(bg='orange')
		wb.open('http://kickass.to/marvel-s-agents-of-s-h-i-e-l-d-tv32656/')
	elif file_index == 2:
		lat2.config(bg='orange')
		wb.open('http://kickass.to/the-big-bang-theory-tv8511/')
	elif file_index == 3:
		lat3.config(bg='orange')
		wb.open('http://kickass.to/atlantis-2013-tv36869/')
	elif file_index == 4:
		lat4.config(bg='orange')
		wb.open('http://kickass.to/game-of-thrones-tv24493/')
	elif file_index == 5:
		lat5.config(bg='orange')
		wb.open('http://kickass.to/the-walking-dead-tv25056/')
	elif file_index == 6:
		lat6.config(bg='orange')
		wb.open('http://kickass.to/silicon-valley-tv33759/')
	elif file_index == 7:
		lat7.config(bg='orange')
		wb.open('http://kickass.to/da-vinci-s-demons-tv32724/')
	else:
		lat0.config(bg='orange')
		lat1.config(bg='orange')
		lat2.config(bg='orange')
		lat3.config(bg='orange')
		lat4.config(bg='orange')
		lat5.config(bg='orange')
		lat6.config(bg='orange')
		lat7.config(bg='orange')

if __name__ == '__main__':
	page_got = "http://next-episode.net/game-of-thrones"   #Game of thrones
	page_arrow = "http://next-episode.net/arrow"
	page_shield = "http://next-episode.net/marvels-agents-of-s.h.i.e.l.d."
	page_bbt = "http://next-episode.net/the-big-bang-theory"
	page_atlantis = "http://next-episode.net/atlantis-2013"
	page_wd = "http://next-episode.net/the-walking-dead"
	page_svally = "http://next-episode.net/silicon-valley"
	page_davinci = "http://next-episode.net/da-vincis-demons"
	#list of all urls
	page_urls = [page_arrow,page_shield,page_bbt,page_atlantis,page_got,page_wd,page_svally,page_davinci]

	read_current_episodes()           #get current episode list
	store_latest_episodes(page_urls)  #get latest episode list

	root = Tk()
	root.title("Get Series Updates")

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
	emptylable = Label(titleframe,text="",bg="green")
	emptylable.pack(fill=X,expand=1)
	arrowlable = Label(titleframe,text="Arrow :",bg="green")
	arrowlable.pack(fill=X,expand=1)
	shieldlable = Label(titleframe,text="S.H.I.E.L.D :",bg="green")
	shieldlable.pack(fill=X,expand=1)
	bbtlable = Label(titleframe,text="Big Bang Theory :",bg="green")
	bbtlable.pack(fill=X,expand=1)
	atlantislable = Label(titleframe,text="Atlantis :",bg="green")
	atlantislable.pack(fill=X,expand=1)
	himymlable = Label(titleframe,text="Game Of Thrones :",bg="green")
	himymlable.pack(fill=X,expand=1)
	wdlable = Label(titleframe,text="Walking Dead :",bg="green")
	wdlable.pack(fill=X,expand=1)
	svlable = Label(titleframe,text="Silicon Valley",bg="green")
	svlable.pack(fill=X,expand=1)
	dvlable = Label(titleframe,text="Davinci's Deamons",bg="green")
	dvlable.pack(fill=X,expand=1)

	#populate current episode list
	titlelabel = Label(currentframe,text="Current",bg="green")
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
	lab5 = Label(currentframe,text=current_episodes[5],bg="yellow")
	lab5.pack(fill=X,expand=1)
	lab6 = Label(currentframe,text=current_episodes[6],bg="yellow")
	lab6.pack(fill=X,expand=1)
	lab7 = Label(currentframe,text=current_episodes[7],bg="yellow")
	lab7.pack(fill=X,expand=1)

	#populate latest episode list
	latlabel = Label(latestframe,text="Latest",bg="green")
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
	lat5 = Label(latestframe,text=latest_episodes[5],bg='orange')
	lat5.pack(fill=X,expand=1)
	lat6 = Label(latestframe,text=latest_episodes[6],bg='orange')
	lat6.pack(fill=X,expand=1)
	lat7 = Label(latestframe,text=latest_episodes[7],bg='orange')
	lat7.pack(fill=X,expand=1)

	latest_list=[lat0,lat1,lat2,lat3,lat4,lat5,lat6,lat7]

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
	bu5 = Button(buframe,text="GOT +",command=lambda:write_latest_episodes(4))
	bu5.pack(fill=X,expand=1)
	bu6 = Button(buframe,text="WD +",command=lambda:write_latest_episodes(5))
	bu6.pack(fill=X,expand=1)
	bu7 = Button(buframe,text="SV +",command=lambda:write_latest_episodes(6))
	bu7.pack(fill=X,expand=1)
	bu8 = Button(buframe,text="DV's D +",command=lambda:write_latest_episodes(7))
	bu8.pack(fill=X,expand=1)

	root.geometry("1000x300+300+300")  #Set starting window size
	root.mainloop()        #starts event loop of the program
	#root.destroy()



