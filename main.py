#!/usr/bin/env python
# "Animakeris 26" – animacijų piešimo programėlė – pieši animacijos kadrus, pasirenki FPS/(mili)sekundės per n kadrų ir sugeneruoja |.mp4|/|.gif| (PIL generuoja |.gif|/|.apng|, ffmpeg "binding"ai generuoja |.mp4|/|.mov|/t.t, tkinter daro main gui (|root|))
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter.filedialog import asksaveasfilename, askopenfile
from PIL import Image, ImageTk, ImageChops
import aggdraw as ImageDraw
import ffmpeg
import json # hold ON!! i can just use json!!
from base64 import b64encode, b64decode
from io import BytesIO

ver = "26.3.8"
codename = "ffAHH!!"
cachedFrm = None
cachedFCImg = None
savedP = None
defSelData = {"x1":0,"y1":0,"x2":0,"y2":0,"pix":None,"move":False}
selData = defSelData.copy()
selRect = None

def fileShit():
	return {"defaultextension": ".a26", "filetypes": [(getStr(17), "*.a26"),(getStr(18), "*.*")]}

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
			if type(curr) == str and curr in lTbl:
				w.config(**{o: trans[lang.get()][lTbl[curr]]})
				continue
		except tk.TclError: pass

def aLangMenu(m, lTbl):
	end = m.index(tk.END)
	if end is None: return
	count = 0
	while count <= end:
		try:
			curr = m.entrycget(count, "label")
			if curr in lTbl: m.entryconfig(count, label=trans[lang.get()][lTbl[curr]])
			ch = m.entrycget(count, "menu")
			if m.type(count) == "cascade" and ch and lTbl[curr] != 11: aLangMenu(m.nametowidget(ch), lTbl)
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
	for l in proj[selFrame][:selLayer]: cachedFrm.paste(l["img"], l["img"])

def blankImg(): return Image.new("RGBA", size)

def redrawCnv():
	global cachedFCImg, selRect, selData
	new = cachedFrm.copy()
	new.paste(proj[selFrame][selLayer]["img"], proj[selFrame][selLayer]["img"])
	cnv.img = ImageTk.PhotoImage(new)
	if cachedFCImg is None:
		cachedFCImg = cnv.create_image(0,0,anchor="nw",image=cnv.img)
		return
	if any([selData["x1"],selData["x2"],selData["y1"],selData["y2"]]):
		if selRect is None: selRect = cnv.create_rectangle(0,0,0,0, width=0, fill="#bbfaff", stipple="gray50")
		cnv.coords(selRect, selData["x1"],selData["y1"],selData["x2"],selData["y2"])
	cnv.itemconfig(cachedFCImg, image=cnv.img)

def layerFromIm(i):
	jraw = ImageDraw.Draw(i)
	return {"img": i, "draw": jraw}

def blankLayer():
	return layerFromIm(blankImg())

def addFrame():
	proj.append([blankLayer()])

def abt():
	msgbox.showinfo(f"Animakeris 26 {ver} (\"{codename}\")",f"{getStr(9)}\n\n{getStr(10)} https://github.com/RixInGithub/animakeris26")

def img2Base64(i):
	buf = BytesIO()
	i.save(buf, format="PNG")
	return b64encode(buf.getvalue()).decode()

def writeProj(p):
	with open(p, "w", encoding="utf8") as projIO:
		json.dump({
			"frames": [[{**{k: v for k, v in b.items() if k != "draw" and k != "img"}, "img": img2Base64(b["img"])} for b in a] for a in proj],
			"w": size[0],
			"h": size[1]
		}, projIO, separators=(",",":"))

def openProjWithoutSave():
	global savedP, size, proj
	with askopenfile("r", title="Open", **fileShit()) as f: # i wonder if this works...
		if f == None: return
		print(f.name)
		savedP = f.name
		fileDict = json.load(f)
	# no moar |f|
	resetProjDangerous() # prepare for opened project
	size = [fileDict.get("w", size[0]), fileDict.get("h", size[1])] # support older projects that didnt save size (aka eraserWorks.a26)
	proj = []
	for frm in fileDict["frames"]:
		idx = len(proj)
		proj.append([])
		for lyr in frm:
			im = Image.open(BytesIO(b64decode(lyr["img"])))
			proj[idx].append(layerFromIm(im))
	recacheFrm()
	redrawCnv()

def saveProj(withSavedP=True):
	global savedP
	if savedP and withSavedP:
		writeProj(savedP)
		return savedP
	p = asksaveasfilename(title="Save as", **fileShit()) # got too lazy, am not translating ts
	if p:
		writeProj(p)
		savedP = p
	return p # just return |p|, if user cancelled, it'll return |None|.

def saveAs():
	return saveProj(False)

def saveCurry(after):
	def inner():
		if enablePp:
			out = msgbox.askyesnocancel("Animakeris 26",getStr(5))
			if out == None: return # cancelled
			if out == True and saveProj() == None: return # also cancelled
		after()
	return inner

def resetProjDangerous():
	global cachedFrm, cachedFCImg, selFrame, selLayer, size, proj
	cachedFrm = None
	if cachedFCImg is not None: cnv.delete(cachedFCImg)
	cachedFCImg = None
	selFrame = 0
	selLayer = 0
	size = [500, 400]
	cnv.config(width=size[0], height=size[1])
	proj = []
	cnv.img = None
	tools.selection_clear(0, tk.END)
	retransTools()
	addFrame()
	recacheFrm()
	redrawCnv()

