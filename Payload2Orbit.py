#Payload2Orbit
from tkinter import *
import math, tkinter.messagebox

root = Tk()
root.title("Payload2Orbit")
root.geometry("500x300")

def database(inp,sub):
    # Function takes the selected LV and sets values for specific impulse, liftoff mass, and structural mass
    if inp == "Space Shuttle":
        if sub == "Lightweight ET":
            isp1,isp2,mo1,fs1,fs2 = 250, 450, 2000000, 0.08, 0.08
        if sub == "Super Lightweight ET":
            isp1,isp2,mo1,fs1,fs2 = 250, 450, 2000000, 0.08,0.075

    if inp == "Falcon 9":
        if sub == "Expended":
            isp1,isp2,mo1,fs1,fs2 = 283,348,549000,0.10,0.05
        if sub == "ASDS Landing":
            isp1,isp2,mo1,fs1,fs2 = 283,348,549000,0.21,0.05
        if sub == "RTLS Landing":
            isp1,isp2,mo1,fs1,fs2 = 283,348,549000,0.27,0.05
    if inp == "New Glenn":
        if sub == "Expended":
            isp1,isp2,mo1,fs1,fs2 = 310,445, 1400000, 0.12,0.09
        if sub == "ASDS Landing":
            isp1,isp2,mo1,fs1,fs2 = 310,445, 1400000, 0.33,0.09
    if inp == "Starship":
        if sub == "Expended":
            isp1,isp2,mo1,fs1,fs2 = 347, 376,5000000, 0.08, 0.08
        if sub == "First Stage Reuse":
            isp1,isp2,mo1,fs1,fs2 = 347, 376,5000000, 0.19, 0.08         
        if sub == "Both Stages Reuse":
            isp1,isp2,mo1,fs1,fs2 = 347, 376,5000000, 0.19, 0.12
            
    if inp == "Electron":
        isp1,isp2,mo1,fs1,fs2 = 311, 343, 13000, 0.07, 0.05

    
    return [isp1,isp2,mo1,fs1,fs2]

def payload2orbit(inp,sub,ls,dvTotal,inclination,lat):
    # Function takes values for specific impulse, liftoff mass, structural mass, dV requirements, and launch inclination
    #to calculate payload to orbit
    isp1,isp2,mo1,fs1,fs2 = database(inp,sub)
    g = 9.81
    lat = float(lat*math.pi/180)
    inclination = float(inclination*math.pi/180.0)
    azimuth = (math.cos(inclination)/math.cos(lat))
    dvTotal += float(ls*(azimuth))
    dV = dvTotal*0.25
    dVs2 = dvTotal - dV
    a = (math.e**((dV/(isp1*g)))-fs1)/(1-fs1)
    b = (math.e**((dVs2/(isp2*g)))-fs2)/(1-fs2)
    payload = round(mo1*a*b,-1)
    if inp == "Space Shuttle":
        payload -= 100000
    if payload < 0:
        payload = 0

    return(int(payload))


