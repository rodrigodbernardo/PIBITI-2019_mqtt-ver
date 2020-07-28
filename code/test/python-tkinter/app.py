import tkinter

def func():
    print('Hey')



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

#inicializacao
btn = tkinter.Button(mainMenu, text = "OK", command = func)
btn2 = tkinter.Button(mainMenu, text = "OK", command = func)
lbl1 = tkinter.Label(mainMenu, text = "Este é um texto.")


#pack

btn.pack()
btn2.pack()
lbl1.pack()

mainMenu.mainloop()