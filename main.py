#!/usr/bin/env python
# "Animakeris 26" – animacijų piešimo programėlė – pieši animacijos kadrus, pasirenki FPS/(mili)sekundės per n kadrų ir sugeneruoja |.mp4|/|.gif| (PIL generuoja |.gif|/|.apng|, ffmpeg "binding"ai generuoja |.mp4|/|.mov|/t.t, tkinter daro main gui (|root|))
import tkinter as tk
import tkinter.messagebox as msgbox
from PIL import Image, ImageDraw, ImageTk
import ffmpeg

ver = "26.3.8"
codename = "me when the"
cachedFrm = None
cachedFCImg = None

def applyLang():
	global prevLang
	if lang.get() == prevLang: return # user clicked againz? whyz?
	lookup = {v: k for k, v in enumerate(trans[prevLang])} # god damn it
	aLangRecursiveW(root, lookup)
	aLangMenu(menu, lookup)
	retransTools()
	prevLang = lang.get()

def aLangRecursiveW(w, lookup):
	aLangW(w, lookup)
	for ch in w.winfo_children(): aLangRecursiveW(ch, lookup)

def aLangW(w, lTbl):
	for o in translatedCfg:
		try:
			curr = w.cget(o)
			if type(curr) == str and curr in lTbl and lTbl[curr] != 12:
				w.config(**{o: trans[lang.get()][lTbl[curr]]})
				continue
		except tk.TclError: pass

def aLangMenu(m, lTbl):
	end = m.index(tk.END)
	if end is None: return # "POOP YOURSELF!"
	count = 0
	while count <= end:
		try:
			curr = m.entrycget(count, "label")
			if curr in lTbl and lTbl[curr] != 12: m.entryconfig(count, label=trans[lang.get()][lTbl[curr]])
			ch = m.entrycget(count, "menu")
			if m.type(count) == "cascade" and ch: aLangMenu(m.nametowidget(ch), lTbl)
		except tk.TclError: pass
		count += 1

def retransTools():
	sels = tools.curselection()
	sel = 0
	if len(sels)>0: sel = sels[0]
	tools.delete(0, tk.END)
	[tools.insert(tk.END, getStr(t)) for t in availableTools]
	tools.selection_set(first=sel)

def recacheFrm():
	global cachedFrm
	cachedFrm = blankImg()
	for l in proj[selFrame][:selLayer]: cachedFrm.paste(l, l)

def blankImg(): return Image.new("RGBA", size)

def redrawCnv():
	global cachedFCImg
	new = cachedFrm.copy()
	new.paste(proj[selFrame][selLayer], proj[selFrame][selLayer])
	cnv.img = ImageTk.PhotoImage(new)
	if cachedFCImg is None:
		cachedFCImg = cnv.create_image(0,0,anchor="nw",image=cnv.img)
		return
	cnv.itemconfig(cachedFCImg, image=cnv.img)

def addFrame():
	proj.append([blankImg()])

def abt():
	msgbox.showinfo(f"Animakeris 26 {ver} (\"{codename}\")",f"{getStr(9)}\n\n{getStr(10)} https://github.com/RixInGithub/animakeris26")

def exitPp():
	if enablePp:
		out = msgbox.askyesnocancel("Animakeris 26",getStr(5))
		if out == None: return # cancelled
	root.destroy()

def downEvt(e):
	global mDown, lastXy
	mDown = True
	lastXy = None

def onMove(e):
	global lastXy, mDown
	if not mDown: return
	sel = tools.curselection()[0]
	if sel == 0 or sel == 1: # pencil AND eraser
		phil = "Black"
		if sel == 1: phil = (0,0,0,0) # always transparent eraser
		if lastXy != None:
			ImageDraw.Draw(proj[selFrame][selLayer]).line((lastXy[0], lastXy[1], e.x, e.y), fill=phil, width=10)
			redrawCnv()
		lastXy = [e.x, e.y]
		return
	if sel == 1: # eraser
		return # tbd
	# wait what

def getStr(n):
	try:
		return trans[lang.get()][n]
	except: return "⁇⁇" # idfk

translatedCfg = ["text", "value", "label", "content"]
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
		"An animation program made by Adas Jankus.",
		"Source available at:",
		"Change languages…",
		"English"
	],
	"lt": [
		"Failas",
		"Išjungti",
		"Nauja animacija",
		"Pieštukas",
		"Trintukas",
		"Ar norėtumete išsaugoti animaciją?",
		"Redaguoti",
		"Pagalba",
		"Apie programą",
		"Ado Jankaus programa, skirta kurti animacijas.",
		"Kodo repоzitorija:",
		"Keisti kalbą…",
		"lietuvių"
	]
}
root = tk.Tk()
lang = tk.StringVar(value="lt")
prevLang = lang.get()
root.geometry("800x600")
root.title("Animakeris 26")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.protocol("WM_DELETE_WINDOW", exitPp)
selFrame = 0
selLayer = 0
size = [500, 400]
proj = []
addFrame()

menu = tk.Menu(root)

file = tk.Menu(menu, tearoff=0)
file.add_command(label=getStr(1), command=exitPp)
file.add_command(label=getStr(2), command=lambda: msgbox.showerror("Animakeris 26","tbd"))
menu.add_cascade(label=getStr(0), menu=file)

edit = tk.Menu(menu, tearoff=0)
menu.add_cascade(label=getStr(6), menu=edit)

help = tk.Menu(menu, tearoff=0)
help.add_command(label=getStr(8), command=abt)
langs = tk.Menu(help, tearoff=0)
for l in trans.keys(): langs.add_radiobutton(label=trans[l][12], value=l, variable=lang, command=applyLang)
help.add_cascade(label=getStr(11), menu=langs)
menu.add_cascade(label=getStr(7), menu=help)

wrap1 = tk.Frame(root)
wrap1.rowconfigure(0, weight=1)
wrap1.columnconfigure(0, minsize=128)
wrap1.columnconfigure(1, weight=1)
wrap2 = tk.Frame(wrap1, background="White") # wrapper for canvas
wrap2.rowconfigure(0, weight=1)
wrap2.columnconfigure(0, weight=1)
cnv = tk.Canvas(wrap2, width=size[0], height=size[1])
recacheFrm()
redrawCnv()
cnv.bind("<ButtonPress-1>", downEvt)
# cnv.bind("<ButtonRelease-1>", upEvt)
cnv.bind("<B1-Motion>", onMove)
cnv.grid(row=0, column=0)
wrap2.grid(row=0, column=1)
wrap3 = tk.Frame(wrap1) # wrapper for tools and tool opts
wrap3.rowconfigure(1, weight=1)
wrap3.columnconfigure(0, weight=1)
tools = tk.Listbox(wrap3, activestyle=tk.NONE, height=len(availableTools), width=0) # tools
retransTools()
tools.grid(row=0, column=0, sticky="nesw")
opts = tk.Frame(wrap3, bg="red")
opts.grid(row=1, column=0, sticky="nesw")
wrap3.grid(row=0, column=0, sticky="nesw")
wrap1.grid(row=0, column=0, sticky="nesw")

root.config(menu=menu)

root.mainloop()