from bs4 import BeautifulSoup
import datetime
import time
try:
    import winsound
except ImportError:
    pass  # Do not import winsound if not on Windows
import os
import sys
import platform
import lxml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random

options = Options()
options.headless = True

# Automatically get the chromedriver depending on which OS you use
userPlatform = platform.system()
if userPlatform == "Linux":
    driver = webdriver.Chrome(r'./chromedriverLinux', options=options)
elif userPlatform == "Darwin":
    driver = webdriver.Chrome(r'./chromedriverMac', options=options)
elif userPlatform == "Windows":
    scriptDir = os.path.dirname(__file__)
    driver = webdriver.Chrome(r'{0}\chromedriver.exe'.format(str(scriptDir)), options=options)
else:
    print("ERROR: user platform undefined")
    sys.exit()

url_target = "https://studentservices.uwo.ca/secure/timetables/mastertt/ttindex.cfm"
driver.get(url_target)  # get to the website

# search criteria
courseinput = input('Enter subject: ')
driver.find_element_by_xpath('//*[@id="inputSubject"]'). send_keys(courseinput)
# hitting submit to generate the form
submit_button = driver.find_elements_by_xpath('//*[@id="searchform"]/fieldset/div[4]/div/button')[0]
submit_button.click()
# scraping the webpage with data
html = driver.page_source
# parsing
soup = BeautifulSoup(html, 'lxml')

# idea for searching present to them a chart of all available time
# slots and then use section number raw input to find the row they want.

courses = soup.find_all('div',class_='span12')[0] # whole results table everything
coursename = courses.find_all('h4')  # generate a list of all the courses

for c, value in enumerate(coursename):  # print me out a nice list of courses headers to figure out what to hit next
    print(c, value.text)


def validtarget():
    i=int(input('Type the number beside the course you like to view: '))
    if i > (len(coursename)-1) or i<0:
        print('invalid selection')
        return(validtarget())
    else:
        return(i)

coursetarget= validtarget()


# for future refference the structure here is that the table class
# table tablestriped is the individual tables containing the class stuff
# there are multiple T bodies depending on how many  courses there are + 1 per section as its per class
# the t body with section numbers is always [0]

coursesections_a = courses.find_all('table',class_='table table-striped')[coursetarget]
coursesections = coursesections_a.find_all('tbody')[0]
coursesections2 = coursesections.find_all('tr')

for c, i in enumerate(coursesections2):
    sectionnumber = i.find_all('td')[0]
    if c%2 ==0:
        print(c,sectionnumber.text)

sectionchoice = int(input('Type the number beside the desired section: '))

coursesections3 = coursesections.find_all('tr')[sectionchoice]

coursestatusraw = coursesections3.find_all('td')[14].text

coursestatus = coursestatusraw.strip()

print(coursestatus)


def is_it_full():
    driver.get(url_target)
    driver.find_element_by_xpath('//*[@id="inputSubject"]').send_keys(courseinput)
    submit_button = driver.find_elements_by_xpath('//*[@id="searchform"]/fieldset/div[4]/div/button')[0]
    submit_button.click()
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, 'lxml')
    courses = soup.find_all('div', class_='span12')[0]  # whole results table everything
    coursesectionsx = courses.find_all('table', class_='table table-striped')[coursetarget]
    coursesections = coursesectionsx.find_all('tbody')[0]
    coursesections3 = coursesections.find_all('tr')[sectionchoice]
    coursestatusraw = coursesections3.find_all('td')[14].text
    coursestatus = coursestatusraw.strip()

    if coursestatus.lower() == 'full':
        return True
    else:
        return False


def checkfull():
    if is_it_full():
        print('full fam' + '  ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        randomNum = random.randint(0, 1800)
        time.sleep(randomNum)
        checkfull()
    else:
        print('ITS OPEN' + '  ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        if userPlatform == "Windows":
            winsound.PlaySound('SystemHand', winsound.SND_ASYNC + winsound.SND_LOOP)
        else:
            try:
                os.system('play -nq -t alsa synth 3 sine 440')
            except Exception:
                sys.exit()


checkfull()
