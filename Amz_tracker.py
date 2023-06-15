import requests
from bs4 import BeautifulSoup # this is the main library for scrapping data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns #used for data visualization
from email.message import EmailMessage
import ssl #secures communication between both the server and client side
import smtplib #for sending a mail, if the price goes down
%matplotlib inline

#The main URL of the product, whose price must be monitered
url="https://www.amazon.in/Apple-iPhone-11-64GB-Product/dp/B07XVKG5XV/ref=sr_1_2_sspa?crid=3I1XCD2J1MZZB&keywords=iphone+13&qid=1686830955&sprefix=iphone%2Caps%2C403&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"

#Same URL but now stored in link as string
link = 'https://www.amazon.in/Apple-iPhone-11-64GB-Product/dp/B07XVKG5XV/ref=sr_1_2_sspa?crid=3I1XCD2J1MZZB&keywords=iphone+13&qid=1686830955&sprefix=iphone%2Caps%2C403&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1'


headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"}

page = requests.get(url,headers=headers)

soup = BeautifulSoup(page.content,'html.parser')

#give desired price
desired_price = 60000
#get values
print (soup.title.string)

#finds the title of the product
a=soup.find(id="productTitle")
b = a.get_text()

#find the price with the help of corresponding ID
price = soup.find(id ="corePriceDisplay_desktop_feature_div")
cprice = price.get_text()

#Since the output has some unwanted characters, we need only the price numbers
s = cprice[16:22]

#The string s has a comma inbetween it (ex:23,000) to remove this, we implement the below piece of code
string_with_comma = s
string_without_comma = string_with_comma.replace(',', '')
appended_string = string_without_comma

#convert the string into float
Float_price = float(appended_string)

#give the desired price as input:
desired = str(desired_price)


#Sending email
email_sender = 'atrueindian05@gmail.com'
email_password = 'iuoa mngv lzcf ksvx'
email_receiver = 'anikethsridhargund.5@gmail.com'

#subject and body of the mail
subject = 'Price down for: ' + b.strip()
body = 'The price for the product has gone down!\n'+ '\n The URL for the product is: ' + link + '\n\n\nThe message is sent by Aniketh Sridhar Gund\n'

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


