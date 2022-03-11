
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item for QUT's teaching unit
#  IFB104, "Building IT Systems", Semester 1, 2021.  By submitting
#  this code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
student_number = 8738033 # put your student number here as an integer
student_name   = 'Jason Kendrick' # put your name here as a character string
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Choose Your News
#
#  In this assignment you will combine your knowledge of HTMl/CSS
#  mark-up languages with your skills in Python scripting, pattern
#  matching, databases and Graphical User Interface design to produce
#  a useful application that allows the user to compare news stories
#  from multiple sources and save them for later perusal.
#
#  See the client's requirements accompanying this file for full
#  details.
#
#--------------------------------------------------------------------#



#-----Initialisation Steps-------------------------------------------#
#

# Import standard Python 3 modules needed to complete this assignment.
# You should not need to use any modules other than those provided
# in a standard Python 3 installation for your solution.
#
# In particular, you may NOT use any Python modules that need to be
# downloaded and installed separately, such as "Beautiful Soup" or
# "Pillow", because the markers will not have access to such modules
# and will not be able to run your code.  Only modules that are part
# of a standard Python 3 installation may be used.

# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from datetime import datetime
from os import name
from sys import exit as abort
from urllib import request
from urllib.error import HTTPError

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function below.)
from urllib.request import urlopen

# Some standard Tkinter functions.  (You WILL need to use
# SOME of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.  (NB: DON'T import all of the "tkinter.tkk" functions
# using a "*" wildcard because this module includes alternative
# versions of standard widgets like "Label".)
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar
from tkinter import messagebox

# Functions for finding occurrences of a pattern defined
# via a regular expression.  (You do not necessarily need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import *

# A function for displaying a web document in the host
# operating system's default web browser (renamed to
# distinguish it from the built-in "open" function for
# opening local files).  (You WILL need to use this function
# in your solution.)
from webbrowser import open as urldisplay

# All the standard SQLite functions.
from sqlite3 import *

# Confirm that the student has declared their authorship.
# You must NOT change any of the code below.
if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()

#
#--------------------------------------------------------------------#



#-----Supplied Function----------------------------------------------#
#
# Below is a function you can use in your solution if you find it
# helpful.  (You are not required to use this function, but it may
# save you some effort.)
#

# A function to download and save a web document.  The function
# returns the downloaded document as a character string and
# optionally saves it as a local file.  If the attempted download
# fails, an error message is written to the shell window and the
# special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * incognito - If this parameter is True the Python program will
#      try to hide its identity from the web server. This can
#      sometimes be used to prevent the server from blocking access
#      to Python programs. However we do NOT encourage using
#      this option as it is both unreliable and unethical to
#      override the wishes of the web document provider!
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'downloaded_document',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             incognito = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if incognito:
            # Pretend to be a Windows 10 computer instead of
            # a Python script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                               'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                               'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')
            print("Warning - Request does not reveal client's true identity.")
            print("          This is both unreliable and unethical!")
            print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

                            ##BACK END##

#Replaces unicode text for readability
def text_cleaner(string):
    global cleaned_text
    cleaned_text = string.replace('&quot;', '"')
    cleaned_text = cleaned_text.replace('&#x27;', "'")
    cleaned_text = cleaned_text.replace("\\", "")
    return cleaned_text

#This function is attatched to each button, utilizes download function
def button_press(address, filename):
    global source_html
    #Try to download, if it can't assume no connection
    try:
        source_html = download(url = address,
        target_filename = filename,
        filename_extension = 'html',
        save_file = False,
        char_set = 'UTF-8',
        incognito = False)
        #if source_html has no value, assume no internet connection
        if not source_html:
            messagebox.showinfo("No Internet Connection!",\
            "No Internet Connection. Please try again later.")
            #Clear list to stop export button on articles
            #remaining after internet disconnects
            export_list.clear()

    #If changes happen in the future or anything else goes wrong
    #(Access Denied or webserver goes down)
    except:
        headline.delete(1.0, END)
        abstract.delete(1.0, END)
        headline.insert(END, "Oops! We had trouble downloading this page.")
        abstract.insert(END, "Oops! We had trouble downloading this page.")

    #website address for check_source function
    #source name for export selection
    global website_address
    global source_name
    website_address = address
    source_name = filename

    #If a button is pressed, then depending on the argument to the call,
    #go to relevant function. Each website has their own function
    if source_name == 'Brisbane Times':
        news_source.delete(1.0, END)
        news_source.insert(END, "News Source: " + source_name)
        find_brisbane_times_details()
    
    elif source_name == 'Nine News':
        news_source.delete(1.0, END)
        news_source.insert(END, "News Source: " + source_name)
        find_nine_details()

    elif source_name == 'The Age':
        news_source.delete(1.0, END)
        news_source.insert(END, "News Source: " + source_name)
        find_the_age_details()

    elif source_name == 'ABC News':
        news_source.delete(1.0, END)
        news_source.insert(END, "News Source: " + source_name)
        find_abc_details()


