import urllib2
import zlib
from Tkinter import *
import webbrowser as wb
import json


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

def get_latest_episodes(url):
	"""
	Returns the name of Latest Episode after parsing the html
	I/p : (String) page url
	O/p : (String) Name of Latest Episode
	"""
	latest_episode = ""
	flag = 2
	page_html = get_page_code(url)
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

def write_to_file():
	"""TEST"""
	data = ["Arrow", "Shield"]
	jsonfile = open('data/seriesname.json','w')
	jsonfile.write(json.dumps(data,indent=4))
	jsonfile.close()
	data = {}
	data['Arrow'] = { 'current' : "arrow 1", 'url' : 'http://next-episode.net/arrow', 'tourl' : 'http://kickass.to/arrow-tv30715/' }
	data['Shield'] = { 'current' : "Shield 1", 'url' : 'http://next-episode.net/marvels-agents-of-s.h.i.e.l.d.', 'tourl' : 'http://kickass.to/marvel-s-agents-of-s-h-i-e-l-d-tv32656/' }
	jsonfile = open('data/seriesdata.json','w')
	jsonfile.write(json.dumps(data,indent=4))
	jsonfile.close()

class SeriesTraker(object):
	"""Initialize tinker window"""

	def __init__(self):
		"""Make skeleton of the application"""
		self.root = Tk()
		self.root.title("Series Tracking Pro")

		self.firstframe = Frame(self.root)
		self.firstframe.pack()

		#populate title frame with titles
		self.titlelabel = Label(self.firstframe,text="Series Names",bg="green")
		self.titlelabel.grid(row=0, column=0)

		#populate current episode list
		self.currenteptitle = Label(self.firstframe,text="Current",bg="green")
		self.currenteptitle.grid(row=0, column=1)

		#populate latest episode list
		self.latesteptitle = Label(self.firstframe,text="Latest",bg="green")
		self.latesteptitle.grid(row=0, column=2)

	def add_series_row(self, ser_obj):
		"""takes an object of series class and creates a row for that series on main window"""
		# set Label for new series
		ser_obj.titlelab = Label( self.firstframe, text = ser_obj.name, bg = "green")
		ser_obj.titlelab.grid( row = ser_obj.num, column = 0 )
		# set current episode label for new series
		ser_obj.currentlab = Label( self.firstframe, text = ser_obj.current, bg = "green")
		ser_obj.currentlab.grid( row = ser_obj.num, column = 1 )

		if ser_obj.is_uptodate:
			ser_obj.latestlab = Label( self.firstframe, text = ser_obj.latest, bg = "green")
			ser_obj.latestlab.grid( row = ser_obj.num, column = 2 )
		else:
			ser_obj.latestlab = Label( self.firstframe, text = ser_obj.latest, bg = "red")
			ser_obj.latestlab.grid( row = ser_obj.num, column = 2 )

		ser_obj.but = Button( self.firstframe, text = "Update " + ser_obj.name, command = ser_obj.update )
		ser_obj.but.grid( row = ser_obj.num, column = 3 )

	def startapp(self):
		self.root.geometry("1000x300+300+300")  #Set starting window size
		self.root.mainloop()        #starts event loop of the program

class Series(object):

	def __init__(self, num, name, data, main_window):
		"""
		num = Integer that decides row number of this series in application
		name = String Name to show as label
		data = This series data read from seriesdata.json file
		main_window = SeriesTraker class object used to insert this series row in main application
		"""
		self.num = num
		self.name = name
		self.current = data.get('current', 'New')
		self.url = data.get('url', None)
		self.latest = get_latest_episodes(self.url).strip()
		self.tourl = data.get('tourl', None)
		self.is_uptodate = self.current == self.latest
		main_window.add_series_row(self)

	def update(self):
		if not self.is_uptodate:
			with open('data/seriesdata.json') as data_file:
				seriesdata = json.load(data_file)
			seriesdata[self.name] = { 'current' : self.latest, 'url' : self.url, 'tourl' : self.tourl }
			jsonfile = open('data/seriesdata.json','w')
			jsonfile.write(json.dumps(seriesdata,indent=4))
			jsonfile.close()
			self.latestlab.config( bg = 'green' )
			wb.open(self.tourl)

if __name__ == '__main__':
	# Get all The names of series user is currently tracking
	with open('data/seriesname.json') as data_file:
		names = json.load(data_file)
	# Get Whole data on those series that we currently have
	with open('data/seriesdata.json') as data_file:
		seriesdata = json.load(data_file)
	# Make primary skeleton of the application
	main_window = SeriesTraker()
	# Add rows as per series that user is following
	series_list = []
	for i, name in enumerate(names):
		series_list.append( Series(i + 1, name, seriesdata[name], main_window) )
	# Function for update All button
	def update_all(series_list):
		for series in series_list:
			series.update()
	#add Buttons to update all content
	bu0 = Button(main_window.firstframe,text="Update all",command = lambda:update_all(series_list) )
	bu0.grid(row=0, column=3)
	# Start the application
	main_window.startapp()

	








