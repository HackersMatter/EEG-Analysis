from tkinter import *
import mne
from tkinter import ttk
from matplotlib.figure import Figure
import threading
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def ondoubleclick(self,event):
        item = self.treev.selection()[0]
        print("you clicked on", self.treev.item(item,"text"))

    def updateinfo(self,mood):
        self.info_label.configure(text = 'Current mood: '+mood)

    def updatetree(self,mood):
        self.treev.delete(*self.treev.get_children())
        file = pd.read_csv(mood+'.txt',delimiter=':',header=None)
        for i in range(file.shape[0]):
            self.treev.insert(parent='', index='end', iid=i, text="l"+str(i), values=(i+1, file.iloc[i][1], file.iloc[i][2]))

    def run(self):

        # Tk root
        self.root = Tk()
        self.root.title('Song Recommendation')
        self.root.iconbitmap('m.ico')
        self.root.geometry('871x724')
        self.root.configure(background='#BABABA')

        # Labels
        self.info_label = Label(self.root, text = 'Current mood:',font=('times new roman',25))
        self.info_label.grid(row=0,padx=10,pady=(10,0),sticky='NESW')

        self.songs_label = Label(self.root, text = 'Recommended Songs based on current mood',font=('times new roman',15))
        self.songs_label.grid(row=1,padx=10,sticky='NESW')

        self.names_label = Label(self.root, text = 'Project members: Keval Meher, Ruchika Narad, Yukta Rane, Mukesh Kurmi',font=('times new roman',8))
        self.names_label.grid(row=5,padx=10,pady=(0,10),sticky='NWSE')

        # List
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=('times new roman', 15),background='#191414',fieldbackground="#191414", foreground="white")
        style.configure("Treeview.Heading", font=('times new roman', 15))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        #style.map('Treeview', background=[('selected', '#BFBFBF')])

        self.treev = ttk.Treeview(self.root, selectmode ='browse',height=29, style="Treeview")
        self.treev.bind("<Double-1>", self.ondoubleclick)
        self.treev["columns"] = ("1", "2", "3")
        self.treev['show'] = 'headings'
        self.treev.column("1", width = 50, anchor ='c')
        self.treev.column("2", width = 500, anchor ='w')
        self.treev.column("3", width = 300, anchor ='w')
        self.treev.heading("1", text ="#")
        self.treev.heading("2", text ="Name")
        self.treev.heading("3", text ="Artist")

        self.treev.grid(row=2,rowspan=3,padx=10)

        self.root.mainloop()
