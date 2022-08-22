import requests #to parse https request
from bs4 import BeautifulSoup #for scraping webcontent
import smtplib #for email authentication

#email body
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText

#date and time manipulation
import datetime
now = datetime.datetime.now()



def extract_news(url):
    print('Extracting the news ...............................')
    cnt = ''
    cnt += ('<b> HN Top Stories</b> \n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    if soup != None:
        for i,tag in enumerate(soup.find_all('td', attrs={'class':'title', 'valign':''})):
            cnt += ((str(i+1)+ '::'+ tag.text + '<br>') if tag.text != 'More' else '')
    return cnt

def send_mail(body):
    SERVER = 'smtp.office365.com' # server needs to be chnage depending upon the email client being use
    PORT = 587 # port number would also change as per the server
    FROM = '' # add the recepient email id
    TO = '' # add the recepient email id
    PASSWORD = '' # add the sender email password

    msg = MIMEMultipart()
    msg['Subject'] = 'Top stories from Hacker News [AUTOMATED MAIL]'+ ' ' +str(now.day)+'-'+str(now.month)+'-'+str(now.year)
    msg['From'] = FROM
    msg['To'] = TO
    msg.attach(MIMEText(body, 'html'))
    print('Initiating Server ......')
    server = smtplib.SMTP(SERVER, PORT)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(FROM, PASSWORD)
    server.sendmail(from_addr=FROM, to_addrs=TO, msg=msg.as_string())
    print('Sending Email......')

    server.quit()


def main():
    CONTENT = ''
    news_site_url = 'https://news.ycombinator.com/'
    CNT = extract_news(news_site_url)
    CONTENT += CNT
    CONTENT += ('<br>~~~~~~~~~~~~~~~~~~~~~~~~~<br>')
    CONTENT += ('<br><br>END OF MESSAGE')
    send_mail(CONTENT)


if __name__ == "__main__":
    main()