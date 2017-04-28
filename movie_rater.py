from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.font import Font
from PIL import Image, ImageTk, ImageFilter
from tkinter import messagebox
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import sys
import collections.abc

class APP_GUI:
	def __init__(self, master):
		self.master = master
		master.title("Rate your movie")

		self.bold_font = Font(family="Helvetica", size=14, weight="bold")
		self.greet_button = Button(master, text="Open", command=self.rating_finder, height = 1, width = 8,bg="#565674",font=self.bold_font,fg='#ffe')
		#self.greet_button.place(x=40,y=50)
		self.greet_button.pack(side = 'top', padx = 100, pady = 100)
		
	def rating_finder(self):
		self.bold_font_me2 = Font(family="Helvetica", size=12)
		self.label2 = Label(root, text="Sucess",font=self.bold_font_me2,bg="#00b3b3",fg="#00b3b3")
		self.label2.pack(side = 'top', padx = 5, pady = 1)
		inp_exp = askdirectory()
		my_movie = []
		for movie_folder in os.listdir(inp_exp):
			my_movie.append(movie_folder)
		base_url = "http://www.imdb.com"
		for each_movie in my_movie:
			each_movie = each_movie.replace(u'\xa0', ' ')
			each_movie = each_movie.replace(':', ' ')
			movie_name = each_movie
			input_movie_name=""
			for words in movie_name:
				if(words==" "):
					input_movie_name+='%20'
				else:
					input_movie_name+=words
			url_search = base_url + '/find?q='
			url_search+= input_movie_name
			page = urlopen(url_search)
			soup = BeautifulSoup(page,"html.parser")
			
			valid1 = soup.find(id="findSubHeader")
			if(valid1):
				valid2 = valid1.find_all('a')
				movie_details = []
				for i in valid2:
					movie_details.append(i.get_text())
				for i in range(len(movie_details)):
					if(movie_details[i] =="Titles"):
						movie_result = soup.find_all(class_="findList")
						movie_links = movie_result[i].find_all('a')
						movie_link = movie_links[0].get('href')
						page1 = urlopen(base_url+movie_link)
						soup1 = BeautifulSoup(page1,"html.parser")
						if(soup1.find(class_="ratingValue")):
							movie_rating_class = soup1.find(class_="ratingValue")
							movie_rating = movie_rating_class.find("span")
							movie_imdb_rating = movie_rating.get_text()
							
							movie_title = soup1.find(class_="title_wrapper")
							movie_title1 = movie_title.find('h1').get_text()
							movie_title2 = movie_title1.replace(u'\xa0', ' ')
							movie_title2 = movie_title1.replace(':', ' ')
							new_folder_name = movie_title2 + "_IMDB_" + movie_imdb_rating
							os.rename(inp_exp+ "/" +each_movie, inp_exp+"/"+new_folder_name)
		messagebox.showinfo("info", "success")


def center_window(width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

		
root = Tk()
my_gui = APP_GUI(root)
center_window(300, 350)
root.configure(bg='#00b3b3')
root.resizable(width=False, height=False)

f=Frame(root,height=2,width=400,bg="yellow")
f.pack(pady=20,padx=30)

__copyright__ = "Copyright (C) 2017 SS"
bold_font_me1 = Font(family="Helvetica", size=12)
label = Label(root, text=__copyright__,font=bold_font_me1,bg="#00b3b3")
label.pack(pady = 10)
root.mainloop()