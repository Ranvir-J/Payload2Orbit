#Payload2Orbit
from tkinter import *
import math, tkinter.messagebox

root = Tk()
root.title("Payload2Orbit")
root.geometry("500x500")

def database(inp,sub):
    if inp == "Space Shuttle":
        if sub == "Lightweight ET":
            isp1,isp2,mo1,fs1,fs2 = 250, 450, 2000000, 0.08, 0.05
        if sub == "Super Lightweight ET":
            isp1,isp2,mo1,fs1,fs2 = 250, 450, 2000000, 0.08,0.045

    if inp == "Falcon 9":
        if sub == "Expended":
            isp1,isp2,mo1,fs1,fs2 = 283,348,549000,0.1,0.05
        if sub == "ASDS Landing":
            isp1,isp2,mo1,fs1,fs2 = 283,348,549000,0.21,0.05
        if sub == "RTLS Landing":
            isp1,isp2,mo1,fs1,fs2 = 283,348,549000,0.29,0.05

    if inp == "Starship":
        if sub == "Expended":
            isp1,isp2,mo1,fs1,fs2 = 347, 376,5000000, 0.08, 0.08
        if sub == "First Stage Reuse":
            isp1,isp2,mo1,fs1,fs2 = 347, 376,5000000, 0.19, 0.08         
        if sub == "Both Stages Reuse":
            isp1,isp2,mo1,fs1,fs2 = 347, 376,5000000, 0.19, 0.12

    if inp == "Falcon Heavy":
        if sub == "Expended":
            isp1,isp2,mo1,fs1,fs2 = 283, 348, 1420000, 0.08, 0.05
        if sub == "Side Boosters RTLS":
            isp1,isp2,mo1,fs1,fs2 = 283, 348, 1420000, 0.24, 0.05
        if sub == "Core Booster ASDS Landing":
            isp1,isp2,mo1,fs1,fs2 = 283, 348, 1420000, 0.35, 0.05
            
    if inp == "Electron":
        isp1,isp2,mo1,fs1,fs2 = 311, 343, 13000, 0.08, 0.08
    

    return [isp1,isp2,mo1,fs1,fs2]

def payload2orbit(inp,sub,ls,dvTotal,inclination):
    isp1,isp2,mo1,fs1,fs2 = database(inp,sub)
    g = 9.81
    dvTotal += ls*math.cos(inclination)
    dV = -2250
    dVs2 = dvTotal + 2250
    a = (math.e**((dV/(isp1*g)))-fs1)/(1-fs1)
    b = (math.e**((dVs2/(isp2*g)))-fs2)/(1-fs2)
    payload = round(mo1*a*b,-2)
    if inp == "Space Shuttle":
        payload -= 100000
    return(int(payload))


def subdropmenu():
    drop.config(state="disabled")
    lsdrop.config(state="disabled")
    orbitdrop.config(state="disabled")
    inc.grid(row = 5, column = 1, columnspan=1)

    try:
        inclination = int(inc.get())
    except ValueError:
        inclination = 0
    print(inc.get())
    if clickedorbit.get() == "LEO":
        dvTotal = -9000

    if clickedorbit.get() == "GTO":
        dvTotal = -11400
    
    if clickedorbit.get() == "GEO":
        dvTotal = -12800
    
    if clickedorbit.get() == "TLI":
        dvTotal = -12100

    if clickedorbit.get() == "TMI":
        dvTotal = -12600

    if clickedls.get() == "Cape Canaveral (USA)":
        lsDV = 410 
    
    if clickedls.get() == "Vandenberg AFB (USA)":
        lsDV = -382
    
    if clickedls.get() == "Spacex Boca Chica (USA)":
        lsDV = 440

    if clicked.get() == "Falcon 9":
        subdrop = OptionMenu(root,subclicked,*falconoptions)
        subclicked.set("Expended")
        subdrop.config(width=35,borderwidth=5)
        subdrop.grid(row=3,column=1)

    if clicked.get() == "Space Shuttle":
        subdrop = OptionMenu(root,subclicked,*shuttleoptions)
        subclicked.set("Lightweight ET")
        subdrop.config(width=35,borderwidth=5)
        subdrop.grid(row=3,column=1)

    if clicked.get() == "Starship":
        subdrop = OptionMenu(root,subclicked,*starshipoptions)
        subclicked.set("Expended")
        subdrop.config(width=35,borderwidth=5)
        subdrop.grid(row=3,column=1)

    if clicked.get() == "Electron":
        subdrop = " "
        show(subdrop,lsDV,dvTotal,inclination)

    if clicked.get() == "Falcon Heavy":
        subdrop = OptionMenu(root,subclicked,*fhoptions)
        subclicked.set("Expended")
        subdrop.config(width=35,borderwidth=5)
        subdrop.grid(row = 3, column = 1)
    
    button.config(text = "Next", command = lambda: show(subclicked.get(),lsDV,dvTotal,inclination))
    button.grid(row = 1, column = 0)
    back.config(command = lambda: reset(subdrop))
    
