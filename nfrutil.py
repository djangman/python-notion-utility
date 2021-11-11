import tkinter as tk
from tkinter import ttk, font
from tkinter import messagebox
from pathlib import PureWindowsPath, PurePosixPath
import sys
import requests
import json
import os
from dotenv import load_dotenv
import time
from tooltip import CreateToolTip
platform = "win"

if platform == "win":
	from winGuiXYPositions import \
	buttonX, buttonY, buttonFont, titleX, titleY, titleFont, leftLabelFontSize, buttonFontSize
else:
	from macGuiXYPositions import \
	buttonX, buttonY, buttonFont, titleX, titleY, titleFont, leftLabelFontSize, buttonFontSize

NOTION_TOKEN = ""
NOTION_DATABASE_ID = ""

class Application(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.initialize()

		self.payload = {
			"note": '',
			"filepath": ''
		}
		self.retrieve_file_or_folderpath()
		self.clicked = tk.StringVar()
		self.master.resizable(False, False)
		self.master.title('NFRUtil')
		self.initGui() # create main window, and center it
		self.retrieve_database_select_items()
		self.create_widgets()
		
	def initGui(self):
		app_width = 456
		app_height = 250
		screen_width = self.master.winfo_screenwidth()
		screen_height = self.master.winfo_screenheight()
		x = (screen_width / 2) - (app_width / 2)
		y = (screen_height / 2) - (app_height / 2)
		self.master.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
		self.master.iconbitmap("nfr.ico")

	def expand_user_display(self, mode, message, detail):
		if mode == "error":
			fgcolor="white"
			bgcolor="darkblue"
			strTitle = "A minor hiccup .. but we'll resolve it"
		else:
			fgcolor="blue"
			bgcolor="lightgreen"
			strTitle = "Successful Update to Notion"

		self.master.geometry("456x414")
		
		self.canvas=tk.Canvas(self.master, width=417, height=150,  bg=bgcolor)
		self.canvas.place(x=17, y=245)
		
		# Message Title
		errorHeaderFont = font.Font(family='TkIconFont', size="16", weight="bold")
		self.currentHeaderText = strTitle
		self.errorTitle = tk.Label(self.master, text=self.currentHeaderText, font=errorHeaderFont, fg=fgcolor, bg=bgcolor)
		self.errorTitle.place(x=19, y=250)

		# Error Message body
		errorBodyFont = font.Font(family='Verdana', size="12")
		if mode == "error":
			generalMessageFont = font.Font(family='Verdana', size="14")
			detailMessageFont = font.Font(family='Verdana', size="18")
			smallDetailMessageFont = font.Font(family='Verdana', size="12")
			detailStrWidth = smallDetailMessageFont.measure(detail)
			
			self.messageText = tk.Label(self.master, text=message, font=errorBodyFont, fg=fgcolor, bg=bgcolor)
			self.messageText.place(x=22, y=280)

			if detailStrWidth > 200:
				detailTextArray = self.generateTwoPartText(detail)
				self.errorDetails = tk.Label(self.master, text=detailTextArray[0], font=smallDetailMessageFont, fg="yellow", bg=bgcolor)
				self.errorDetails.place(x=45, y=301)
				if len(detailTextArray) > 1:
					self.errorDetails2 = tk.Label(self.master, text=detailTextArray[1], font=smallDetailMessageFont, fg="yellow", bg=bgcolor)
					self.errorDetails2.place(x=45, y=320)
			else:
				self.errorDetails = tk.Label(self.master, text=detail, font=detailMessageFont, fg="yellow", bg=bgcolor)
				self.errorDetails.place(x=45, y=301)

			self.generalMessage = tk.Label(self.master, text="If you haven't yet, check .env file", font=generalMessageFont, fg=fgcolor, bg=bgcolor)
			self.generalMessage.place(x=19, y=353)
			
		else:
			messageBodyFont = font.Font(family='Verdana', size="13")
			self.errorBody = tk.Label(self.master, text=message, font=messageBodyFont, fg=fgcolor, bg=bgcolor)
			self.errorBody.place(x=19, y=290)

	def generateTwoPartText(self, detailText):
		tempCharArray = detailText.split(":")
		return tempCharArray

	def retrieve_file_or_folderpath(self):
		strPath = sys.argv[1]
		fontForWidthCalc = font.Font(size=12)
		strWidth = fontForWidthCalc.measure(strPath)
		self.payload['filepath'] = strPath
		if strWidth > 230:
			self.displayPath = self.generateTruncatedPath( strPath )
		else:
			self.displayPath = strPath
		
	def generateTruncatedPath(self, strPath):
		if platform == "win":
			partsList = PureWindowsPath(strPath).parts
		else:
			partsList = PurePosixPath(strPath).parts
		numParts = len(partsList)
		finalPathText = partsList[0] + partsList[1] + "...." + partsList[numParts - 1]
		return finalPathText

	def retrieve_database_select_items(self):
		# The actual API request
		global NOTION_DATABASE_ID
		global NOTION_TOKEN
		response = requests.get('https://api.notion.com/v1/databases/'+NOTION_DATABASE_ID, headers={
								'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})
		self.optionsLst = []
		
		#Parse the response as JSON
		data = response.json()
		if not "properties" in data:
			self.expand_user_display("error", "Please note error message below:", data['message'] )
			self.appErrorState = 1
			return
	
		str_options = data['properties']['Note']['select']['options']
		for option in str_options:
			self.optionsLst.append(option['name'])
		self.clicked.set(self.optionsLst[0])
	
	def create_widgets(self):
		

		# Display Canvas
		# ---------------------------------------------------------------
		self.canvas=tk.Canvas(self.master, width=417, height=221,  bg='lightblue')
		self.canvas.place(x=17, y=12)

		# Display Top Title
		# ---------------------------------------------------------------
		myFont = font.Font(family='Arial', size="23", weight="bold")
		self.title = tk.Label(self.master,text="Add Reminder/Note", font=myFont, bg='lightblue', fg="darkblue")
		self.title.place(x=titleX, y=titleY)
		self.separator = ttk.Separator(self.master, orient='horizontal')
		self.separator.place(x=titleX-30, y=titleY+45, relwidth=.75, relheight=.015 )
		
		# Display Left Label for Path/Filename
		# ---------------------------------------------------------------
		self.pathlabel = tk.Label(self.master,text="Path/Filename:", font=('Helvetica', leftLabelFontSize,'bold'), bg='lightblue')
		self.pathlabel.place(x=38, y=90)

		# Display Info for Path/Filename
		# ---------------------------------------------------------------
		self.textLabel = tk.Label(self.master, text=" ", font="14", width=28)
		self.textLabel.place(x=160,y=90)
		
		self.pathvalue = tk.Label(self.master,text=self.displayPath, font="12", fg="red")
		self.pathvalue.place(x=165,y=90)
		label_ttp = CreateToolTip(self.pathvalue, self.payload['filepath'])
		
		# Display Left Label for Note:
		# ---------------------------------------------------------------
		self.notelabel = tk.Label(self.master,text="Note:", font=('Helvetica', leftLabelFontSize,'bold'), bg='lightblue')
		self.notelabel.place(x=38, y=120)

		# Display Dropdown for Note:
		# ---------------------------------------------------------------
		if len(self.optionsLst):
			self.dropdown = tk.OptionMenu(self.master, self.clicked, *self.optionsLst, command=lambda _: self.update_payload())
			self.dropdown.place(x=160, y=120)
			self.payload['note'] = self.clicked.get()
		else:
			self.emptyListText = tk.Label(self.master,text="Your Database Select options \n were not found", font=('Helvetica', leftLabelFontSize,'bold'), bg='lightblue')
			self.emptyListText.place(x=160, y=120)

		# Display Submit Button
		# ---------------------------------------------------------------
		myFont = font.Font(family='TkHeadingFont', size="14")

		ttk.Style().configure("TButton", padding=6, relief="flat", font=('Tahoma', buttonFontSize))
		if len(self.optionsLst):
			buttonText = "Submit Record To Notion"
		else:
			buttonText = "         Close NFRUtil           "
		self.submitButton = ttk.Button(text=buttonText, command=self.create_row)
		self.submitButton.place(x=buttonX, y=buttonY)
	
	def update_payload(self):
		self.payload['note'] = self.clicked.get()
	
	def resource_path(self,relative_path):
		if hasattr(sys, '_MEIPASS'):
			return os.path.join(sys._MEIPASS, relative_path)
		return os.path.join(os.path.abspath("."), relative_path)
		
	def create_row(self):
		if self.appErrorState:
			sys.exit()
		
		payloadObj = {
			'parent': {'database_id': NOTION_DATABASE_ID},
			'properties': {  # These are our columns
				# Read the documentation to see what values you can use, I can't explain it better:)
				# https://developers.notion.com/reference/page#property-value-object
				'FolderOrFilePath': {
					'title': [
						{
							'text': {'content': self.payload['filepath']}
						}
					]
				},
				'Note': {
					'select': {'name': self.payload['note']}
				}
			}
		}

		# The actual API request
		response = requests.post('https://api.notion.com/v1/pages/', json=payloadObj, headers={
			'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})
		self.submitButton['text'] = "         Close NFRUtil           "

		# Parse response as JSON and return
		data = response.json()
		if not "id" in data:
			self.expand_user_display("error", 'Please Note Error Below', data['message'])
			return

		self.expand_user_display("success", "Id of your new record ( page ): \n" + data['id'], "")
		self.appErrorState = 2

	def initialize(self):
		global NOTION_DATABASE_ID, NOTION_TOKEN
		self.appErrorState = 0       # 1 is error state, 0 is normal state, 2 means: Just saved to notion, so ready to close
		os.chdir(sys.argv[2])
		load_dotenv()
		NOTION_TOKEN = os.getenv('NOTION_SECRET')
		NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
		self.currentHeaderText = ""
		self.displayPath = ""
		

root = tk.Tk()
app = Application(master=root)
app.mainloop()
