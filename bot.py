import socket
import datetime
import argparse

server = "irc.freenode.net"
channel = "#jec-dev"
botnick = "Mybot"
logfileSuffix = "logs"
date_time=datetime.datetime(2016,9,13)
  
def ping(): # responds to server pings
  ircsock.send("PONG :pingis\n")

def sendmsg(chan , msg,s=0):
  if s:
    ircsock.send(msg)
  else:
    ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")
  
def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

def hello(receiver=channel):
  ircsock.send("PRIVMSG "+ receiver +" :Hello!\n")

def name_parser(msg):
  #  Returns the values from the server message.
  #  :amey!~amey@182.70.246.196 PRIVMSG #jec-dev :Hello Mybot
  #  ^^^^This is basic syntax of messages received from server. 
  return msg[1:(msg.find('!'))]
  
def init_logger():
  #Initialses the open function and returns a file handle to write logs to
  
  f.write('\n***********************Logging started***************************\n')
  f.write('\t%s\t\n'%date_time.now().strftime('%Y-%m-%d %H:%M:%S'))
  

def logger(msg,f):
  #stores the message into a file on the host
  f.write(str(msg)+'\n')
  
def close_logger(f):
  f.write('\t%s\t\n'%date_time.now().strftime('%Y-%m-%d %H:%M:%S'))
  f.write('\n***********************Logging ended***************************\n')


logfile=channel[1:]+'.'+logfileSuffix
with open(logfile,'a') as f:
  try:
    init_logger()
    ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
    ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" Test Bot\n") # user authentication
    ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot
    joinchan(channel)
    while 1:
      ircmsg = ircsock.recv(2048)
      ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
      print(ircmsg) # server messages
      logger(ircmsg,f)
      if ircmsg.find("PRIVMSG "+botnick+" :Hello ") != -1:
        #PRIVMSG to Mybot
        ircsock.send("PRIVMSG "+name_parser(ircmsg)+' :Hello!!! How are you?\n')
        logger("PRIVMSG "+name_parser(ircmsg)+' :Hello!!! How are you?\n',f)

      if ircmsg.find("PRIVMSG "+channel+' :Hello '+botnick) != -1:
        #PRIVMSG to Mybot on channel
        name=name_parser(ircmsg)
        ircsock.send("PRIVMSG "+channel+' :Hello '+name+' \n')
        logger("PRIVMSG "+channel+' :Hello '+name+' \n',f)

      if ircmsg.find("PING :") != -1:
        ping()

  except(KeyboardInterrupt):
    close_logger(f)
