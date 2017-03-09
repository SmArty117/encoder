#!/usr/bin/python
__author__ = 'Dan'

##TO DO: screw the menu
#
# saving settings
# returning corrupt codes
#
# creating drop down menus for the text boxes
#

import Tkinter as TK
import tkMessageBox
import code_algorithm as coder
from datetime import datetime
import shutil
import os

logfile = open("log.txt", 'a')
codes = coder.getcodes()
nrcodes = len(codes)

def notyet():
    tkMessageBox.showinfo("NOTYET", "Sorry, this function is\nnot yet available!")

myfont1 = ("Consolas", 12)
bigfont = ("Helvetica", 16)

def validnum(s):
    if s.isdigit():
        return True
    else:
        return False


def log(s):
    logfile.write(str(datetime.now()) + '\n')
    logfile.write(s + '\n')

def retrieve_about():
    aboutfile = open("about.txt", 'r')
    S = aboutfile.read()
	aboutfile.close()
    return S

class MultiEntry(TK.Frame):
    def __init__(self, parent, nrentries=3, checkfunct=validnum,
                 entrysize=3, gridx=5, gridy=1, **kwargs):
        TK.Frame.__init__(self, parent, **kwargs)
        self.parent = parent

        self.lb = []
        self.numentry = []
        self.nr = []

        numcheck = self.register(checkfunct)

        for i in xrange(nrentries):
            lbobj = TK.Label(self, text="    " + str(i + 1) + ": ",
                             bg="white")
            self.lb.append(lbobj)

            nrobj = TK.StringVar()
            nrobj.set("0")
            self.nr.append(nrobj)
            numentryobj = TK.Entry(self, exportselection=0, textvariable=self.nr[i],
                                   width=entrysize, validatecommand=(numcheck, '%S'),
                                   validate="key", relief="sunken", bd=2)
            self.numentry.append(numentryobj)

            self.lb[i].grid(column=(i%gridx)*2, row=i/gridx)
            self.numentry[i].grid(column=(i%gridx)*2+1, row=i/gridx)


class TextBox(TK.Frame):
    def __init__(self, parent, **kwargs):
        TK.Frame.__init__(self, parent)

        self.box = TK.Text(self, **kwargs)
        self.scroll = TK.Scrollbar(self, orient=TK.VERTICAL)

        self.scroll.config(command=self.box.yview)
        self.box.config(yscrollcommand=self.scroll.set)

        self.box.grid(row=0, column=0, sticky=TK.N + TK.S + TK.W + TK.E)
        self.scroll.grid(row=0, column=1, sticky=TK.N + TK.S)


class DeleteDialog(TK.Toplevel):
    def __init__(self):
        TK.Toplevel.__init__(self, bg="white")

        self.title("Delete logs")
        self.resizable(width=0, height=0)

        self.text = TK.Label(self, text="Are you sure you want to delete the logs?", width=30, height=2, bg="white")
        self.yesbutton = TK.Button(self, text="Yes", command=self.YesCallback, width=15, bg="white", bd=3)
        self.nobutton = TK.Button(self, text="No", command=self.NoCallback, width=15, bg="white", bd=3)

        self.text.grid(row=0, column=0, columnspan=2)
        self.yesbutton.grid(row=1, column=0)
        self.nobutton.grid(row=1, column=1)

    def YesCallback(self):
        if os.path.exists("log.txt"):
            logfile.seek(0)
            logfile.truncate()
        self.destroy()

    def NoCallback(self):
        self.destroy()


def OpenDeleteDialog():
    dialog = DeleteDialog()


