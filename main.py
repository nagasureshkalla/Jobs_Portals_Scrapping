
from argparse import Action
from cgitb import html
from operator import contains, indexOf
from re import S
from attr import attrs
import telebot
import requests
import time
import concurrent.futures
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--start-maximized")


API_KEY =  "MyAPIKey"
bot=telebot.TeleBot(API_KEY)

###################################  URLS ###################################################
urllist=["https://in.indeed.com/jobs?q=Fresher+%E2%82%B92%2C70%2C000&l=india&sort=date&fromage=3",
"https://www.linkedin.com/jobs/search?keywords=LinkedIn&location=India&locationId=&geoId=102713980&f_TPR=r86400&f_E=2&position=1&pageNum=0",
"https://www.monsterindia.com/srp/results?sort=2&limit=100&locations=hyderabad,secunderabad&experienceRanges=1~1&experience=1&salaryRanges=200000~500000&filter=true",
"https://www.naukri.com/google-jobs?experience=0&jobAge=1"]
##############################################################################################



############################# Functions ##############################


def naukari(naukari_url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(naukari_url)
    
    
    soup=BeautifulSoup(driver.page_source,'html5lib')
    list1=[]
    for i in soup.findAll('article',attrs={'class':'jobTuple bgWhite br4 mb-8'}):
        dict1={}
        dict1['Job']=i.find('a',attrs={'class':'title fw500 ellipsis'}).text
        dict1['Recruiter']=i.find('a',attrs={'class':'subTitle ellipsis fleft'}).text
        dict1['Salary']=i.find('li',attrs={'class':'fleft grey-text br2 placeHolderLi salary'}).text
    
        try:
            dict1['Experience']=i.find('li',attrs={'class':'fleft grey-text br2 placeHolderLi experience'}).text
        except:
            pass
        try:
            dict1['Application DeadLine']=i.find('li',attrs={'class':'fleft grey-text br2 placeHolderLi date'}).text
        except:
            pass
        try:
            dict1['link']=i.find('a',attrs={'class':'title fw500 ellipsis'}).get('href')
        except:
            pass
        list1.append(dict1)

    print(str(len(list1))+" Jobs Found in Last 24 Hours from Naukari","\n\n")
    return list1

def linkedIn(linkedin_url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(linkedin_url)
    
 
    
    list1=[]

    for i in range(0,3):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(4)
    
    soup=BeautifulSoup(driver.page_source,'html5lib')

   
   
    dict1={}

    try:  # For First record
        first=soup.find('div',attrs={'class':'base-card base-card--link base-search-card base-search-card--link job-search-card job-search-card--active'})
        card=first.find('div',attrs={'class':'base-search-card__info'})
        
        dict1['Job']=card.find('h3',attrs={'class':'base-search-card__title'}).text.strip()
        dict1['Recruiter']=card.find('h4',attrs={'class':'base-search-card__subtitle'}).text.strip()
        dict1['Location']=card.find('div',attrs={'class':'base-search-card__metadata'}).find('span',attrs={'class':'job-search-card__location'}).text.strip()
        dict1['Posted']=card.find('div',attrs={'class':'base-search-card__metadata'}).find('time',attrs={'class':'job-search-card__listdate--new'}).text.strip()
        dict1['Link']=first.find('a',attrs={'class':'base-card__full-link'}).get('href').strip()
    except:
        pass
    list1.append(dict1)
    # From Second to Last Reord
    for i in soup.findAll('div',attrs={'class':'base-card base-card--link base-search-card base-search-card--link job-search-card'}):
        
        jd=False
        

        dict1={}
        
        card=i.find('div',attrs={'class':'base-search-card__info'})
        dict1['Job']=card.find('h3',attrs={'class':'base-search-card__title'}).text.strip()
        dict1['Recruiter']=card.find('h4',attrs={'class':'base-search-card__subtitle'}).text.strip()
        dict1['Location']=card.find('div',attrs={'class':'base-search-card__metadata'}).find('span',attrs={'class':'job-search-card__location'}).text.strip()
        

        try:
            dict1['Posted']=card.find('div',attrs={'class':'base-search-card__metadata'}).find('time',attrs={'class':'job-search-card__listdate--new'}).text.strip()
            jd=True
        except:
            pass
        try:
            if jd==False:
                dict1['Posted']=card.find('div',attrs={'class':'base-search-card__metadata'}).find('time',attrs={'class':'job-search-card__listdate'}).text.strip()
        except:
            pass
        dict1['Link']=i.find('a',attrs={'class':'base-card__full-link'}).get('href').strip()

        list1.append(dict1)
    print(str(len(list1))+" Jobs Found in Last 24 Hours from LinkedIN","\n\n")
    return list1

########################################################  Test cases ##########################################

# print(linkedIn("https://www.linkedin.com/jobs/search?keywords=LinkedIn&location=India&locationId=&geoId=102713980&f_TPR=r86400&f_E=2&position=1&pageNum=0"))


###############################################################################################################
def lambda_handler(list1):

    if list1[1]==0:
        #### Indeed
        return []
    if list1[1]==1:
        result=linkedIn(str(list1[0]))
        return result
    if list1[1]==2:
        #### Monster
        return []
    if list1[1]==3:
        result=naukari(str(list1[0]))
        return result
    




def parralle_execution(list1):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results=executor.map(lambda_handler, list1)

    return list(results)



##################################  Functions Code END    ########


#################################################################################

# url = 'https://api.telegram.org/bot5238925279:AAG-MA4LlKpLE6-EQrMq3N1ylnRuGRckALA/sendMessage?chat_id=@daily_nagu_jobs&text=hello'


##################################################################################

######################################  BOT CODE  ############################################
@bot.message_handler(commands=['hi'])
def hi(message):
    bot.reply_to(message,"\n<b>"+"Hello"+"</b><a href='www.google.com'>"+"World"+"</a>",parse_mode="HTML")
    

@bot.message_handler(func=lambda msg: msg.text is not None and "go" in msg.text)
def quantity_link(message):
    list2=[]
    list3=[]
    count=0
    for i in urllist:
        list2.append((i,count))
        count+=1
   
    final_report=parralle_execution(list2)

    for i in final_report:
        if i != []:
            for j in i:
                str=""
                for key, val in j.items():
                    if "http" in val or "www" in val:
                        str=str+"\nMore info : <a href='{}'>{}</a>".format(val, key)
                    else:
                        str=str+"\n<b>{}</b> : {}".format(key, val)
                        
                list3.append(str)

    count1=0
    for i in list3:
        # if list3.index(i)%4==0:
            
        
        bot.send_message("@daily_nagu_jobs",i,parse_mode="HTML",disable_web_page_preview=True,disable_notification=False)
        time.sleep(5)
        count1+=1
    print(count1," is the No. messages Send")

############################################################################################



######################################### BOT HEAD CODE  ###################################

try:
    bot.polling()
except:
    pass

###########################################################################################