#Command for check source button
def check_source():
    try:
        urldisplay(website_address, new=2)
    #if website_address is null, assume no source has been selected
    except NameError:
        messagebox.showinfo("Select a source first!",\
            "Please choose a website to check!")

"""
All website functions have been kept individual and may be repetitive
This is due to the nature of websites changing HTML over time making it
easier to debug findall in the future.
"""

#If the distance between certain HTML characters,
#picked with find, is greater than 300 than assume the abstract
#for the current article is not the correct one.
def check_distance_between_text(pattern_start, pattern_end):
    distance_start = source_html.find(pattern_start)
    distance_end = source_html.find(pattern_end)
    distance = distance_end - distance_start
    if distance > 300:
        abstract.delete(1.0, END)
        abstract.insert(END, "Error - No Abstract Found!")
    
#Brisbane Times function for scraping HTML.
def find_brisbane_times_details():
    #Using regular expressions and findall to get all information

    #Brisbane Times Headline
    try:
        brisbane_times_headline = findall\
            ('"headline":"(.+?(?="))', source_html)[0]
        text_cleaner(brisbane_times_headline)
        headline.delete(1.0, END)
        headline.insert(END, cleaned_text)
    #If none found by findall, print this!
    except:
        headline.delete(1.0, END)
        headline.insert(END, "Error - No Headline Found!")

    #Brisbane Times Abstract
    try:
        brisbane_times_abstract = findall\
            ('"about":"(.+?(?="))', source_html)[0]
        text_cleaner(brisbane_times_abstract)
        abstract.delete(1.0, END)
        abstract.insert(END, cleaned_text)
    except:
    #If none found from findall, error handle
        abstract.delete(1.0, END)
        abstract.insert(END, "Error - No Abstract Found!")

    #Checking distance between headline start and abstract start
    #Brisbane Times has abstract before headline, so checking backwards
    check_distance_between_text\
        ('"about":"', '"headline":"')

    #Brisbane Times Dateline
    try:
        brisbane_times_dateline = findall\
            (':\d\d">([^<]+)', source_html)[0]
        dateline.delete(1.0, END)
        dateline.insert(END, "Dateline: " + brisbane_times_dateline)
    #If none found from findall, error handle    
    except:
        dateline.delete(1.0, END)
        dateline.insert(END, "Dateline: Error - No Dateline Found!")

    #Brisbane Times Hostname
    hostname.delete(1.0, END)
    hostname.insert\
        (END, "Hostname: www.brisbanetimes.com.au")

    #Brisbane Times URL
    url_address.delete(1.0, END)
    url_address.insert\
        (END,"URL: " + website_address)

    #export_list for export selection
    #Updated every function to ensure correct exporting
    try:
        global export_list
        export_list = [brisbane_times_dateline,
        brisbane_times_headline,
        brisbane_times_abstract,
        source_name]
    #As the error handling happens in the export_selection function
    #skip this if it fails to assign the list due to missing variables
    except:
        pass

