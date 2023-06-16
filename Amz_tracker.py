#import all the required modules
import requests
# this is the main library for scrapping data
from bs4 import BeautifulSoup 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#used for data visualization
import seaborn as sns
#We use the below module for emailing the message
from email.message import EmailMessage
#secures communication between both the server and client side
import ssl 
#for sending a mail, if the price goes down
import smtplib 
import time
%matplotlib inline

#The main URL of the product, whose price must be monitered
url="https://www.amazon.in/Apple-iPhone-11-64GB-Product/dp/B07XVKG5XV/ref=sr_1_2_sspa?crid=3I1XCD2J1MZZB&keywords=iphone+13&qid=1686830955&sprefix=iphone%2Caps%2C403&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"

#Same URL but now stored in link as string
link = 'https://www.amazon.in/Apple-iPhone-11-64GB-Product/dp/B07XVKG5XV/ref=sr_1_2_sspa?crid=3I1XCD2J1MZZB&keywords=iphone+13&qid=1686830955&sprefix=iphone%2Caps%2C403&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1'

#header for Mozilla browser
headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"}

#send the request to get the HTML page
page = requests.get(url,headers=headers)

soup = BeautifulSoup(page.content,'html.parser')

#give desired price
desired_price = 60000 #SET THE DESIRED PRICE HERE
#get values
print (soup.title.string)


def check_price():
  #finds the title of the product
  a = soup.find(id="productTitle")
  b = a.get_text()

  #find the price with the help of corresponding ID
  price = soup.find(id ="corePriceDisplay_desktop_feature_div")
  cprice = price.get_text()

  #Since the output has some unwanted characters, we need only the price numbers
  s = cprice[16:22]

  #The string s has a comma inbetween it (ex:23,000) to remove it, we implement the below piece of code
  string_with_comma = s
  string_without_comma = string_with_comma.replace(',', '')
  appended_string = string_without_comma

  #convert the string into float
  Float_price = float(appended_string)

  #give the desired price as input:
  desired = str(desired_price)


def send_email():
  #Sending email
  email_sender = 'sender_email@gmail.com'
  email_password = 'sender_password'
  email_receiver = 'receiver_email@gmail.com'

  #subject and body of the mail
  subject = 'Price down for: ' + b.strip()
  body = 'The price for the product has gone down!\n'+ '\n\n The URL for the product is: ' + link 
  em = EmailMessage()
  em['From'] = email_sender
  em['To'] = email_receiver
  em['Subject'] = subject
  em.set_content(body)

  context = ssl.create_default_context()

  with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
    #required condition to be satisfied
     if(Float_price <= desired_price):
       smtp.login(email_sender,email_password)
       smtp.sendmail(email_sender, email_receiver, em.as_string())
        
#loop that allows the program to regularly check for prices
while(True):
  check_price()
  send_mail()
  time.sleep(60 * 60)
