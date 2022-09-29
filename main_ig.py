#PROJECT TO MAKE A NEWSLETTER WHICH TAKES DATA FROM THE WEBSITE AND PUBLISES THE DATA OVER EMAIL AUTOMATICALLY

from http import server
import requests #requests part
from bs4 import BeautifulSoup #web scraping- looking for contents which are in our interest
import smtplib #for emailbody
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime #for datetime

#importing done

now=datetime.datetime.now()  #to check whether the emal sent is not overwritten and that new email is sent everyday. 

content= '' #content placeholder for email from where the email wll begin

#function to extract components such as stories from hacker news website

def extract_news(url): #purpose of the function is to extract the front page titles or headlines and get it in text format
    print('Extracting News stories...')
    cnt='' #temp placeholder which will feed data to content var
    cnt += ('<b>HN TOP STORIES:</b>\n '+'<br>'+'-'*50+'<br>')
    response=requests.get(url) #to get content form the given url...repose is an http response body
    content= response.content #local var
    soup=BeautifulSoup(content,'html.parser')  #extract contents from the parser and find the attributes and components that we require i.e class:title
    for i,tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})): #get data in <td> for class title and valign and enumerate so as to get all the titles with their numerical place...1,2,3,4
        cnt +=((str(i+1)+' :: '+tag.text + "\n"+'   <br>') if tag.text!='More' else '')  #to make a table of all the rows of news columns in serial order...and to  get the data, in text format, of all the headlines except the title:'MORE' present at the very end of the site
    return(cnt)

#preparing the email

cnt=extract_news('https://news.ycombinator.com')    
content +=cnt #global var
content += ('<br>--------------------------------------------------<br>')
content += ('<br><br>End of message') 

#sending the mail

print('Composing email')

SERVER='smtp.gmail.com' #smtp server for gmail
PORT= 587 #port number
FROM='EMAIL ID OF USER'
TO='EMAIL ID OF SENDER'
PASS='*****'

#Creating the message body using MIMEmultipart

msg= MIMEMultipart()

#Creating the titel fo the mail....we add date and time so as to keep the mails unique

msg['Subject'] = 'TOP NEWS IN HN COMMUNITY TODAY' + '' + str(now.day) + '' + str(now.month) + '' + str(now.year)
msg['From'] = FROM 
msg['To'] = TO

msg.attach(MIMEText(content,'html')) #attach the email body to mail

#initiatie the server to send the mail

print('Initiating the server...')

server=smtplib.SMTP(SERVER,PORT)
server.set_debuglevel(1) #to allow debug and error messages,if any, to be seen
server.ehlo() #initiate the server
server.starttls() #initiate the secure tls connection to server
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Mail delivered...')

server.quit()