#The Age function for scraping HTML.
def find_the_age_details():
    #Using regular expressions and findall to get all information

    #The Age Headline
    try:
        the_age_headline = findall\
            ('"headline":"(.+?(?="))', source_html)[0]
        text_cleaner(the_age_headline)
        headline.delete(1.0, END)
        headline.insert(END, cleaned_text)
    #If none found from findall, error handle
    except:
        headline.delete(1.0, END)
        headline.insert(END, "Error - No Headline Found!")

    #The Age Abstract
    try:
        the_age_abstract = findall\
            ('"about":"(.+?(?="))', source_html)[0]
        text_cleaner(the_age_abstract)
        abstract.delete(1.0, END)
        abstract.insert(END, cleaned_text)
    #If none found from findall, error handle
    except:
        abstract.delete(1.0, END)
        abstract.insert(END, "Error - No Abstract Found!")

    #The Age also has abstract start before headline in HTML
    #check distance to ensure correct abstract
    check_distance_between_text\
        ('"about":"', '"headline":"')

    #The Age Dateline
    try:
        the_age_dateline = findall\
            ('dateTime="([\d+\W]*)T\d\d\D\d', source_html)[0]
        dateline.delete(1.0, END)
        dateline.insert(END, "Dateline: " + the_age_dateline)    
    #If none found from findall, error handle
    except:
        dateline.delete(1.0, END)
        dateline.insert(END, "Dateline: Error - No Dateline Found!")

    #The Age Hostname
    hostname.delete(1.0, END)
    hostname.insert\
        (END, "Hostname: www.theage.com.au")

    #The Age URL
    url_address.delete(1.0, END)
    url_address.insert\
        (END,"URL: " + website_address)

    #export_list for export selection
    #Updated every function to ensure correct exporting
    try:
        global export_list
        export_list = [the_age_dateline,
        the_age_headline,
        the_age_abstract,
        source_name]
    #As the error handling happens in the export_selection function
    #skip this if it fails to assign the list due to missing variables
    except:
        pass

#ABC News function for scraping HTML.
def find_abc_details():

    #Using regular expressions and findall to get all information

    #ABC News Headline
    try:
        abc_news_headline = findall\
            ('title":{"children":"(.+?(?="))', source_html)[0]
        text_cleaner(abc_news_headline)
        headline.delete(1.0, END)
        headline.insert(END, cleaned_text)
    #If none found from findall, error handle
    except:
        headline.delete(1.0, END)
        headline.insert(END, "Error - No Headline Found!")

    #ABC News Abstract
    try:
        abc_news_abstract = findall\
            ('"synopsis":"(.+?(?=","title"))', source_html)[0]
        text_cleaner(abc_news_abstract)
        abstract.delete(1.0, END)
        abstract.insert(END, cleaned_text)
    #If none found from findall, error handle
    except:
        abstract.delete(1.0, END)
        abstract.insert(END, "Error - No Abstract Found!")

    #ABC also has abstract before headline
    check_distance_between_text\
    ('"synopsis":"', 'title":{"children":"')

    #ABC News Dateline
    try:
        abc_news_dateline = findall\
            ('dateTime="([\d+\W]*)T\d\d\D\d', source_html)[0]
        dateline.delete(1.0, END)
        dateline.insert(END, "Dateline: " + abc_news_dateline)
    #If none found from findall, error handle
    except:
        dateline.delete(1.0, END)
        dateline.insert(END, "Dateline: Error - No Dateline Found!") 

    #ABC News Hostname
    hostname.delete(1.0, END)
    hostname.insert\
        (END, "Hostname: www.abc.net.au")

    #ABC News URL
    url_address.delete(1.0, END)
    url_address.insert\
        (END,"URL: " + website_address)

    #export_list for export selection
    #Updated every function to ensure correct exporting
    try:
        global export_list
        export_list = [abc_news_dateline,
        abc_news_headline,
        abc_news_abstract,
        source_name]
    #As the error handling happens in the export_selection function
    #skip this if it fails to assign the list due to missing variables
    except:
        pass

