import requests
import sqlupload
from datetime import datetime
import smtplib
from selenium import webdriver
import configparser


lastcountydate=sqlupload.getlastcountydate()    #get the last county date   
lastusadate=sqlupload.getlastusadate()          #get the last usa date
resp = requests.get('https://api.covidtracking.com/v1/states/daily.json')   #called the api request
for x in resp.json():                                                       #loop thru the json response
    date = datetime.strptime(str(x['date']), '%Y%m%d').date()               #get date in yy-mm-dd format
    if date<=lastusadate:                                                   #check if date less than or equal than the last date (date in database already)
        continue                                                            #skip over the record in the database
    state=x['state']                                                        #get the state value
    positive=x['positive']                                                  #get positive value
    if positive==None:                                                      #check if positive is none
        positive=0                                                          #set positve to 0
    negative=x['negative']                                                  #get negative value
    if negative==None:                                                      #check if negative is none
        negative=0                                                          #set negative to 0
    hospital=x['hospitalizedCurrently']                                     #get hosital value
    if hospital==None:                                                      #check if hospital is none
        hospital=0                                                          #set negative to 0
    death=x['death']                                                        #get death value
    if death==None:                                                         #check if death is none
        death=0                                                             #set death to 0
    sqlupload.insertcoviddata(date,state,positive,negative,hospital,death)  #insert the data to the database

driver = webdriver.Firefox(executable_path='C:/Users/chris/OneDrive/Running/Running/geckodriver.exe')   #load driver 
driver.get("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv")            #go to csv file
splitcounty=driver.find_element_by_tag_name('body').text.split('\n')                                    #get the csv file
for line in splitcounty[1:]:                                                                            #loop thru each line of the split file starting at the 2nd line
    if line.split(',')[0]=='date':                                                                      #check if date in first column
        continue                                                                                        #skip that line
    date,county,state,fips,cases,deaths=line.split(',')                                                 #split the line 
    date=datetime.strptime(date,"%Y-%m-%d").date()                                                      #get date in yy-mm-dd format
    if date<=lastcountydate:                                                                            #check if date less than or equal than the last date (date in database already)
        continue                                                                                        #skip over the record in the database
    sqlupload.insertcoviddatacounty(date,county,state,fips,cases,deaths)                                #insert the data to the database
