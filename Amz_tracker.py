#import all the required modules
import requests
# for taking command line inputs of url and desired price from user
import argparse
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

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Amazon Price Tracker')
parser.add_argument('--url', type=str, help='URL of the product to track')
parser.add_argument('--desired_price', type=float, help='Desired price for the product')
args = parser.parse_args()

# Ensure the required arguments are provided
if not args.url or not args.desired_price:
    parser.error('Both --url and --desired_price are required.')


#Same URL but now stored in link as string
link = args.url

#header for Mozilla browser
headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"}

#send the request to get the HTML page
page = requests.get(args.url,headers=headers)

soup = BeautifulSoup(page.content,'html.parser')

#give desired price
desired_price_of_item = args.desired_price #SET THE DESIRED PRICE HERE
#get values
print (soup.title.string)
Float_price = 0
b = 'a'

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
  desired = str(desired_price_of_item)


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
     if(Float_price <= desired_price_of_item):
       smtp.login(email_sender,email_password)
       smtp.sendmail(email_sender, email_receiver, em.as_string())
        
#loop that allows the program to regularly check for prices
while(True):
  check_price()
  send_email()
  time.sleep(60 * 60)