class Main(TK.Tk):
    def __init__(self):
        TK.Tk.__init__(self)
        self.title("Encoder")
        self.resizable(width=0, height=0)

        self.logswitch = TK.IntVar()
        self.logswitch.set(1)

        self.MainFrameBuild()

    def MainFrameBuild(self):
        self.MainFrame = TK.Frame(self, bg="white", bd=3)

        self.setbutton = TK.Button(self.MainFrame, text="Settings&About >>", command=self.SettingsCallback, relief="raised",
                                   activebackground="#aaffff", width=20, bg="#ffffaa")

        self.lb0 = TK.Label(self.MainFrame, text="Input initial values here:", width=30, height=3,
                            justify=TK.LEFT, bg="white", font=bigfont)

        self.initval = MultiEntry(self.MainFrame, nrentries=nrcodes, bg="white")

        self.lb1 = TK.Label(self.MainFrame, text="Input your text here:", width=30, height=3,
                            justify=TK.LEFT, bg="white", font=bigfont)

        self.msgout = TK.StringVar()
        self.msgout.set("awaiting input from user")
        self.fbmsg = TK.Message(self.MainFrame, textvariable=self.msgout, relief="ridge", width="5c",
                                bg = "#cccccc")

        self.input = TextBox(self.MainFrame, exportselection=0, wrap=TK.WORD, undo=True,
                             height=5, width=50, font=myfont1, relief="sunken", bd=3,)

        self.buttonframe = TK.Frame(self.MainFrame, background="white", bd=0)

        self.encodebutton = TK.Button(self.buttonframe, text="Encode", command=self.Encode_CallBack,
                                      height=2, width=20, relief="raised", activebackground="#aaffff")

        self.decodebutton = TK.Button(self.buttonframe, text="Decode", command=self.Decode_CallBack,
                                      height=2, width=20, relief="raised", activebackground="#aaffff")

        self.lb2 = TK.Label(self.MainFrame, text="Output:", width=30, height=3,
                            justify=TK.LEFT, bg="white", font=bigfont)

        self.output = TextBox(self.MainFrame, wrap=TK.WORD, undo=True,
                              height=5, width=50, font=myfont1, relief="sunken", bd=3)

        self.setbutton.pack(anchor=TK.NE)

        self.lb0.pack()
        self.initval.pack()

        self.lb1.pack()
        self.input.pack()

        self.encodebutton.grid(row=0, column=0)
        self.decodebutton.grid(row=0, column=1)
        self.buttonframe.pack()

        self.fbmsg.pack()

        self.lb2.pack()
        self.output.pack()

        self.MainFrame.grid(column=0, row=0, sticky=TK.N)

    def ResetFbmsg(self):
        self.msgout.set("awaiting input from user")
        self.fbmsg.config(bg="grey")

    def gettext(self):

        INS = self.input.box.get("1.0", TK.END)
        return str(INS)

    def getnrs(self):
        nrs = []
        for s in self.initval.nr:
            nrs.append(int(s.get()))
        return nrs

    def Encode_CallBack(self):
        INS = self.gettext()
        nrs = self.getnrs()
        self.msgout.set("Input received. Processing...")
        self.fbmsg.config(bg="yellow")

        tobelogged = "Encoded:\n" + INS + str(nrs)
        if self.logswitch.get():
            log(tobelogged)

        encoded = coder.encode(INS, nrs, codes)
        self.output.box.insert("1.0", encoded)

        if encoded == "CORRUPT CODES" or encoded == "INVALID INPUT":
            self.msgout.set("An error was raised")
            self.fbmsg.config(bg="red")
            if self.logswitch.get():
                log("failed\n\n")

        self.msgout.set("Processing complete. Output ready.")
        self.fbmsg.config(bg="green")
        if self.logswitch.get():
            log("successful\n\n")

    def Decode_CallBack(self):
        INS = self.gettext()
        nrs = self.getnrs()
        self.msgout.set("Input received. Processing...")
        self.fbmsg.config(bg="yellow")

        tobelogged = "Decoded:\n" + INS + str(nrs)
        if self.logswitch.get():
            log(tobelogged)

        decoded = coder.decode(INS, nrs, codes)
        self.output.box.insert("1.0", decoded)

        if decoded == "CORRUPT CODES" or  decoded == "INVALID INPUT":
            self.msgout.set("An error was raised")
            self.fbmsg.config(bg="red")
            if self.logswitch.get():
                log("failed\n\n")

        self.msgout.set("Processing complete. Output ready.")
        self.fbmsg.config(bg="green")
        if self.logswitch.get():
            log("successful\n\n")

    def SettingsCallback(self):
        try:
            self.SettingsFrame.grid(column=1, row=0, sticky=TK.N)
        except:
            self.SettingsFrameBuild()

        self.setbutton.config(command=self.HideCallback, text="Hide<<")

    def HideCallback(self):
        self.SettingsFrame.grid_remove()
        self.setbutton.config(command=self.SettingsCallback, text="Settings&About >>")

    def SettingsFrameBuild(self):
        self.SettingsFrame = TK.Frame(self, bg="white", bd=3)

        self.toplabel = TK.Label(self.SettingsFrame, text="Strings used (codes):", font=bigfont,
                                 height=1, bg="white")

        self.codesentry = TextBox(self.SettingsFrame, wrap=TK.WORD, undo=True, font=myfont1,
                                  relief="sunken", bd=3, height=5, width=50)

        self.sbframe = TK.Frame(self.SettingsFrame, bg="white", bd=0)
        self.updatebutton = TK.Button(self.sbframe, text="Update Codes", command=self.UpdateCallback,
                                      bg="#eeeeee", activebackground="#aaffff")
        self.resetbutton = TK.Button(self.sbframe, text="Reset codes to default", command=self.ResetCallback,
                                     bg="#eeeeee", activebackground="#aaffff")

        self.radioframe1 = TK.LabelFrame(self.SettingsFrame, bg="white", text="Logging input", bd=1)

        self.fr1b1 = TK.Radiobutton(self.radioframe1, text="Log input", variable=self.logswitch, value=1, bg="white")
        self.fr1b2 = TK.Radiobutton(self.radioframe1, text="Do not log input", variable=self.logswitch, value=0, bg="white")
        self.deletelog = TK.Button(self.radioframe1, text="Erase all logs", command=OpenDeleteDialog, width=15)

        self.closebutton = TK.Button(self.SettingsFrame, text="Close", command=self.DestroyCallback)

        self.msg=TK.StringVar()
        self.msg.set("...")
        self.sfbmsg = TK.Message(self.SettingsFrame, textvariable=self.msg, relief="ridge", bg="#dddddd", width="6c")

        self.about = retrieve_about()
        self.aboutmsg = TK.Message(self.SettingsFrame, text=self.about, relief="flat", bg="white", width=400)

        self.toplabel.pack(anchor=TK.NW)
        self.codesentry.pack()

        self.updatebutton.grid(row=0, column=0)
        self.resetbutton.grid(row=0, column=1)
        self.sbframe.pack()

        self.fr1b1.grid(row=0, column=0)
        self.fr1b2.grid(row=0, column=1)
        self.deletelog.grid(row=1, columnspan=2)
        self.radioframe1.pack()

        self.aboutmsg.pack()
        self.closebutton.pack(anchor=TK.SE)

        self.sfbmsg.pack(anchor=TK.SW)

        self.BoxUpdate()
        self.SettingsFrame.grid(column=1, row=0, sticky=TK.N)

    def UpdateCallback(self):
        INS = self.codesentry.box.get("1.0", TK.END)

        codesfile = open("codes.in", "w")
        codesfile.write(INS)
        codesfile.close()

        self.BoxUpdate()
        self.msg.set("Codes Updated! Restart the application to start using the new codes")

    def ResetCallback(self):
        shutil.copy2("DefaultCodes.in", "codes.in")
        self.BoxUpdate()
        self.msg.set("Codes reset to default!")

    def DestroyCallback(self):
        self.SettingsFrame.destroy()
        self.setbutton.config(text="Settings>>", command=self.SettingsCallback)

    def BoxUpdate(self):
        self.codesentry.box.delete("1.0", TK.END)
        codes = coder.getcodes()
        for code in codes:
            self.codesentry.box.insert(TK.END, code+'\n')


app = Main()
app.mainloop()

logfile.close()
