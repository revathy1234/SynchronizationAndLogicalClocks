#Revathy Ramamoorthy
#https://pymotw.com/2/socket/tcp.html
#https://www.youtube.com/watch?v=SepyXsvWVfo
#http://effbot.org/tkinterbook/label.htm
import socket
import threading
from tkinter import *
import select
import time


client_num = {}		#Dictionary to store connected clients and their socket details
message=''
a={}				#Dictionary to store users and their port numbers

#server gui
def gui():
    win = Tk()
    win.geometry('500x500')
    print("GUI started")
    global vLabel					#Declaring label and variable
    global b
    headerLabel = Label(win, text="Server GUI", fg="blue", font=("Helvetica", 16))
    headerLabel.pack()
    vLabel = StringVar()
    b = Label(win, textvariable=vLabel, fg="blue", font=("Helvetica", 16))  	#Label to display message
    button = Button(win, text='close', width=30, command=win.quit())		#To close the connection
    b.pack()
    button.pack()
    win.mainloop()


#function facilitating server to connect to the clients
def server_connection():
	while(1):
		try:
			connection, client_address=server.accept()		#Accepting the client
			print(client_address[1])						#Displaying client port number
			data1 = connection.recv(1024).decode('utf8')	#Registration with username
			source_client = str(data1)
			print('Source_client:'+source_client)			
			client_num[source_client] = connection          #Storing client details
			a[source_client]=client_address[1]
			print(client_num)
			print(a)
			threading.Thread(target=server_send, args=(connection, address)).start()  #thread to handle receiving and sending messages
		except select.error:  #error handling
			print("error")
			server.close()

#function for sending and receiving messages between clients
def server_send(connection,address):
	while(1):
		try:
			data2 = connection.recv(1024).decode('utf-8')	#Receiving destination client name from source client
			dest_client = str(data2)
			data3 = connection.recv(1024).decode('utf-8')	#Receiving time from client
			t = str(data3)
			data4 = connection.recv(1024).decode('utf-8')	#Receiving username again from client for sending to destination
			usr = str(data4)
			if(t!="no"):
				final_message = ''
				date = ''
				date = time.strftime("%a, %d %b %Y %H:%M:%S")	#function to current calcualte date and time
				final_message = 'HTTP POST/1.1 200 OK\n'+date+'\nContent-Type: test/xml; charset="utf-8"\nhost: 127.0.0.1:5000\nUser-Agent:Socket-Client\n'+ str(t)
				vLabel.set(final_message);			#displaying message in HTTP format on GUI
				print('Message:\n'+t)
				message2=usr +","+ t 			   #one to one message delivery
				for sock in client_num:
					if sock==dest_client:
						client_num[sock].send(message2.encode('utf-8'))
						print("sent")
			else:
				if sock==usr:
					print(client_num[sock]+" disconnected")
					client_num[sock].close()
		except select.error:				#exception handling
			print("error")
			server.close()



#main function with threading to handle multiple concurrent client connection
if __name__ == '__main__':
	serverIP = '127.0.0.1'
	port = 5000
	address = (serverIP, port)
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(address)
	server.listen(3)
	print("listening")
	threading.Thread(target=server_connection).start()
	gui()