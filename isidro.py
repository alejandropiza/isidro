from urllib.request import urlopen
import time

import smtplib
from email.mime.text import MIMEText



url="https://www.vh-ulm.de/wir-ueber-uns/dozentinnen/dozentin-detailseite/dozent/nuacutentildeez-ornelas-isidro/7987"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
start_index=0
longitud=(len(html))
seguir=1
urlList=[]
nameList=[]
timeList=[]
numList=[]
statusList=[]
numCursos=0


while seguir==1:
  title_index = html.find("course__link",start_index)
  if title_index==-1:
    seguir=0
    break
  start_index = title_index + 21
  end_index = html.find("data-pjax",start_index)-2
  courselink = html[start_index:end_index]
  courselink="https://www.vh-ulm.de/"+ courselink
  #print(courselink)
  urlList.append(courselink)  
  numCursos=numCursos+1  
  
  start_index=html.find("course__num",start_index)+13
  end_index=html.find("</span>",start_index)
  coursenum=html[start_index:end_index]
  #print(coursenum)
  numList.append(coursenum)
    
  start_index=html.find("course__title",start_index)+15
  end_index=html.find("</span>",start_index)
  coursename=html[start_index:end_index]
  #print(coursename)
  nameList.append(coursename)
    
  start_index=html.find("course__time",start_index)+14
  end_index=html.find("</span>",start_index)
  coursetime=html[start_index:end_index]
  #print(coursetime)
  timeList.append(coursetime)
  statusList.append("status1")


while True:
  theBody=""
  for x in range(numCursos-1):
    nuevoStatus=0
    page = urlopen(urlList[x])  
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")  
    title_index = html.find("kfrcrs__avlblty-")
    start_index = title_index + len("kfrcrs__avlblty--")
    end_index = start_index+7
    status = html[start_index:end_index]
    if status!=statusList[x]:
      statusList[x]=status
      nuevoStatus=1
    if nuevoStatus==1:
      print(nameList[x] + " ( " + numList[x] + " )")      
      print(status)
      print()
      theBody=theBody+nameList[x] + " ( " + numList[x] + " )"
      theBody=theBody+ "\r\n"+status+ "\r\n" + "\r\n"

  subject = "Aviso de cambio de asistentes a tu curso."
  body = theBody
  sender = "alexpatopiza@gmail.com"
  recipients = ["alejandropiza@hotmail.com", "chinonlineservices@gmail.com"]
  password = "dgnfkubvalfgaupx"


  def send_email(subject, body, sender, recipients, password):
      msg = MIMEText(body)
      msg['Subject'] = subject
      msg['From'] = sender
      msg['To'] = ', '.join(recipients)
      with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
         smtp_server.login(sender, password)
         smtp_server.sendmail(sender, recipients, msg.as_string())
      print("Message sent!")

  if (theBody!=""):
    send_email(subject, body, sender, recipients, password)

  
  time.sleep(300)
