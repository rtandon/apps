#python myip.py
import commands
import smtplib

def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
	header  = 'From: %s\n' % from_addr
	header += 'To: %s\n' % ','.join(to_addr_list)
	header += 'Cc: %s\n' % ','.join(cc_addr_list)
	header += 'Subject: %s\n\n' % subject
	message = header + message
	server = smtplib.SMTP(smtpserver)
	server.starttls()
	server.login(login,password)
	problems = server.sendmail(from_addr, to_addr_list, message)
	server.quit()

message_body = commands.getstatusoutput('curl ifconfig.me')
sendemail(from_addr    = 'from_email_address@gmail.com',
          to_addr_list = ['to_email_address@gmail.com'],
          cc_addr_list = [],
          subject      = 'my ip is ==>',
          message      = message_body[1],
          login        = 'gmail_usr_id_who_is_sending_content@gmail.com', #if gmail id is abc.xyz@gmail.com then it shoudl be abc.xyz
          password     = 'xxxxxxxxxx')
