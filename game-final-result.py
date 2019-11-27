import tkinter as tk
import os
from time import sleep
import ctypes  
from tkinter import *
from tkinter import messagebox
from pandastable import Table, TableModel
import pandas as pd
from PIL import Image,ImageTk  
from pathlib import Path


app = ''
current_path = os.path.dirname(os.path.realpath(__file__))
print(current_path)
FILENAME='results.txt'

#проверка
def file_not_exist():
    ctypes.windll.user32.MessageBoxW(0, "File results not exist!", "Warning", 1) #отключить эту строку что бы при старте не было окна об отсутствии
#про
def about():
    ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)

#Splashscreen
class SplashScreen(Toplevel):
     def __init__(self, master, image=None, timeout=500):
         Toplevel.__init__(self, master, relief=RAISED, borderwidth=5)
         self.main = master
         self.main.withdraw()
         self.overrideredirect(1)
         im = Image.open(image)#open image
         self.image = ImageTk.PhotoImage(im)
         self.after_idle(self.centerOnScreen)
         self.update()
         self.after(timeout, self.destroy)
    #center image
     def centerOnScreen(self):
         self.update_idletasks()
         width, height = self.width, self.height = \
                         self.image.width(), self.image.height()
         xmax = self.winfo_screenwidth()
         ymax = self.winfo_screenheight()
         x0 = self.x0 = (xmax - self.winfo_reqwidth()) / 2 - width/2
         y0 = self.y0 = (ymax - self.winfo_reqheight()) / 2 - height/2
         self.geometry("+%d+%d" % (x0, y0))
         self.createWidgets()
     def createWidgets(self):
         self.canvas = Canvas(self, height=self.width, width=self.height)
         self.canvas.create_image(0,0, anchor=NW, image=self.image)
         self.canvas.pack()
         #destroy imgae on close
     def destroy(self):
         self.main.update()
         self.main.deiconify()
         self.withdraw()
         
#Table frame from pandastable
class TableFrame(Frame):
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('400x200+200+100')#geometry 
        self.main.title('Game')#titile
        
                 
        my_file = Path(os.path.join(current_path,FILENAME))
        if my_file.is_file():    
            print("EXIST")
            self.dataOrig = pd.read_csv(os.path.join(current_path,FILENAME), sep=" ", header=None)# load data in table from results.txt
            #first row as index
            self.dataOrig = self.dataOrig.set_index([0]) 
            new_header = self.dataOrig.iloc[0]
            self.dataOrig = self.dataOrig[1:]
            self.dataOrig.columns = new_header  
            #замена пустых на ноли для статистики
            self.data = self.dataOrig.fillna(0).astype(float).sum(axis=1).to_frame()
            #добавление колонки
            self.data.columns = ['Баллы']
            #переменные игроков
            test = (self.dataOrig=='0').sum(axis=1).sort_values().to_frame()  
            test.columns = ['some']
            
            if (test.some[-1]!=0):
                self.worst_player =   ' '.join(test[(test.some == test.some[-1])].index.values)#(self.dataOrig=='0').sum(axis=1).sort_values(ascending=False).tail(1).index[0]
            else:
                 self.worst_player =   ' нет '
                 
            test = (self.dataOrig=='1').sum(axis=1).sort_values().to_frame()  
            test.columns = ['some']
            
            if (test.some[-1]!=0):
                self.best_player =   ' '.join(test[(test.some == test.some[-1])].index.values)#(self.dataOrig=='1').sum(axis=1).sort_values(ascending=False).tail(1).index[0]
            else:
                 self.best_player =   ' нет '
                       
            test = (self.dataOrig=='0.5').sum(axis=1).sort_values().to_frame()  
            test.columns = ['some']
            
            if (test.some[-1]!=0):
                self.middle_player =   ' '.join(test[(test.some == test.some[-1])].index.values)#(self.dataOrig=='0.5').sum(axis=1).sort_values(ascending=False).tail(1).index[0]
            else:
                 self.middle_player =   ' нет '
                 
            #сортируем
            self.data = self.data.sort_values(by=['Баллы'],ascending=False)
            
            
            #загружаем в таблицу
            self.table = pt = Table(self, dataframe=self.data,
                                    showtoolbar=False, showstatusbar=True)   
        
        #if file not exist
        else:
            print("NO EXIST")
            self.table = pt = Table(self, dataframe=pd.DataFrame(),
                                showtoolbar=False, showstatusbar=True) 


        #показываем таблицу
        pt.show()
        pt.showIndex()
        return
    
    dataOrig = pd.read_csv(os.path.join(current_path,FILENAME), sep=" ", header=None)# load data in table from results.txt
    #first row as index
    dataOrig = dataOrig.set_index([0]) 
    new_header = dataOrig.iloc[0]
    dataOrig = dataOrig[1:]
    dataOrig.columns = new_header  
    #замена пустых на ноли для статистики
    data = dataOrig.fillna(0).astype(float).sum(axis=1).sort_values(ascending=False).to_frame()
    #добавление колонки
    data.columns = ['Баллы']
    
    test = (dataOrig=='0.5').sum(axis=1).sort_values().to_frame()    
    test.columns = ['some']   
    if (test.some[-1]!=0):
        ' '.join(test[(test.some == test.some[-1])].index.values)
    else:
        print(' нет ')
    
    
    (dataOrig=='1').sum(axis=1).sort_values()
    
    plus = (dataOrig=='1').sum(axis=1).sort_values().to_frame()
    plus.columns = ['some']


    dataOrig.fillna(0).astype(float).sum(axis=1).sort_values(ascending=False).to_frame()

     #.filter(lambda x: len(x) == 1)
            
    
