# NFRUtil ( abbreviation of Notion File Reminder Utility )
A cross-compatible Desktop app that allows a right click on a file in Finder/Windows Explorer and send the pathname and a note, to your Notion database

## Why
Sometimes I download random files - such as a meditation mp3, or a free pdf someone offers through their website, of a VueJs manual or similar.  Even if i keep my Windows file system organized and keep things in order, I still may forget that the file is there, ( because I get too file-happy and download too much )

So I wanted an easy way to quickly add the full pathname of the file to my Notion database.

( But I also wanted an excuse to code in Python - the last time for me previously was in 2010 when I created a Django site )


## A video summarizing how it works


https://user-images.githubusercontent.com/292466/141028752-92e11623-547f-426e-8571-76388c7e40a7.mp4

## Requirements

Python 3.*


## To set up

#### Configure env file

* Create a Notion Integration ( if you google, there is a plentitude of articles and youtube vids )

  * The Integration Key will be the NOTION_SECRET as specified below

* Get the id for the database that you want to use for this app.

* Rename .env-example to .env and fill in the values for keys: 
     ````NOTION_SECRET````
     ````NOTION_DATABASE_ID````

#### Set variable to "win" or "mac" depending on your operation system

 * In nfrutil.py:

     Line 12:  platform = "mac"
    
#### In order to have the app working as a right-click context menu option, there is a necessary list of steps
 ##### Windows
  * Search google for using Windows registry, for adding an app to the context menu
    * The path of the app would of course be the full path of nfrutil.py
    * The first argument to this command line needs to be "%1" which represents what you right clicked on
    * The second argument needs to be the path of nfrutil.py file, so it would be c:\nfrutil if you downloaded the files there
    
 ##### Mac
   * You'll need to search for an article on use Automator which is a native app that comes with MacOS
   * when you open Automator first, click on the geer icon, which may be named: "Quick Action" or something else
   * Set up the path and the arguments like the above ( the windows instructions )
     
## To run
 #### On the commandline:
    python3 nfrutil.py 
