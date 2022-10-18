import socket
from threading import Thread
from tkinter import *
from tkinter import ttk



nameLabel=None
listBox=None
textArea=None
labelChat=None
entryBox=None
textMsg=None
filePathLabel = None
sending_file=None

def openChatWindow():

    global nameLabel
    global listBox
    global textArea
    global labelChat
    global textMsg
    global filePathLabel
    global entryBox
    

    window=Tk()
    window.title("Message")
    window.geometry("500x350")

    nameLabel = Label(window,text="Enter Your name",font=("Times New Roman",40))
    nameLabel.place(x=10,y=8)

    entryBox=Entry(window,width=20,font=("Times New Roman",40))
    entryBox.place(x=520,y=8)
    entryBox.focus()

    connectServer=Button(window,text="conntect to chat server",bd=2,font=("Times New Roman",40),command=connectToServer)
    connectServer.place(x=1280,y=8)


    separator = ttk.Separator(window,orient="horizontal")
    separator.place(x=0,y=120,relwidth=1,height=0.1)

    labelUsers = Label(window,text="Active Users",font=("Times New Roman",40))
    labelUsers.place(x=0,y=150)

    listBox=Listbox(window,height=3,width=80,font=("Times New Roman",40))
    listBox.place(x=20,y=220)
    scrollbar1=Scrollbar(listBox)
    scrollbar1.place(relheight=1,relx=1)
    scrollbar1.config(command=listBox.yview)

    connect=Button(window,text="Connect",bd=2,font=("Times New Roman",30))
    connect.place(x=900,y=450)

    disconnect=Button(window,text="Disconnect",bd=2,font=("Times New Roman",30))
    disconnect.place(x=1100,y=450)

    refresh=Button(window,text="Refresh",bd=2,font=("Times New Roman",30),command=showClientsList)
    refresh.place(x=1400,y=450)

    chatUsers = Label(window,text="Chat Window",font=("Times New Roman",40))
    chatUsers.place(x=0,y=510)

    textArea=Text(window,height=5,width=100,font=("Times New Roman",40))
    textArea.place(x=20,y=600)
    scrollbar2=Scrollbar(textArea)
    scrollbar2.place(relheight=1,relx=1)
    scrollbar2.config(command=textArea.yview)

    Attach=Button(window,text="Attach And Send",bd=2,font=("Times New Roman",40))
    Attach.place(x=20,y=900)

    entryBox1=Entry(window,width=40,font=("Times New Roman",40))
    entryBox1.place(x=500,y=940)
    entryBox1.focus()

    send=Button(window,text="Send",bd=2,font=("Times New Roman",40))
    send.place(x=1550,y=900)


    window.resizable(True,True)

    window.mainloop()

def receiveMessage():
    global SERVER
    global BUFFER_SIZE

    while True:
        # its stores the buffer size of the data reserveed by
        chunk = SERVER.recv(BUFFER_SIZE)
        try:
            if("tiul" in chunk.decode() and "1.0," not in chunk.decode()):
                letter_list = chunk.decode().split(",")
                listBox.insert(letter_list[0],letter_list[0]+":"+letter_list[1]+": "+letter_list[3]+" "+letter_list[5])
                print(letter_list[0],letter_list[0]+":"+letter_list[1]+": "+letter_list[3]+" "+letter_list[5])
            else:
                textArea.insert(END,"\n"+chunk.decode('ascii'))
                textArea.see("end")
                print(chunk.decode('ascii'))
        except:
            pass


def showClientsList():
    global listBox
    listBox.delete(0,"end")
    SERVER.send("show list".encode("ascii"))



def connectToServer():
    global sending_file
    global SERVER
    global entryBox

    cname = entryBox.get()
    SERVER.send(cname.encode())



PORT  = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096





def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))


    receive_thread = Thread(target=receiveMessage)               #receiving multiple messages
    receive_thread.start()

    openChatWindow()
setup()


#-----------Bolierplate Code Start -----