#Once downloaded, find the specific text from Nine News HTML
def find_nine_details():
    #Using regular expressions and findall to get all information

    #Nine News Headline
    try:
        nine_news_headline = findall\
            ('(?:story__headline__text">)([^<]+)', source_html)[0]
        text_cleaner(nine_news_headline)
        headline.delete(1.0, END)
        headline.insert(END, cleaned_text)

    #If none found from findall, error handle
    except:
        headline.delete(1.0, END)
        headline.insert(END, "Error - No Headline Found!")

    #Nine News Abstract
    try:
        nine_news_abstract = findall\
            ('(?:story__abstract">)([^<]+)', source_html)[0]
        text_cleaner(nine_news_abstract)
        abstract.delete(1.0, END)
        abstract.insert(END, cleaned_text)
        
    #If none found from findall, error handle
    except:
        abstract.delete(1.0, END)
        abstract.insert(END, "Error - No Abstract Found!")

    #Error handle distance in the case that findall finds the next
    #articles items instead of displaying none found.
    check_distance_between_text\
        ('"story__headline__text">', '"story__abstract">')
        
    #Nine News Dateline
    try:
        nine_news_dateline = findall\
            ('date[t|T]ime="([^">]+)+', source_html)[0]
        dateline.delete(1.0, END)
        dateline.insert(END, "Dateline: " + nine_news_dateline)
    #If none found from findall, error handle
    except:
        dateline.delete(1.0, END)
        dateline.insert(END, "Dateline: Error - No Dateline Found!")

    #Nine News Hostname
    hostname.delete(1.0, END)
    hostname.insert\
        (END, "Hostname: www.9news.com.au")

    #Nine News URL
    url_address.delete(1.0, END)
    url_address.insert\
        (END,"URL: " + website_address)

    #List is always defined at the end as to always
    #be the correct source to export
    try:
        global export_list
        export_list = [nine_news_dateline,
        nine_news_headline,
        nine_news_abstract,
        source_name]
    #As the error handling happens in the export_selection function
    #skip this if it fails to assign the list due to missing variables
    except:
        pass

#Export selection into selected_news database
def export_selection():

    #Initial connection and SQL query
    connection = connect(database = 'selected_news.db')
    selected_news = connection.cursor()
    sql_statement = "INSERT INTO latest_news\
        (date_or_time, headline, abstract, news_source)\
            VALUES (?, ?, ?, ?)"

    #List obtained after news article prints on screen.
    try:
        dateline = export_list[0]
        headline = export_list[1]
        abstract = export_list[2]
        news_source = export_list[3]
        sql_values = (dateline, headline, abstract, news_source)
        selected_news.execute(sql_statement, sql_values)
        connection.commit()
        selected_news.close()
        connection.close()
        messagebox.showinfo("Done!",
        "Export Successful!")
    #export_list NameError if no source selected
    #or if there's an error finding text
    except NameError:
        messagebox.showinfo("Try again later!",
        "Cannot export at this time!")
    #List empty if internet connection offline
    except IndexError:
        messagebox.showinfo("No Internet Connection!",
        "Cannot export in offline mode!")

                    ##FRONT END##

main_window = Tk()
main_window.title('This Just In! (Breaking News)')
main_window.configure(background='#2f3030')

#Main image of BREAKING NEWS
banner = PhotoImage(file = 'Breaking_news.gif')
banner_label = Label(main_window,
                image = banner, borderwidth = 0, bg = '#2f3030').\
     grid(row = 3, column = 1, rowspan = 2, sticky = SE, columnspan = 3)

#Image with frame used to blend drop shadow of BREAKING NEWS image
story_border = PhotoImage(file = 'story_border.gif')
latest_news_border = Label(main_window,
                           image = story_border,
                           borderwidth = 0).\
     grid(row= 1, column = 4, rowspan = 4)

#Frame for Headline section inside of story_border image
headline_frame = LabelFrame(latest_news_border,
                            text="Breaking News Headlines",
                            font = 'Arial 16 bold',
                            fg = 'white',
                            bg = '#2f3030')
headline_frame.grid(row = 1, column = 4, rowspan = 4)


#headline text centered at the top
headline = Text(headline_frame,
                 font = ('Arial 12 bold'),
                 width = 51, height = 4,
                       bg = '#2f3030',
                       fg = 'white',
                       wrap = WORD)
headline.insert(END, "Story Headline appears here")

#Dateline text box
dateline = Text(headline_frame, height = 1, width = 65,
                bg = '#2f3030',
                fg = 'white',
                font = 'Arial 10 bold')
dateline.insert(END, "Dateline: ")

#News source text box
news_source = Text(headline_frame, height = 1, width = 65,
                bg = '#2f3030',
                fg = 'white',
                font = 'Arial 10 bold')