def show(clickvar,ls,dvTotal,inclination):
    e.config(state="normal")
    e.delete(0,'end')
    e.insert(0,(payload2orbit(clicked.get(),clickvar,ls,dvTotal,inclination),"Kg"))
    e.config(state="disabled")


def reset(subdrop):
    button.config(text = "Next", command = lambda: subdropmenu())
    e.config(state="normal")
    e.delete(0,'end')
    e.config(state="disabled")
    drop.config(state="active")
    lsdrop.config(state="active")
    orbitdrop.config(state="active")
    subdrop.grid_forget()
    inc.delete(0,'end')
    #inc.insert(0,"Enter Orbital Inclination (deg)")
    inc.grid_forget()


orbitoptions = [
    "LEO",
    "GTO",
    "GEO",
    "TLI",
    "TMI"
]
launchsite_options = [
    "Cape Canaveral (USA)",
    "Vandenberg AFB (USA)",
    "Spacex Boca Chica (USA)"
]
options = [
    "Falcon 9",
    "Falcon Heavy",
    "Starship",
    "Space Shuttle",
    "Electron"
]
empty = [" "]
falconoptions = [
    "Expended",
    "ASDS Landing",
    "RTLS Landing"
]
shuttleoptions = [
    "Lightweight ET",
    "Super Lightweight ET"
]
starshipoptions = [
    "Expended",
    "First Stage Reuse",
    "Both Stages Reuse"
]
fhoptions = [
    "Expended",
    "Side Boosters RTLS",
    "Core Booster ASDS Landing"
]

clickedorbit = StringVar()
clickedorbit.set("LEO")

clickedls = StringVar()
clickedls.set("Cape Canaveral (USA)")

clicked = StringVar()
clicked.set("Falcon 9")

subclicked = StringVar()
subclicked.set(" ")

orbitdrop = OptionMenu(root,clickedorbit,*orbitoptions)
orbitdrop.config(width = 35,borderwidth=5)
orbitdrop.grid(row = 1, column = 1, columnspan= 1)

lsdrop = OptionMenu(root,clickedls,*launchsite_options)
lsdrop.config(width = 35, borderwidth = 5)
lsdrop.grid(row = 2, column = 1,columnspan=1)

drop = OptionMenu(root,clicked,*options)
drop.config(width=35,borderwidth=5)
drop.grid(row = 3, column = 1,columnspan=1)

button = Button(root,text = "Next", command = lambda: subdropmenu())
button.grid(row = 1, column = 0)

back = Button(root,text="Back")
back.grid(row=2,column =0)

quit = Button(root,text = "Quit", command = root.quit)
quit.grid(row=1,column=5)

e = Entry(root, width=35, borderwidth=5,state = "disabled")
e.grid(row = 7, column = 1)

inc = Entry(root,width = 35,borderwidth=5)


heading = Label(root,text = "Payload to Orbit Calculator")
heading.grid(row = 0,column = 1)

root.mainloop()
