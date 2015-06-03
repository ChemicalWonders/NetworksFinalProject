# Twitter Server - CS 164 Final Project
# by Kevin Chan - 861009116

import socket
import select
import sys

#Added a new Class for Username and Password Combinations
class User: 
   def __init__(self, name, pwd):
       self.name = name
       self.pwd = pwd
   
   def change_pwd(self, pwd):
       self.pwd = pwd


#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)
 
if __name__ == "__main__":
    
    if(len(sys.argv) < 2):
       print 'Usage : python server.py port'
       sys.exit()
    a = ['alpha', 'abcde']
    b = ['beta' , 'aabbcc']
    c = ['omega', 'abcabc']
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

                #broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
             
            #Some incoming message from a client
            else : 
                # Data recieved from client, process it
                try:
                    #data that needs to be broadcasted to followers
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast_data(sock, "\r" + data + "\n")                

                 
                except:
                    #broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    #print "Client (%s, %s) is offline" % addr
                    sock.close()
                    #CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()
