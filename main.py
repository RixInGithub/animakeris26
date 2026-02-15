# "Animakeris 26" – animacijų piešimo programėlė – pieši animacijos kadrus, pasirenki FPS/(mili)sekundės per n kadrų ir sugeneruoja |.mp4|/|.gif| (PIL generuoja |.gif|/|.apng|, ffmpeg "binding"ai generuoja |.mp4|/|.mov|/t.t, tkinter daro main gui (|root|))
import tkinter as tk
from PIL import Image
import ffmpeg

def pickProj():
	def _quit():
		projPick.destroy()
		root.destroy()
	projPick = tk.Toplevel(root)
	projPick.title("Animakeris 26")
	projPick.protocol("WM_DELETE_WINDOW", _quit)

root = tk.Tk() # main gui
root.withdraw()

pickProj()
root.mainloop()