def subdropmenu():
    # Function disables previous drop down menus and displays the sub dropdown menus
    # then, takes inputs for orbits, and launch vehicles from dropdowns
    drop.config(state="disabled")
    lsdrop.config(state="disabled")
    orbitdrop.config(state="disabled")
    enterinc.grid(row = 6, column = 1, columnspan = 1)
    inc.grid(row = 7, column = 1, columnspan=1)
    #assigns rotational velocity based on latitude
    if clickedls.get() == "Cape Canaveral (USA)":
        lsDV,lat = 410.0, 28.47
    if clickedls.get() == "Vandenberg AFB (USA)":
        lsDV, lat = 382.0, 34.74
    if clickedls.get() == "Spacex Boca Chica (USA)":
        lsDV, lat = 441.0, 18.45
    if clickedls.get() == "Mahia (New Zealand)":
        lsDV, lat = 361.0, 39.08
    if clickedls.get() == "Wallops (USA)":
        lsDV, lat = 367.0, 37.88
    #assigns dV requirements based on selected orbit
    if clickedorbit.get() == "LEO":
        dvTotal = -9000.0

    if clickedorbit.get() == "GTO":
        dvTotal = -11400.0
    
    if clickedorbit.get() == "GEO":
        dvTotal = -12800.0
    
    if clickedorbit.get() == "TLI":
        dvTotal = -12100.0

    if clickedorbit.get() == "TMI":
        dvTotal = -12600.0
    #creates drop down menus depending on the LV selection
    if clicked.get() == "Falcon 9":
        subdrop = OptionMenu(root,subclicked,*falconoptions)
        subclicked.set("Expended")
        subdrop.config(width=35,borderwidth=5)
        subdrop.grid(row=3,column=1)
    
    if clicked.get() == "New Glenn":
        subdrop = OptionMenu(root,subclicked,*glennoptions)
        subclicked.set("Expended")
        subdrop.config(width = 35, borderwidth = 5)
        subdrop.grid(row = 3, column = 1)

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

    button.config(text = "Next", command = lambda: show(subclicked.get(),lsDV,dvTotal,lat))
    button.grid(row = 1, column = 0)
    back.config(command = lambda: reset(subdrop))
    
def show(clickvar,ls,dvTotal,lat):
    # Function displays the calculated payload to orbit mass
    try:
        inclination = int(inc.get())
    except ValueError:
        inclination = 0
    e.config(state="normal")
    e.delete(0,'end')
    e.insert(0,(payload2orbit(clicked.get(),clickvar,ls,dvTotal,inclination,lat),"Kg"))
    e.config(state="disabled")


def reset(subdrop):
    # Function resets the calculator back to the start to select new settings
    button.config(text = "Next", command = lambda: subdropmenu())
    e.config(state="normal")
    e.delete(0,'end')
    e.config(state="disabled")
    drop.config(state="active")
    lsdrop.config(state="active")
    orbitdrop.config(state="active")
    try:
        subdrop.grid_forget()
    except AttributeError:
        pass
    inc.delete(0,'end')
    inc.grid_forget()
    enterinc.grid_forget()

# Dropdown menu options
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
    "Spacex Boca Chica (USA)",
    "Wallops (USA)",
    "Mahia (New Zealand)"
]
options = [
    "Falcon 9",
    "New Glenn",
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
glennoptions = [
    "Expended",
    "ASDS Landing"
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


# setting the default for the dropdown menus and allowing the values selected to be returned later
clickedorbit = StringVar()
clickedorbit.set("LEO")

clickedls = StringVar()
clickedls.set("Cape Canaveral (USA)")

clicked = StringVar()
clicked.set("Falcon 9")

subclicked = StringVar()
subclicked.set(" ")

# initializing the dropdown menus
orbitdrop = OptionMenu(root,clickedorbit,*orbitoptions)
orbitdrop.config(width = 35,borderwidth=5)
orbitdrop.grid(row = 1, column = 1, columnspan= 1)

lsdrop = OptionMenu(root,clickedls,*launchsite_options)
lsdrop.config(width = 35, borderwidth = 5)
lsdrop.grid(row = 2, column = 1,columnspan=1)

drop = OptionMenu(root,clicked,*options)
drop.config(width=35,borderwidth=5)
drop.grid(row = 3, column = 1,columnspan=1)

# initializing buttons
button = Button(root,text = "Next", command = lambda: subdropmenu())
button.grid(row = 1, column = 0)

back = Button(root,text="Back")
back.grid(row=2,column =0)

quit = Button(root,text = "Quit", command = root.quit)
quit.grid(row=1,column=5)

# initializing entry boxes
e = Entry(root, width=35, borderwidth=5,state = "disabled")
e.grid(row = 9, column = 1)

inc = Entry(root,width = 35,borderwidth=5)

# initializing labels
enterinc = Label(root,text = "Enter orbital inclination (Deg)")

payloadlabel = Label(root,text = "Payload to orbit is")
payloadlabel.grid(row = 8, column = 1)

heading = Label(root,text = "Payload to Orbit Calculator")
heading.grid(row = 0,column = 1)

root.mainloop()