exitPp = saveCurry(lambda: root.destroy())
newProj = saveCurry(resetProjDangerous)
openProj = saveCurry(openProjWithoutSave)

def applyErase(i):
	eraseAlpha = i.getchannel("A")
	base = proj[selFrame][selLayer]["img"]
	r, g, b, a = base.split()
	a = ImageChops.subtract(a, eraseAlpha)
	proj[selFrame][selLayer]["img"] = Image.merge("RGBA", (r, g, b, a))
	proj[selFrame][selLayer]["draw"] = ImageDraw.Draw(proj[selFrame][selLayer]["img"])

def downEvt(e):
	global mDown, lastXy, selData
	mDown = True
	lastXy = None
	sel = tools.curselection()[0]
	if sel == 0 or sel == 1: # pencil AND eraser
		drawOn = proj[selFrame][selLayer]["draw"]
		x = e.x
		y = e.y
		phil = "Black"
		pSize = 10
		hSize = pSize/2
		if sel == 1:
			eraseIm = blankImg()
			drawOn = ImageDraw.Draw(eraseIm)
			phil = "Black" # constant
		drawOn.ellipse((x-hSize,y-hSize,x+hSize,y+hSize), ImageDraw.Brush(phil))
		drawOn.flush()
		if sel == 1:
			applyErase(eraseIm)
		redrawCnv()
		lastXy = [x, y]
		return
	if sel == 2:
		if selData["move"]:
			return
		if not selRect:
			selData["x1"] = selData["x2"] = e.x
			selData["y1"] = selData["y2"] = e.y
			redrawCnv()
		return

def onMove(e):
	global lastXy, mDown, selData
	if not mDown: return
	sel = tools.curselection()[0]
	if sel == 0 or sel == 1: # pencil AND eraser
		drawOn = proj[selFrame][selLayer]["draw"]
		x = e.x
		y = e.y
		phil = "Black"
		pSize = 10
		hSize = pSize/2
		if sel == 1:
			eraseIm = blankImg()
			drawOn = ImageDraw.Draw(eraseIm)
			phil = "Black" # constant
		drawOn.line((lastXy[0], lastXy[1], x, y), ImageDraw.Pen(phil, pSize))
		drawOn.ellipse((x-hSize,y-hSize,x+hSize,y+hSize), ImageDraw.Brush(phil))
		drawOn.flush()
		if sel == 1:
			applyErase(eraseIm)
			# print("hello??")
		redrawCnv()
		lastXy = [x, y]
		return
	if sel == 2:
		if not selData["move"]:
			selData["x2"] = e.x
			selData["y2"] = e.y
			redrawCnv()
			return
		return
	# wait what

def upEvt(e):
	global mDown
	mDown = False
	sel = tools.curselection()[0]
	if sel == 2:
		selData["move"] = True

def newSel(e):
	global selRect, selData, defSelData
	if selRect:
		cnv.delete(selRect)
		selRect = None
		selData = defSelData.copy()
		redrawCnv()

def getStr(n):
	try:
		return trans[lang.get()][n]
	except: return "⁇⁇" # idfk

translatedCfg = ["text", "value", "label", "content"]
enablePp = 1
availableTools = [3, 4, 14, 19]
mDown = False
lastXy = None
trans = {
	"en": [
		"File",
		"Exit",
		"New",
		"Pencil",
		"Eraser",
		"Would you like to save?",
		"Edit",
		"Help",
		"About",
		"An animation program made by Adas Jankus.",
		"Source available at:",
		"Change languages…",
		"English",
		"Save",
		"Selection tool",
		"Open",
		"Save as...",
		"Animakeris 26 files",
		"All files",
		"Fill bucket"
	],
	"lt": [
		"Failas",
		"Išjungti",
		"Nauja animacija",
		"Pieštukas",
		"Trintukas",
		"Ar norėtumete išsaugoti animaciją?",
		"Redaguoti",
		"Pagalba (Help)",
		"Apie programą",
		"Ado Jankaus programa, skirta kurti animacijas.",
		"Kodo repоzitorija:",
		"Keisti kalbą… (Change languages…)",
		"lietuvių",
		"Išsaugoti",
		"Pasirinkimas",
		"Atidaryti",
		"Išsaugoti kitu vardu...",
		"Animakeris 26 failai",
		"Visi failai",
		"Pildymo kibiras"
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
file.add_command(label=getStr(13), command=saveProj)
file.add_command(label=getStr(16), command=saveAs)
file.add_command(label=getStr(15), command=openProj)
file.add_command(label=getStr(2), command=newProj)
file.add_command(label=getStr(1), command=exitPp)
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
cnv.bind("<ButtonRelease-1>", upEvt)
cnv.bind("<B1-Motion>", onMove)
cnv.grid(row=0, column=0)
wrap2.grid(row=0, column=1)
wrap3 = tk.Frame(wrap1) # wrapper for tools and tool opts
wrap3.rowconfigure(1, weight=1)
wrap3.columnconfigure(0, weight=1)
tools = tk.Listbox(wrap3, activestyle=tk.NONE, height=len(availableTools), width=0) # tools
tools.bind("<<ListboxSelect>>", newSel)
retransTools()
tools.grid(row=0, column=0, sticky="nesw")
opts = tk.Frame(wrap3, bg="red")
opts.grid(row=1, column=0, sticky="nesw")
wrap3.grid(row=0, column=0, sticky="nesw")
wrap1.grid(row=0, column=0, sticky="nesw")

root.config(menu=menu)

root.mainloop()