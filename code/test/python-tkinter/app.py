import tkinter

def capture():
    print('Capture Mode')
    lblMenu['text'] = 'capture'

def liveView():
    print('Live View Mode')
    lblMenu['text'] = 'LIVE'


mainMenu = tkinter.Tk()
mainMenu.title("PIBITI-2019")

#dimensoes da janela
windowWidth = 480
windowHeight = 320
screenWidth = mainMenu.winfo_screenwidth()
screenHeight = mainMenu.winfo_screenheight()
posx =screenWidth/2 - windowWidth/2 
posy =screenHeight/2 - windowHeight/2

mainMenu.geometry("%dx%d+%d+%d" % (windowWidth,windowHeight,posx,posy))
mainMenu.minsize(width = windowWidth, height = windowHeight)

#aparencia

mainMenu.iconbitmap("code/resources/icon/if.ico")
#mainMenu.state("zoomed") 
#mainMenu['bg'] = "gray"

#
# Widgets da janela
#

#inicializacao DE WIDGETS
btnCapture = tkinter.Button(mainMenu, text = "Capture", command = capture)
btnLive    = tkinter.Button(mainMenu, text = "Live View", command = liveView)
lblMenu    = tkinter.Label(
                mainMenu,
                text = "What do you want to do?", 
                relief = "groove",
                font = "Arial 30 bold",
                justify = "left",
                width = "50",
                height = 2,
                anchor = 'w')

#GRID



#pack

lblMenu.pack()
btnCapture.pack()
btnLive.pack()

mainMenu.mainloop()