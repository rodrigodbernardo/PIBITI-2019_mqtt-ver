import tkinter

def capture():
    print('Capture Mode')
    lblMenu['text'] = 'capture'

def liveView():
    print('Live View Mode')
    lblMenu['text'] = 'LIVE'


mainWindow = tkinter.Tk()
mainWindow.title("PIBITI-2019")

#dimensoes da janela
windowWidth = 480
windowHeight = 320
screenWidth = mainWindow.winfo_screenwidth()
screenHeight = mainWindow.winfo_screenheight()
posx =screenWidth/2 - windowWidth/2 
posy =screenHeight/2 - windowHeight/2

mainWindow.geometry("%dx%d+%d+%d" % (windowWidth,windowHeight,posx,posy))
mainWindow.minsize(width = windowWidth, height = windowHeight)

#aparencia

mainWindow.iconbitmap("code/resources/icon/if.ico")
#mainWindow.state("zoomed") 
#mainWindow['bg'] = "gray"

#
# Widgets da janela
#

#inicializacao DE WIDGETS
'''
btnCapture = tkinter.Button(mainWindow, text = "Capture", command = capture)
btnLive    = tkinter.Button(mainWindow, text = "Live View", command = liveView)
lblMenu    = tkinter.Label(
                mainWindow,
                text = "What do you want to do?", 
                relief = "groove",
                font = "Arial 30 bold",
                justify = "left",
                width = "50",
                height = 2,
                anchor = 'w')
'''
#label
tkOperation    = tkinter.Label(mainWindow, bg = "blue",text="Operation").grid(row=0,column=0,sticky="we")
#


#-------------------
#widgets

tkProprierties = tkinter.Label(mainWindow, bg = "green",text="Proprierties").grid(row=0,column=1,sticky="we")

    #tkLabelCapt = tkinter.Label(mainWindow,text="Number of Captures:")
    #tkEntryCapt = tkinter.Entry(mainWindow)
    #tkLabelSample = tkinter.Label(mainWindow,text="Number of Samples:")
    #tkEntrySample = tkinter.Entry(mainWindow)
    #tkLabelRate = tkinter.Label(mainWindow,text="Sample Rate(ms):")
    #tkEntryRate = tkinter.Entry(mainWindow)

tkAdditional   = tkinter.Label(mainWindow, bg = "gray",text="Additional").grid(row=1,column=0,sticky="we")

    #tkButtonCommand = tkinter.Button(mainWindow,text="SEND COMMAND",command = sendModeToSensor)

tkTerminal     = tkinter.Label(mainWindow, bg = "red",text="Terminal").grid(row=1,column=1,sticky="we")

#-------------------
#GRID


#-------------------
#pack

##lblMenu.pack()
##btnCapture.pack()
#btnLive.pack()

mainWindow.mainloop()