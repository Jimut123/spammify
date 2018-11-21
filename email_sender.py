'''
Author : jimutbahanpal@yahoo.com

This software can be used to send enormous amount of spam email using google's smtp library.
The author is not responsible for any trouble caused by this software. Don't spread troubles unless needed to!

...remember

WITH GREAT POWERS COMES GREAT RESPONSIBILITIES

Use as you want...
'''

import smtplib                          # importing the smtplib for google mail
import colorama
from colorama import Fore, Back, Style  # for cool coloring stuffs!
import sqlite3                          # for db stuffs!
from datetime import datetime           # date time stuffs

from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid


conn = sqlite3.connect('spam_email.sqlite')
cur = conn.cursor()

# no  sub content temp img date start end send_addr recv_addr omail
cur.executescript('''
CREATE TABLE IF NOT EXISTS MAIL (
    no          INTEGER,
    sub         TEXT, 
    content     TEXT,
    temp        TEXT,  
    date        DATE,
    start       DATE,
    end         DATE,
    send_addr   TEXT,
    recv_addr   TEXT
);
''')

# sender details
#username    # write the username here
#password			# write the password here

# paljimutbahan@gmail.com

class mail_sender():
    template = """\
	<html>
	  <title> This is the title</title>
	  <head> Some head in this place</head>
	  <body>

	  <h1> 
	  		Header of the mail
	  </h1>

	  <b> 
	  		This is bold!
	  </b>
	  <i> 
	  	This is italics
	  </i>
	  <u> 
	  	This is underline 
	  </u>
	   <p>
	   Salut!
	   </p>
	    <p>Follow on github!
	        <a href="https://github.com/Jimut123">
	            recipie
	        </a> 
	    </p>
	    
	  </body>
	</html>
	"""
    content = """\
	Rse!
	Cela ressemble à un excellent recipie[1] déjeuner.
	[1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718
	--Pepé
	"""

    def get_timestap():
        return datetime.now().isoformat(timespec='seconds')

    def sendmail(senderName, 								# Name of the sender
                    recvName,									# Name of the recipient here
                    subject, 	 								# Give the subject here
                    template, 									# Send the template here
                    content,									# normal text
                    img_flag=False,						  	# By default image flag is set to false
                    img_name="",								# add image name here
                    bckupmsgfilename="outgoingmsg.txt" 		# add the name of the backup msg here
                ):					
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        global username, password
        server.login(username, password)	# load the server
        message = EmailMessage()
        asparagus_cid = make_msgid()
        message['Subject'] = subject
        message['From'] = senderName
        message['To'] = recvName
        #setting the contents here, just the mail here
        message.set_content(content)
        #Adding the template here and formatting to html
        message.add_alternative(template.format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')
        # Now add the related image to the html part.
        '''
        if img_flag == True:
            with open(img_name,'rb') as img:
                message.get_payload()[1].add_related(img.read(),'image','jpeg',cid=asparagus_cid)
        '''
        # Make a local copy of what we are going to send.
        with open(bckupmsgfilename, 'wb') as f:
            f.write(bytes(message))
        server.sendmail(senderName, recvName, str(message))
        server.quit()



if __name__=='__main__':
    # to send the mail
    number_mails = int(input(Fore.BLUE+"Enter the number of mails you want to send  [LIMIT is 10,000 for Google (gmail) SMTP] :  "))
    print(Fore.BLUE+"SENDING ",Fore.RED+str(number_mails),Fore.BLUE+" one by one ... ")
    recv_name = input(Fore.GREEN+"Enter the receiver's address :  ")
    obj = mail_sender       # creating the object of the email sender class
    sub = input(Fore.GREEN+"Enter the subject of the email :  ")
    global username,password
    
    start_time = obj.get_timestap()
    print(Fore.GREEN+" START TIME :: ",start_time)
    num_sent = 0
    for i in range(number_mails):

        if i%5==0:              # commiting after sending 5 emails sucessfully! 
            conn.commit()       
        
        try:
            num_sent += 1
            obj.sendmail(username,
                recv_name,
                sub,
                obj.template,
                obj.content,
                False,                  # set : True for sending image
                "roasted-asparagus.jpg",
                "outgoingmsg.txt")
            end_time = obj.get_timestap()
            print(Fore.GREEN+"LOGS : ", Fore.GREEN,num_sent, sub, obj.content, Style.DIM+obj.template, start_time, start_time, end_time, username, recv_name)
            cur.execute('''INSERT OR IGNORE INTO MAIL (no, sub, content, temp, date, start, end, send_addr, recv_addr)
                    VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )''', ( num_sent, sub, obj.content, obj.template, start_time, start_time, end_time, username, recv_name  ) ) # stacks the link found at the bottom
        except:
            print(Fore.RED+"OOPS!!! SOMETHING WENT WRONG!")

conn.commit()

    