#главный фрейм        
class ResultsFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("Grid Manager")

        for r in range(6):
            self.master.rowconfigure(r, weight=1)    
        #фрейм таблицы    
        self.Frame1 = TableFrame(self)
        self.Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S) 
        self.master.columnconfigure(1, weight=1)
        #фрейм статистики игроков
        self.label1Text = StringVar()      
        self.label1Text.set("")
        self.label2Text = StringVar()      
        self.label2Text.set("")
        self.label3Text = StringVar()      
        self.label3Text.set("")
        #лейблы 
        Label(master, textvariable=self.label1Text).grid(row=0,column=2,sticky=W+E+N+S)
        Label(master, textvariable=self.label2Text).grid(row=1,column=2,sticky=W+E+N+S)
        Label(master, textvariable=self.label3Text).grid(row=2,column=2,sticky=W+E+N+S)
        
        #show winner statistic in new columns
    def show_winners(self):
          
          self.label1Text.set("Наибольше проиграшей\n"+self.Frame1.worst_player)
          self.label2Text.set("Наибольше побед\n"+self.Frame1.best_player)
          self.label3Text.set("Наибольше ничьих\n"+self.Frame1.middle_player)
         
    #обновить даные с файла
    def update(self):           
        my_file = Path(os.path.join(current_path,FILENAME))
        if my_file.is_file():    
            print("EXIST")
            self.dataOrig = pd.read_csv(os.path.join(current_path,FILENAME), sep=" ", header=None)# load data in table from results.txt
            #first row as index
            self.dataOrig = self.dataOrig.set_index([0]) 
            new_header = self.dataOrig.iloc[0]
            self.dataOrig = self.dataOrig[1:]
            self.dataOrig.columns = new_header  
            #замена пустых на ноли для статистики
            self.data = self.dataOrig.fillna(0).astype(float).sum(axis=1).to_frame()
            #добавление колонки
            self.data.columns = ['Баллы']
            #сортируем
            self.data = self.data.sort_values(by=['Баллы'],ascending=False)
            print(self.data)
            print(self.Frame1.table.model.df)
            print('prev')
            #обновить таблицу
            #self.Frame1.table.updateModel(self.data)
            #self.Frame1.table.model = TableModel(self.data)
            self.Frame1.table.model.df = self.data
            self.Frame1.table.redraw()
            
            #переменные игроков
            test = (self.dataOrig=='0').sum(axis=1).sort_values().to_frame()  
            test.columns = ['some']            
            if (test.some[-1]!=0):
                self.Frame1.worst_player =   ' '.join(test[(test.some == test.some[-1])].index.values)#(self.dataOrig=='0').sum(axis=1).sort_values(ascending=False).tail(1).index[0]
            else:
                 self.worst_player =   ' нет '
                 
            test = (self.dataOrig=='1').sum(axis=1).sort_values().to_frame()  
            test.columns = ['some']
            if (test.some[-1]!=0):
                self.Frame1.best_player =   ' '.join(test[(test.some == test.some[-1])].index.values)#(self.dataOrig=='1').sum(axis=1).sort_values(ascending=False).tail(1).index[0]
            else:
                 self.best_player =   ' нет '
                 
            test = (self.dataOrig=='0.5').sum(axis=1).sort_values().to_frame()  
            test.columns = ['some']
            if (test.some[-1]!=0):
                self.Frame1.middle_player =   ' '.join(test[(test.some == test.some[-1])].index.values)#(self.dataOrig=='0.5').sum(axis=1).sort_values(ascending=False).tail(1).index[0]
            else:
                 self.middle_player =   ' нет '
                 
            self.show_winners()
                        

        
        
        
        
        
                      
#app
class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #bind close to over function        
        self.protocol("WM_DELETE_WINDOW", self.closeEvent)
        #create table frame
        self.window = ResultsFrame(self)#TableFrame(self)
        m = Menu(self) #menu
        self.config(menu=m)        
        fm = Menu(m)
        m.add_cascade(label="Меню",menu=fm)
        fm.add_command(label="Показать победителей и проигравших",command=self.window.show_winners)
        fm.add_command(label="Обновить",command=self.window.update)
        fm.add_command(label="Справка",command=about)

    #close app
    def closeEvent(self):
        app.destroy()        
        exit()

def nofile():
    global app
    #проверка на наличие файла
    file_not_exist();
    
if __name__ == "__main__":
    try:#open file if exist continue
        with open(os.path.join(current_path,FILENAME)):
            pass
        #if file not exist
    except:
        nofile()
           
    app = ExampleApp()
    s = SplashScreen(app, timeout=500, image="image.jpg")
    app.mainloop()