news_source.insert(END, "News Source: ")

#Hostname text box
hostname = Text(headline_frame, height = 1, width = 65,
                bg = '#2f3030',
                fg = 'white',
                font = 'Arial 10 bold')
hostname.insert(END, "Hostname: ")

#URL text box
url_address = Text(headline_frame, height = 1, width = 65,
                bg = '#2f3030',
                fg = 'white',
                font = 'Arial 10 bold')
url_address.insert(END, "URL: ")

#Abstract text box
abstract = Text(headline_frame, height = 15, width = 51,
                bg = '#2f3030',
                fg = 'white',
                font = 'Arial 12 bold',
                wrap = WORD)
abstract.insert(END, "Story abstract appears here")

#Positions of text boxes on screen
headline.grid(row= 1, column = 4)
dateline.grid(row = 2, column = 4)
news_source.grid(row = 3, column = 4)
hostname.grid(row = 4, column = 4)
url_address.grid(row = 5, column = 4)
abstract.grid(row = 6, column = 4)


#border image behind buttons and frames
top_border = PhotoImage(file = 'top_border.gif')
top_button_border = Label(main_window,
                         image = top_border,
                         borderwidth = 0).\
     grid(row= 1, column = 0, rowspan = 2, columnspan = 5, sticky = W)

#Frame for the four buttons
button_frame = LabelFrame(top_button_border,
                          text="Breaking News Sources",
                          font = 'Arial 18 bold',
                          fg = 'white',
                          bg = '#2f3030')
button_frame.grid(row = 1, column = 1, rowspan = 2, sticky = E)

#Frame for Options Menu buttons
option_frame = LabelFrame(top_button_border,
                          text="Options",
                          font = 'Arial 18 bold',
                          fg = 'white',
                          bg = '#2f3030')
option_frame.grid(row = 1, column = 2, rowspan = 2)

#Options Menu button 1 
export_selection = Button(option_frame, text = "Export Selection",
                    command = export_selection,
                    font = ('Arial 15 bold'),
                    padx = 10, pady = 10).\
                    grid(row = 1, column = 1)

#Options Menu button 2
check_source = Button(option_frame, text = "Check Source",
                    command = check_source,
                    font = ('Arial 15 bold'),
                    padx = 22, pady = 10).\
                    grid(row = 2, column = 1)

#NEWS SOURCES#

#lambda is used below because Tkinter's command argument runs a call
#to a function automatically without the button being pressed,
#but only if the function being called as a command has an argument.

#News Source button for ABC
abcnews = PhotoImage(file = 'ABCNews.GIF')
news_option_1 = Button(button_frame,
                       image = abcnews,
                       command = lambda:
                       button_press(
                           #Website to be downloaded
                           'https://www.abc.net.au/news/justin/',
                           #Title of news site
                           'ABC News'),
                       padx = 10, pady = 10).\
                    grid(row = 1, column = 2)

#News Source button for The Age
the_age = PhotoImage(file = 'TheAge.GIF')
news_option_2 = Button(button_frame,
                       image = the_age,
                       command = lambda:
                       button_press(
                            #Website to be downloaded
                           'https://www.theage.com.au/breaking-news',
                           #Title of news site
                           'The Age'),
                       padx = 10, pady = 10).\
                    grid(row = 1, column = 3)

#News Source button for 9 News
ninenews = PhotoImage(file = '9News.GIF')
news_option_3 = Button(button_frame, image = ninenews,
                    command = lambda:
                    button_press(
                        #Website to be downloaded
                        'https://www.9news.com.au/just-in',
                        #Title of news site
                        'Nine News'),
                    padx = 10, pady = 10).\
                        grid(row = 2, column = 2)

#News Source button for Brisbane Times
brisbane_times = PhotoImage(file = 'brisbanetimes.GIF')
news_option_4 = Button(button_frame, image = brisbane_times,
                    command = lambda:
                    button_press(
                    #Website to be downloaded
                    'https://www.brisbanetimes.com.au/breaking-news',
                    #Title of news site
                    'Brisbane Times'),
                    padx = 10, pady = 10).\
                    grid(row = 2, column = 3)

main_window.mainloop()
