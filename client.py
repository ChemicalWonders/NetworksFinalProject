# Twitter Client - CS 164 Final Project
# by Kevin Chan - 861009116

import socket
import select
import string
import sys
import getpass
import os
import re

def prompt() :
    return raw_input('Enter a tweet \'140 or less\' : ')

def hashtag():
    return raw_input('Enter the hashtags you want to include: ')

def login() : 
    name = raw_input('Enter Username: ')
    #print name
    s.send(name);
 
    pwd = getpass.getpass('Enter your Password: ')
    #print pwd
    s.send(pwd)

def menu() :
    print '\n|| Welcome to Kitter: Kevin\'s Twitter! ||'
    print '|| MENU OPTIONS:                       ||'
    print '|| A. READ OFFLINE KWITS               ||'
    print '|| B. EDIT SUBSCRIPTIONS               ||'
    print '|| C. POST A MESSAGE                   ||'
    print '|| D. HASHTAG SEARCH                   ||'
    print '|| E. LOG OUT                          ||\n'
    print 'Enter a value :'

#main function
if __name__ == "__main__":
     
    if(len(sys.argv) < 3) :
        print 'Usage : python client.py hostname port'
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
    loggedin = 0

while loggedin == 0:

       login()
       name = s.recv(128)
       if name == '0':
          print 'Username/Password combination was incorrect'

       else:
      	  loggedin = 1
          

number = '0'
while 1:
        socket_list = [sys.stdin, s]
        #os.system('clear')
        print 'Welcome ' + name + '!' + ' You have ' + number + ' of unread messages.'
        print 'You can start sending messages '
        menu()

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
    
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    print data
                    #prompt()
             
            #user entered a message
            else :
                msg = raw_input()
                if msg == 'A':
                   print 'You have 0 unread messages'
                elif msg == 'B':
                   print 'You are following,\'beta\', \'omega\' '
                   following = raw_input('Enter \'1\' to unfollow. Enter \'2\' to follow.')
                   if following == '1':
                      unfollowing = raw_input('Enter the name you want to unfollow: ')
                      print 'You are not following: ' + unfollowing + ' anymore.'                   
                   elif following == '2':
                      follower = raw_input('Enter the name you want to follow: ')
                      print 'You are now following: ' + follower + ' now!'

                elif msg == 'C':
                   message = prompt()
                   hash = hashtag()
                   if len( message + hash) <= 140:
                      s.send(name + ': ' + message + hash)
                   else:
                      print 'Cannot send because it\'s over 140 characters!\n'
                elif msg == 'D':
                   hashsearch = raw_input('Enter the Hashtag you would like to search') 
                   s.send('HASH: ' + hashsearch)
                   hash = s.recv(1024)
                   print hash

                elif msg == 'E':
                   print 'Goodbye!'
                   s.close()
                   sys.exit()
