# "Animakeris 26" – animacijų piešimo programėlė – pieši animacijos kadrus, pasirenki FPS/(mili)sekundės per n kadrų ir sugeneruoja |.mp4|/|.gif| (PIL generuoja |.gif|/|.apng|, ffmpeg "binding"ai generuoja |.mp4|/|.mov|/t.t, tkinter daro main gui (|root|))
import tkinter as tk
import tkinter.messagebox as msgbox
from PIL import Image
import ffmpeg

ver = "26.2.22"
codename = "cow tools"

def abt():
	msgbox.showinfo(f"Animakeris 26 {ver} (\"{codename}\")",f"{getStr(9)}\n{getStr(10)} https://github.com/RixInGithub/animakeris26")

def exitPp():
	if enablePp:
		out = msgbox.askyesnocancel("Animakeris 26",getStr(5))
		if out == None: return # cancelled
	root.destroy()

def downEvt(e):
	global mDown, lastXy
	mDown = True
	lastXy = None
def upEvt(e):
	global mDown
	mDown = False

def onMove(e):
	global lastXy, mDown
	if not mDown: return
	sel = tools.curselection()[0]
	if sel == 0: # pencil
		if lastXy != None: cnv.create_line(lastXy[0], lastXy[1], e.x, e.y, fill="black")
		lastXy = [e.x, e.y]
		return
	if sel == 1: # eraser
		return # tbd
	# wait what

def getStr(n):
	try:
		return trans["en"][n]
	except: return "None" # idfk

enablePp = False
availableTools = [3, 4]
mDown = False
lastXy = None
trans = {
	"en": [
		"File",
		"Exit",
		"New",
		"Pencil",
		"Eraser",
		"Would you like to save before exiting?",
		"Edit",
		"Help",
		"About",
		"Made by Adas Jankus.",
		"Source available at:"
	],
	"lt": [
		"Failas"
	]
}
root = tk.Tk()
root.geometry("800x600")
root.title("Animakeris 26")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.protocol("WM_DELETE_WINDOW", exitPp)

menu = tk.Menu(root)

file = tk.Menu(menu, tearoff=0)
file.add_command(label=getStr(1), command=exitPp)
file.add_command(label=getStr(2), command=lambda: msgbox.showerror("Animakeris 26","tbd"))
menu.add_cascade(label=getStr(0), menu=file)

edit = tk.Menu(menu, tearoff=0)
menu.add_cascade(label=getStr(6), menu=edit)

help = tk.Menu(menu, tearoff=0)
help.add_command(label=getStr(8), command=abt)
menu.add_cascade(label=getStr(7), menu=help)

wrap1 = tk.Frame(root)
wrap1.rowconfigure(0, weight=1)
wrap1.columnconfigure(1, weight=1)
wrap2 = tk.Frame(wrap1, background="White") # wrapper for canvas
wrap2.rowconfigure(0, weight=1)
wrap2.columnconfigure(0, weight=1)
cnv = tk.Canvas(wrap2, width=500, height=400)
cnv.bind("<ButtonPress-1>", downEvt)
cnv.bind("<ButtonRelease-1>", upEvt)
cnv.bind("<Motion>", onMove)
cnv.grid(row=0, column=0)
wrap2.grid(row=0, column=1)
wrap3 = tk.Frame(wrap1, width=128) # wrapper for tools and tool opts
wrap3.rowconfigure(1, weight=1)
wrap3.columnconfigure(0, weight=1)
tools = tk.Listbox(wrap3, activestyle=tk.NONE, height=len(availableTools)) # tools
[tools.insert(tk.END, getStr(t)) for t in availableTools]
tools.selection_set(first=0)
tools.grid(row=0, column=0, sticky="nesw")
opts = tk.Frame(wrap3, bg="red")
opts.grid(row=1, column=0, sticky="nesw")
wrap3.grid(row=0, column=0, sticky="nesw")
wrap1.grid(row=0, column=0, sticky="nesw")

root.config(menu=menu)

root.mainloop()