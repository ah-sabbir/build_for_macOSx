import tkinter as tk
import pandas as pd
from tkinter import filedialog,messagebox
from tkinter import *
import logging
import os
import glob

LARGE_FONT= ("Verdana", 12)

about_text = """Hello Users! Welcome to Excel Application.
This app has created for compare Parcel Numbers from the two
CSV FIles. Before running this app you should make sure that
the "ParcelNumber" column exists in both FIles.when you run
its operation by clicking the "check" button it may take
some moment to complete operation.

The ParcelNumbers which are not exist in Cross Reference File then stored them into
ParcelNumbers_Not_Exists_into_Cross_Reference_File.txt/.CSV FIles

If The Parcel Numbers exists in both files then It will show this
'There is no Unique Parcel Number :)'

for any support please contact: ahsabbir104@gmail.com
Thanks
"""
error_log = logging

error_log.basicConfig(filename="compareGUIerror.log",level=error_log.ERROR,
    format='%(asctime)-15s : %(message)s')

class SeaofBTCapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.label = tk.Label(self,text="Please select File Path to Check", font=LARGE_FONT)
        self.label.pack(pady=20,padx=20)
        output_file_path = tk.Button(self,text = "where to save the Output File",font = LARGE_FONT,command = self.output_File_loc)
        output_file_path.pack(pady=20,padx=20)
        input_btn = tk.Button(self,text="Select Input File",font=LARGE_FONT,command=self.Input_File)
        input_btn.pack(side=LEFT,pady=20,padx=20)
        cross_ref_btn = tk.Button(self,text="Select Cross Reference FIle",font=LARGE_FONT,command=self.Cross_Ref_file)
        cross_ref_btn.pack(side=LEFT,pady=20,padx=20)
        check_btn = tk.Button(self,text="Check",font=LARGE_FONT,command=self.compare)
        check_btn.pack(side=RIGHT,pady=20,padx=20)

    def Input_File(self):
        self.in_file = filedialog.askopenfilename(title = "Select Input File",initialfile=".csv")
        self.label.config(text= "Input File Selected :) ")
    def Cross_Ref_file(self):
        self.cross_file = filedialog.askopenfilename(title = "Select Cross Reference File",initialfile=".csv")
        self.label.config(text= "Cross Reference File Selected :) ")
    def output_File_loc(self):
        self.outputFileLoc = filedialog.askdirectory(title = "Select where will save file")
        self.label.config(text= "Output Folder Selected :) ")
    def compare(self):
        try:
            cross_path = self.cross_file
            input_path = self.in_file
        except Exception as e:
            error_log.error(e)
            self.label.config(text= "Sorry you didn't select FIles. please select both Files")
            return 0
        try:
            outputfilepath = self.outputFileLoc
        except Exception as e:
            error_log.error(e)
            self.label.config(text= "Sorry you didn't select The Folder or Path.where will save output file")
            return 0

        self.label.config(text = "running please wait !")
        try:
            cross_df = pd.read_csv(cross_path)
            input_df = pd.read_csv(input_path)
        except Exception as e:
            error_log.error(e)
            self.label.config(text = "The File or File Path is not valid.\nplease enter valid file path :( ")
            return 0

        values_list = []
        for parcelnumber in input_df['ParcelNumber']:
            if self.compare_d(parcelnumber,cross_df['ParcelNumber']):
                #print(parcelnumber)
                d_frame = input_df[input_df['ParcelNumber']==parcelnumber]
                values_list.append(d_frame)

        try:
            df = pd.concat(values_list)
        except Exception as e:
            error_log.error(e)
            self.label.config(text = "There is no Unique Parcel Number :)")
            return 0
        try:
            self.text_file_out(df['ParcelNumber'],outputfilepath)
            df.to_csv(os.path.join(outputfilepath,"Not_Exists_into_Cross_Reference_File.csv"),index=False)
            msg_txt = "Saved location: "+outputfilepath
            self.label.config(text = "operation completed !\n\n"+msg_txt)
        except Exception as e:
            error_log.error(e)
            self.label.config(text = "Please Select Valid Location Paths and Try Again")

    def compare_d(self,num,df_num):
        for number in df_num:
        	try:
	            if int(number) == int(num):
	                return False
	                break
	        except:
	            if number == num:
	                return False
	                break
        return True

    def text_file_out(self,args,out_path):
        txt = ""
        for tx in args:
            if len(str(tx))<10:
                txt += "00"+str(tx)+","
            else:
                txt += str(tx)+","
        txt = txt[:-1]
        try:
            with open(os.path.join(out_path,"ParcelNumbers_Not_Exists_into_Cross_Reference_File.txt"),"w") as writer:
                writer.write(txt)
        except:
            open(os.path.join(out_path,"ParcelNumbers_Not_Exists_into_Cross_Reference_File.txt"),"r").close()
            with open(os.path.join(out_path,"ParcelNumbers_Not_Exists_into_Cross_Reference_File.txt"),"w") as writer:
                writer.write(txt)

class menu_bar:
    def __init__(self,root):
        self.root = root
        menubar = Menu(self.root)
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.help_menu)
        help_menu.add_command(label="Exit",command=self.quit)
        menubar.add_cascade(label="Help",menu=help_menu)
        self.root.config(menu=menubar)
    def help_menu(self):
        messagebox.showinfo("About", about_text)
    def quit(self):
        self.root.destroy()

if __name__=='__main__':
    app = SeaofBTCapp()
    app.minsize(550,300)
    app.maxsize(750,500)
    #app.geometry("550x300")
    #app.resizable(0,0)
    app.title("PARCEL NUMBER CHECKER")
    menu = menu_bar(app)
    app.mainloop()
