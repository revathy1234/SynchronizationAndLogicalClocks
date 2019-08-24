#Revathy Ramamoorthy
#https://realpython.com/python-sockets/
#https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
#https://www.geeksforgeeks.org/socket-programming-python/
#https://stackabuse.com/basic-socket-programming-in-python/
#https://www.youtube.com/watch?v=SepyXsvWVfo
#https://stackoverflow.com/questions/2905965/creating-threads-in-python
#https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
#https://www.tutorialspoint.com/python/python_gui_programming.htm
#http://effbot.org/tkinterbook/label.htm
import socket
import threading
from tkinter import *
import select


#client gui

def gui():
    win = Tk()
    win.geometry('300x400')
    print("GUI started")
    global vLabel					#Declaring labels for display
    global b
    global aLabel
    global c
    global headerLabel
    global srLabel
    srLabel = StringVar()
    srLabel.set("Client GUI");
    headerLabel = Label(win, textvariable=srLabel, fg="blue", font=("Helvetica", 16))		#Displaying sender/receiver GUI
    headerLabel.pack()
    vLabel = StringVar()
    aLabel = StringVar()
    b = Label(win, textvariable=vLabel, fg="blue", font=("Helvetica", 16)) #Label to display message
    #vLabel.set("")
    c = Label(win, textvariable=aLabel, fg="blue", font=("Helvetica", 16))
    button = Button(win, text='close', width=30, command=win.quit())	 #To close the connection
    b.pack()
    c.pack()
    button.pack()
    win.mainloop()


#function to check whether clock adjustment is necessary or not
def check(sent_time,received_time):					
		sent_time=int(sent_time)
		a=''
		a='Adjustment necessary'
		b=''
		b='No Adjustment necessary'
		if(sent_time == received_time):				#handles sending time being equal to the receiving time scenario
			print("Adjustment necessary: 1 unit"+'\n'+"Adjusted local time is :")
			aLabel.set(a)							#displaying adjustment decision on GUI
			f=received_time+1
			print(f)
			return received_time+1
		elif(sent_time < received_time):			#handles sending time being less than the receiving time scenario
			print("No adjustment necessary")		
			aLabel.set(b)							#displaying adjustment decision on GUI
			return received_time
		else:										#handles sending time being greater than the receiving time scenario
			print("Adjustment necessary, units are :")
			adj=''
			e=sent_time-received_time+1
			print(e)
			aLabel.set(a)							#displaying adjustment decision on GUI
			adj=sent_time+1
			print("Adjusted local time is :")
			print(adj)
			return adj

#function performing connection to server
def client_connection():
	t=0
	try:
		host = '127.0.0.1'
		port = 5000
		global client
		client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Client socket creation
		client.connect((host,port))      #Connection
		print("connected")
		s_name = input("Enter UserName\t")
		sc_name=s_name
		client.send(s_name.encode('utf8'))		#Sending username - Registration
		while (1):
			choice=''
			a=input("press 1 to send 2 to receive\t")
			if(a=="1") :
				srLabel.set("Sender GUI");		#Resetting all labels
				aLabel.set('');
				vLabel.set('');
				while (1):						#Counter for sender client
					t=t+4						#incrementing counter by 4 for each tick of clock
					print(t)				
					choice=input("Enter C to continue ticking OR Enter SEND to send time\t")
					if(choice=="c") :
						continue
					else :
						break
				dest=''
				dest=input("Enter destination client name\t")
				client.send(dest.encode('utf-8')) #Sending destination client name to server
				client.send(str(t).encode('utf-8'))	#Sending time
				print("Sent successfully\n")
				here=''
				here=dest+","+str(t)
				vLabel.set(here);					#Displaying sent details on GUI
				client.send(s_name.encode('utf8'))  #Sending username
				
			elif(a=="2"):
				srLabel.set("Receiver GUI");		#Resetting all labels
				vLabel.set('');
				aLabel.set('');
				while (1):							#Counter for receiver client
					t=t+4							#incrementing counter by 4 for each tick of clock
					print(t)						
					choice=input("Enter C to continue ticking OR Enter RECEIVE to receive time\t")
					if(choice=="c") :
						continue
					else :
						break
				data=client.recv(1024).decode('utf-8')			#Receiving time
				b,c=data.split(",")
				print(b)
				print(c)
				sent_time=str(c)
				vLabel.set(data);								#Displaying received details on GUI
				t=check(sent_time,t)
			else:
				print("enter the correct choice")
				continue
			ans = input('\nDo you want to continue(y/n) :') 
			if (ans == 'y'):
				continue
			else:
				sd="no"
				client.send(sd.encode('utf-8'))
				client.send(sc_name.encode('utf-8'))
				break
	except select.error:					#error handling
		print("error")
		client.close()

#main function forking a thread for each new client
if __name__ == '__main__':
	threading.Thread(target=client_connection).start() #Starting thread
	gui()

