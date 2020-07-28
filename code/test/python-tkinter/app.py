import tkinter as tk
from tkinter import ttk

i = 0
def capture():
    print('Capture Mode')
    lblMenu['text'] = 'capture'

def liveView():
    print('Live View Mode')
    lblMenu['text'] = 'LIVE'

def sendButtonPressed():
    print('Button pressed')
    label_command['text'] = 'Button pressed!'
    nCapture = entry_capture.get()
    nSamples = entry_sample.get()
    sampleRate = entry_rate.get()

    print(nCapture)
    print(nSamples)
    print(sampleRate)

    global i
    i += 1
    print(i)
    bar_var.set(i)
 

mainWindow = tk.Tk()
mainWindow.title("PIBITI-2019")

#dimensoes da janela
windowWidth = 480
windowHeight = 320
screenWidth = mainWindow.winfo_screenwidth()
screenHeight = mainWindow.winfo_screenheight()
posx =screenWidth/2 - windowWidth/2 
posy =screenHeight/2 - windowHeight/2

#mainWindow.geometry("%dx%d+%d+%d" % (windowWidth,windowHeight,posx,posy))
#mainWindow.minsize(width = windowWidth, height = windowHeight)

#aparencia

mainWindow.iconbitmap("code/resources/icon/if.ico")
#mainWindow.state("zoomed") 
#mainWindow['bg'] = "gray"

#
# Widgets da janela
#

#inicializacao DE WIDGETS
'''
btnCapture = tk.Button(mainWindow, text = "Capture", command = capture)
btnLive    = tk.Button(mainWindow, text = "Live View", command = liveView)
lblMenu    = tk.Label(
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

#


#-------------------
#widgets

##OPERATION frame

frame_operation = tk.Frame(mainWindow)

### widgets

label_operation = tk.Label(frame_operation, bg = "blue",text="Operation")

label_capture = tk.Label(frame_operation,text="Number of Captures:")
entry_capture = tk.Entry(frame_operation)
label_sample = tk.Label(frame_operation,text="Number of Samples:")
entry_sample = tk.Entry(frame_operation)
label_rate = tk.Label(frame_operation,text="Sample Rate(ms):")
entry_rate = tk.Entry(frame_operation)

### layout

label_operation.grid(sticky="we",rowspan=2)

label_capture.grid(sticky='we')
entry_capture.grid(sticky='we')
label_sample.grid(sticky='we')
entry_sample.grid(sticky='we')
label_rate.grid(sticky='we')
entry_rate.grid(sticky='we')


##Graphic Frame


##ADDITIONAL Frame
frame_additional = tk.Frame(mainWindow)

### widgets
label_additional = tk.Label(frame_additional,text = "ADDITIONAL",bg = 'blue')

button_command = tk.Button(frame_additional,text="SEND\nCOMMAND",command = sendButtonPressed)#lambda: sendButtonPressed(i))
label_command = tk.Label(frame_additional,text = '\n\n\n')
label_progress = tk.Label(frame_additional,text ='Progress')

bar_var = tk.DoubleVar()
bar_var.set(i)
bar_progress = ttk.Progressbar(frame_additional,variable=bar_var,maximum=10)

### layout
label_additional.grid(sticky='we',rowspan=2)

button_command.grid(sticky="we",rowspan=2)
label_command.grid(sticky='we')

label_progress.grid(sticky='we')
bar_progress.grid(sticky='we')

##TERMINAL ZONE

#tkTerminal     = tk.Label(mainWindow, bg = "red",text="Terminal")

#tkTerminal.grid(row=6,column=1,sticky="nswe",rowspan=3)

#tkAdditional.grid(row=6,column=0,sticky="we")

## GERAL
frame_operation.grid()
frame_additional.grid()

mainWindow.mainloop()