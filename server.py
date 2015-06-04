# Twitter Server - CS 164 Final Project
# by Kevin Chan - 861009116

import socket
import select
import sys
import re

messagecount = 0

portValues = {}

#Added a new Class for Username and Password Combinations
class User: 
   def __init__(self, name, pwd):
       self.name = name
       self.pwd = pwd
   
   def change_pwd(self, pwd):
       self.pwd = pwd

sublistA = ['beta', 'omega']
sublistB = ['alpha']
sublistC = []

messages = []
#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        #print socket
        if socket != server_socket and socket != sock :
            
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)


def hashtag_search (sock, message):
    for socket in CONNECTION_LIST:
        if socket == sock:
            try :
                socket.send(message)
            except:
                socket.close()
                CONNECTION_LIST.remove(socket)

def search(hashtag, list):
    for h in list:
        if h[hashtag] == hashtag:
            return h


if __name__ == "__main__":
    
    if(len(sys.argv) < 2):
       print 'Usage : python server.py port'
       sys.exit()
    a = ['alpha', 'abcde']
    b = ['beta' , '12345']
    c = ['omega', 'abc123']
    checkNames = [a,b,c];

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = int(sys.argv[1])
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print 'Chat server started on port ' + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])         
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                
                print "Client (%s, %s) connected" % addr
                 
                personfound = '0'
                while personfound == '0': 
                    #verification process
                    name = sockfd.recv(RECV_BUFFER)
                    print name
                    pwd =  sockfd.recv(RECV_BUFFER)
                    print pwd

                    currentUser = [name, pwd]

                    for index in range(len(checkNames)):
                        if currentUser == checkNames[index]:
                           print checkNames[index]
                           print 'Match indicated'
                           personfound = name
                           break
 
                        else :
                            print 'Match not found'

                    print personfound;
                    sockfd.send(personfound);
                portValues[personfound] = sock
                print portValues
                #broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
             
            #Some incoming message from a client
            else : 
                # Data recieved from client, process it
                try:
                    #data that needs to be broadcasted to followers
                    #print 'sock = ' + str(sock)
                    data = sock.recv(RECV_BUFFER)
                    #print data.split(':', '#')
                    if data:
                        splitData = re.split('[:#]', data)
                        if splitData[0] == 'HASH':
                            value = search(splitData[1], messages)
                            hashtag_search(sock, str(value))
                        
                        tweet = {}
                        tweet['author'] = splitData[0]
                        tweet['body'] = splitData[1]
                        tweet['hashtags'] = splitData[2:]
                        tweet['number'] = messagecount
                        #print tweet
                        messages.append(tweet)
                        print str(messages)
                        messagecount += 1
                        #print messagecount
                        
                        broadcast_data(sock, "\r" + data + "\n")                

                 
                except:
                    #broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    #print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()
