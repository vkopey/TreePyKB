# -*- coding: utf-8 -*-
"""
TreePyKB v0.5
        
Simple outliner and expert system in Python
    
Kopey Vladimir, 2014
vkopey@gmail.com    
    
This software is distibuted under the Gnu-GPL. Please Visit
http://www.gnu.org/licenses/gpl.txt to see the license."""
import Tkinter
import ttk
import tkSimpleDialog
from tkFileDialog import *
import tkMessageBox
import os
import shutil
import re
import keyword
import MakeCode
from Tkinter import StringVar
import JunctionPoints
import subprocess

class MyApp(Tkinter.Tk):
    '''Клас головного вікна програми GUI'''    
    def __init__(self):
        '''Конструктор'''
        Tkinter.Tk.__init__(self) #виклик конструктора базового класу
        self.KBdir=u"" # повний шлях до каталогу бази знань
        self.programDir=os.getcwd() # каталог з програмою # ???
        self.images=[] # рисунки для позначення каталогів
        self.images.append(Tkinter.PhotoImage(file='class.ppm')) # рисунок за замовчуванням
        self.srcPath=('',1) # шлях джерела для копіювання (джерело, копіювати(1)/вирізати(0))
        self.classfile='class.pykb' # назва файла класу-каталога
        self.editedId=None # Id елемента, який зараз редагується в txt (None - ніщо не радагується)
        self.dlgEntry=None # активне поле вводу вікна шаблону
        self.history=[] # історія вибору елементів дерева
        self.historyIndex=0 # поточний індекс історії
        
        self.frame0 = Tkinter.Frame(self) # фрейм з меню
        self.btnFile = Tkinter.Menubutton(self.frame0,text="File",padx=1,pady=1) # створити кнопку меню
        self.btnFile.pack(side=Tkinter.LEFT) # розмістити компонент
        submenu = Tkinter.Menu(self.btnFile,tearoff=True) # створити підменю
        self.btnFile['menu'] = submenu # задати меню підменю
        submenu.add_command(label='New',command=self.new) # додати команду
        submenu.add_command(label='Open',command=lambda:self.openKB())
        submenu.add_command(label='Run',command=self.run)
        submenu.add_command(label='Import',command=self.importCode)
        submenu2 = Tkinter.Menu(submenu) #створити підменю
        submenu.add_cascade(label='Export To', menu=submenu2) #добавити підменю 
        #submenu2.add_command(label='HTML',command=self.exportToHTML)
        submenu2.add_command(label='Code',command=self.exportCode)
        submenu.add_command(label='About',command=self.about)
        submenu.add_command(label='Exit',command=self.exit)
        self.btnEdit = Tkinter.Menubutton(self.frame0,text='Edit',padx=1,pady=1)
        self.btnEdit.pack(side=Tkinter.LEFT)
        submenu = Tkinter.Menu(self.btnEdit,tearoff=True)
        self.btnEdit['menu'] = submenu
        submenu.add_command(label='Rename',command=self.rename)
        submenu.add_command(label='Find/Replace Text',command=self.dialogFindReplaceText)
        submenu.add_command(label='Collapse/Expand',command=self.collapseExpand)
        submenu.add_command(label='Rebuild All Tree',command=lambda:self.newTree(os.getcwd()))
        submenu.add_command(label='Display Columns',command=self.displayColumns)
        submenu.add_separator() # додати розділювач
        submenu.add_command(label='Create Child Dir',command=self.appendChildDir)
        submenu.add_command(label='Create Child File',command=self.appendChildFile)
        submenu.add_command(label='Delete',command=self.removeChild)
        submenu.add_separator()
        submenu.add_command(label='Cut',command=self.cut)
        submenu.add_command(label='Copy',command=self.copy)
        submenu.add_command(label='Paste',command=self.paste)
        submenu.add_separator()
        submenu.add_command(label='Run Macro',command=self.runMacro)
        self.btnText = Tkinter.Menubutton(self.frame0,text='Text',padx=1,pady=1)
        self.btnText.pack(side=Tkinter.LEFT)
        submenu = Tkinter.Menu(self.btnText,tearoff=True)
        self.btnText['menu'] = submenu
        submenu.add_command(label='Close',command=self.save)
        submenu.add_command(label='Wrap',command=self.txtWrap)
        submenu.add_separator()
        submenu.add_command(label='Cut',command=self.cutText)
        submenu.add_command(label='Copy',command=self.copyText)
        submenu.add_command(label='Paste',command=self.pasteText)
        submenu.add_separator()
        submenu.add_command(label='Insert Template',command=self.dialogTemplate)
        self.btnPrev = Tkinter.Button(self.frame0,text="<<",padx=1,pady=1,command=self.historyPrev) # створити кнопку меню
        self.btnPrev.pack(side=Tkinter.LEFT) # розмістити компонент
        self.btnNext = Tkinter.Button(self.frame0,text=">>",padx=1,pady=1,command=self.historyNext) # створити кнопку меню
        self.btnNext.pack(side=Tkinter.LEFT) # розмістити компонент
        self.frame0.pack(side=Tkinter.TOP,fill=Tkinter.X)      
        
        #PanedWindow
        panedWindow=Tkinter.PanedWindow(self, orient=Tkinter.HORIZONTAL, sashrelief=Tkinter.RAISED)
        panedWindow.pack(fill=Tkinter.BOTH, expand=1)
             
        self.frame1 = Tkinter.Frame(self) # фрейм з Text
        self.txt = Tkinter.Text(self.frame1,wrap=Tkinter.NONE) # створити текстове поле
        self.txt['font']='Arial 10' # 'Courier 10'
        sbar_y1 = Tkinter.Scrollbar(self.frame1) # створити вертикальну смугу прокручування
        sbar_x1 = Tkinter.Scrollbar(self.frame1, orient=Tkinter.HORIZONTAL) # створити горизонтальну смугу прокручування
        sbar_y1.pack(side=Tkinter.RIGHT, fill=Tkinter.Y) # розмістити компоненти
        sbar_x1.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
        self.txt.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=1)
        sbar_y1['command'] = self.txt.yview # під час прокручування змінювати положення
        sbar_x1['command'] = self.txt.xview
        self.txt['yscrollcommand'] = sbar_y1.set # значення повзунка смуги прокручування
        self.txt['xscrollcommand'] = sbar_x1.set
        
        self.frame2 = Tkinter.Frame(self) # фрейм з tree
        sbar_y2 = Tkinter.Scrollbar(self.frame2) # створити вертикальну смугу прокручування
        sbar_x2 = Tkinter.Scrollbar(self.frame2,orient=Tkinter.HORIZONTAL) # створити горизонтальну смугу прокручування
        self.tree = ttk.Treeview(self.frame2) # створити дерево
        self.tree['selectmode']=Tkinter.BROWSE # дозволити вибір лише одного елементу (EXTENDED - мультіселект)
        self.tree['columns'] = ('path',) # добавити колонки
        self.tree.column('#0', width=300, anchor='w')# параметри колонки з деревом
        self.tree.column('path', width=100, anchor='w')# параметри колонки 'path'
        #self.tree['displaycolumns']=('path',) # показувати колонку 'path'
        self.tree['displaycolumns']=() # не показувати колонки
        self.tree.heading('#0', text='Item') # надпис на колонці з деревом
        self.tree.heading('path', text='Path') # надпис на колонці 'path'
        sbar_y2['command'] = self.tree.yview # під час прокручування змінювати положення дерева
        sbar_x2['command'] = self.tree.xview
        self.tree['yscrollcommand'] = sbar_y2.set # значення повзунка смуги прокручування
        self.tree['xscrollcommand'] = sbar_x2.set
        
        # розмістити компоненти
        sbar_y2.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        sbar_x2.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
        self.tree.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=1)
        
        # рядок стану внизу вікна
        self.statusBarVar=Tkinter.StringVar() # рядкова змінна для рядку стану
        status = Tkinter.Entry(self, textvariable=self.statusBarVar)
        status.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
        
        self.wm_state('zoomed') # розвернути на весь экран
        #sizex, sizey = self.wm_maxsize() #повернути max розмір
        #self.wm_geometry('%dx%d+0+0'%(sizex-6,600)) # установити розмір
        
        # розмістити компоненти на panedWindow
        panedWindow.add(self.frame2, minsize=50)
        panedWindow.add(self.frame1, minsize=50)
        
        # popup меню
        self.popup1 = Tkinter.Menu(self.tree, tearoff=0) # popup меню для tree
        self.popup1.add_command(label='Generate HTML',command=self.genHTML)
        self.popup1.add_command(label='Rename',command=self.rename)
        self.popup1.add_command(label='CopyName',command=self.btn2Click)
        self.popup1.add_command(label='Find/Replace Text',command=self.dialogFindReplaceText)
        self.popup1.add_command(label='Collapse/Expand',command=self.collapseExpand)
        self.popup1.add_command(label='Rebuild Node',command=self.rebuildTree)
        self.popup1.add_command(label='Dialog Template',command=self.dialogTemplate)
        self.popup1.add_separator() # додати розділювач
        self.popup1.add_command(label='Create Child Dir',command=self.appendChildDir)
        self.popup1.add_command(label='Create Child File',command=self.appendChildFile)
        self.popup1.add_command(label='Create NTFS Junction Point',command=self.appendChildJunction)
        self.popup1.add_command(label='Delete',command=self.removeChild)
        self.popup1.add_separator()
        self.popup1.add_command(label='Cut',command=self.cut)
        self.popup1.add_command(label='Copy',command=self.copy)
        self.popup1.add_command(label='Paste',command=self.paste)
        
        self.popup2 = Tkinter.Menu(self.txt, tearoff=0) # popup меню для txt
        self.popup2.add_command(label='Close',command=self.save)
        self.popup2.add_separator()
        self.popup2.add_command(label='Cut',command=self.cutText)
        self.popup2.add_command(label='Copy',command=self.copyText)
        self.popup2.add_command(label='Paste',command=self.pasteText)
        self.popup2.add_separator()
        self.popup2.add_command(label='Insert Template',command=self.dialogTemplate)
        
        # прив'язки до обробників подій
        self.tree.bind('<ButtonRelease-1>', self.btn1Click)
        self.tree.bind('<Double-ButtonRelease-1>', self.btn1dblClick)
        self.tree.bind('<Button-3>', self.btn3Click)
        self.tree.bind('<Button-2>', self.btn2Click)
        self.tree.bind('<Motion>', self.Motion)
        self.tree.bind('<<TreeviewSelect>>', self.treeSelect) # обробник події вибору
        self.tree.bind('<<TreeviewOpen>>', self.treeOpen) # обробник події відкриття піддерева
        self.tree.bind('<<TreeviewClose>>', self.treeClose) # обробник події закриття піддерева
        self.tree.bind('<FocusIn>', self.tree_focusIn)
        self.txt.bind('<FocusIn>', self.txt_focusIn)
        self.txt.bind('<FocusOut>', self.txt_focusOut)
        self.txt.bind('<Button-2>', self.txtBtn2Click)
        self.txt.bind('<Button-3>', self.txtBtn3Click)
        self.txt.bind('<Control-X>',self.cutText)
        self.txt.bind('<Control-C>',self.copyText)
        self.txt.bind('<Control-V>',self.pasteText)
        self.txt.bind('<Tab>',self.indent)
        self.txt.bind('<Key>',self.keyPressed)
        self.txt.bind('<Control-l>',self.manualParseText)
        self.bind('<F5>',self.historyPrev)
        self.bind('<F6>',self.historyNext)
        self.protocol("WM_DELETE_WINDOW", self.exit) # при закритті
        
        self.btnText['state']=Tkinter.DISABLED # заблокувати меню 'Text'
        
        # відкрити останню базу знань
        if os.path.exists('TreePyKB2.ini'):
            lastPath=open('TreePyKB2.ini','r').read().split('=')[1].decode('utf-8')
            if os.path.exists(lastPath):
                self.openKB(lastPath) # відкрити

    def historyPrev(self,event=None):
        '''Натиск F5. Перехід до попереднього в історії'''
        if self.historyIndex>0: # якщо поточний індекс історії >0
            self.historyIndex-=1 # індекс попереднього
            prev=self.history[self.historyIndex] # попередній
            if self.tree.exists(prev):
                self.tree.see(prev) # прокрутити
                self.tree.focus(prev) # установити фокус
        
    def historyNext(self,event=None):
        '''Натиск F6. Перехід до наступного в історії'''
        if self.historyIndex<len(self.history)-1: # якщо поточний індекс історії < останнього
            self.historyIndex+=1 # індекс наступного
            next=self.history[self.historyIndex] # наступний
            if self.tree.exists(next):
                self.tree.see(next) # прокрутити
                self.tree.focus(next) # установити фокус
            
    def historyAppend(self,nodeId):
        '''Додає nodeId в історію'''
        del self.history[self.historyIndex+1:] # видалити застарілу історію
        self.history.append(nodeId) # додати в історію
        if len(self.history)==101: # обмежити довжину історії до 100
            del self.history[0]
        self.historyIndex=len(self.history)-1 # поточний індекс = останній
                   
    def txtWrap(self):
        '''Переніс рядка в txt'''
        if self.txt['wrap']=='none':
            self.txt.config(wrap=Tkinter.CHAR)
        else:
            self.txt.config(wrap=Tkinter.NONE)
            
    def keyPressed(self,event):
        '''Натиснута клавіша у txt'''
        if event.keysym in ['Return','space']: # якщо клавіша в списку
            self.parseText() # може уповільнити роботу з дуже великими файлами
            
    def txt_focusOut(self,event):
        '''Фокус вводу txt втратило.'''
    
    def tree_focusIn(self,event):
        '''Фокус вводу tree отримало.'''
    
    def btn1Click(self,event):
        '''Обробник події відпускання кнопки 1 миші
         Додає в активне поле вводу вікна шаблону відносний шлях вибраного елементу дерева'''

        id=self.tree.focus() # id вибраного елемента дерева
        path=self.getRelPath(id) # відносний шлях вибраного елементу
        
        if self.dlgEntry!=None: # якщо поле вводу вікна шаблону під фокусом (активне)
            self.dlgEntry.delete(0, Tkinter.END) # очистити
            self.dlgEntry.insert(0, path) # вставити в поле текст
    
    def runMacro(self):
        '''Виконує макрос'''
        filename = askopenfilename(defaultextension='py',
            filetypes=[('Python files', '.py')]) # діалогове вікно відкриття файлу
        if filename: # якщо є ім'я файлу
            # замінити на субпроцес ???
            exec(open(filename,'r').read(),{'self':self,'ClassFile':ClassFile}) # виконати
        else: return # інакше вийти
                                               
    def importCode(self):
        '''Імпортує базу знань з файлу .py'''
        def save(ls):
            '''Зберігає рядки в файлі. Створює каталоги'''
            path=os.path.abspath(ls[0][6:]) # абсолютний шлях
            if os.path.basename(path)==self.classfile: # якщо це файл класу
                if not os.path.exists(os.path.dirname(path)): # якщо каталога не існує
                    os.mkdir(os.path.dirname(path)) # створити каталог
            f=open(path,'w') # відкрити файл
            for s in ls[1:]: # записати у файл усі рядки крім першого
                f.write(s+'\n')
            f.close() # закрити файл
            
        dir = askdirectory()# діалогове вікно вибору каталогу
        if not dir: return # якщо не вибрано, вийти
        os.chdir(dir) # задати робочий каталог
        filename = askopenfilename(defaultextension='py',
            filetypes=[('Python files', '.py')]) # діалогове вікно відкриття файлу
        if filename: # якщо є ім'я файлу
            code=open(filename,'r').read() # прочитати
        else: return # інакше вийти
        lines=code.splitlines() # список рядків
        ls=[] # список рядків для окремого файлу
        for line in lines: # для усіх рядків
            if line[0:6]=='#path=': # якщо є такий рядок
                if line is not lines[0]: # якщо рядок не перший у lines
                    save(ls) # зберегти рядки в файлі
                ls=[] # очистити
            ls.append(line) # додати рядок  
            if line is lines[-1]: # якщо рядок останній у lines
                save(ls) # зберегти рядки в файлі
        self.newTree(os.getcwd()) # перебудувати дерево на нове
        self.title(os.getcwd()) # заголовок вікна
                          
    def indent(self,event):
        '''Обробник події натиску Tab. Замість табуляції виводить 4 пробіли'''
        self.txt.insert(Tkinter.INSERT, ' '*4) # вставити 4 пробіли
        return 'break' # табуляцію не вставляти
        
    def Motion(self,event):
        '''Обробник події руху миші над деревом'''
        if event.state==12: # якщо натиснута клавіша Ctrl
            row=self.tree.identify_row(event.y) # ID елемента
            path=self.tree.set(row)['path'] # повний шлях
            self.statusBarVar.set(path) # показати в рядку стану
    
    def txt_focusIn(self,event):
        '''Фокус вводу txt отримало. Запам'ятовує self.editedId і блокує меню'''
        if self.editedId!=None: return # якщо редагується елемент у txt, вийти
        # інакше:
        self.editedId=self.tree.focus() # запам'ятати Id елемента, що буде редагуватись у txt
        self.btnFile['state']=Tkinter.DISABLED # заблокувати меню
        self.btnEdit['state']=Tkinter.DISABLED # заблокувати меню
        self.btnText['state']=Tkinter.NORMAL # розблокувати меню
        
    def txtBtn2Click(self,event):
        '''Обробник події натиску кнопки 2 миші.
        Зберігає файл, що редагувався в txt'''
        self.save() # зберегти файл
        
    def genHTML(self):
        '''Генерує HTML для файлу pykb'''
        id=self.tree.focus() # id вибраного елемента дерева
        path=self.tree.set(id)['path'] # повний шлях до файлу pykb
        if os.path.splitext(path)[1]!='.pykb': # якщо це не .pykb
            tkMessageBox._show('Warning','You must select .pykb file!',icon=tkMessageBox.WARNING,type=tkMessageBox.OK)
            return # то вийти
        pathHTML=os.path.splitext(path)[0]+'.html' # шлях до HTML
        if os.path.exists(pathHTML): # якщо HTML вже існує
            # діалогове вікно з запитанням 'Зберегти файл?'
            answer = tkMessageBox._show('Warning!','File exist. Save new file?',icon=tkMessageBox.QUESTION,type=tkMessageBox.YESNO)
            if answer=='no': return
        pathHTML=MakeCode.genHTML(os.path.relpath(path))# генерувати HTML для цього файлу  
        parentId=self.tree.parent(id)
        self.rebuildTree(parentId) # перебудувати гілку
            
    def save(self):
        '''Меню Text/Save. Зберігає файл, що редагувався в txt'''
        if self.editedId==None: return # якщо не редагується елемент у txt, вийти
        # інакше:
        # діалогове вікно з запитанням 'Зберегти файл?'
        answer = tkMessageBox._show('Save File','Save the current file?',icon=tkMessageBox.QUESTION,type=tkMessageBox.YESNOCANCEL)
        if answer == 'yes': # якщо 'так'
            fileName=self.tree.set(self.editedId)['path'] # повний шлях редагованого елемента
            self.writeFile(fileName) # зберегти
            #MakeCode.genHTML(os.path.relpath(fileName))# генерувати HTML для цього файлу  
        elif answer == 'cancel': # якщо 'відмінити'
            return # вийти
        # якщо 'так' або 'ні'
        self.tree.see(self.editedId)# прокрутити
        self.tree.focus(self.editedId)# знайти
        self.editedId=None # позначити, що ніщо не редагується
        self.btnFile['state']=Tkinter.NORMAL # розблокувати меню
        self.btnEdit['state']=Tkinter.NORMAL # розблокувати меню
        self.btnText['state']=Tkinter.DISABLED # заблокувати меню
                               
    def readFile(self,filename):
        '''Вставляє вміст файлу в self.txt'''
        self.txt.delete('1.0', Tkinter.END) # очистити txt
        if not os.path.isfile(filename):# якщо filename не файл
            classfile=os.path.join(filename,self.classfile) # шлях до файлу класу
            if os.path.isfile(classfile): # якщо існує цей файл
                filename=classfile # працюємо з ним
            else: # якщо файлу класу немає
                return  # вийти
        allowed=['.pykb','.py','.txt'] # список дозволених файлів
        # якщо файл не дозволено показувати в txt
        if os.path.splitext(filename)[1] not in allowed:
            self.txt.insert('1.0', "File type is not allowed to display...")
            return # вийти
        f=open(filename, 'r') # відкрити файл
        all=f.read() # прочитати все
        f.close() # закрити
        self.txt.insert('1.0', all) # вставити в txt
        if os.path.splitext(filename)[1] in ['.pykb','.py']: # якщо файли з таким розширенням
            if len(all)<10000: # якщо файл не дуже великий
                self.parseText() # аналізувати текст з посиланнями
            
    def writeFile(self,filename):
        '''Зберігає вміст self.txt у файл'''
        if not os.path.isfile(filename):# якщо filename не файл
            classfile=os.path.join(filename,self.classfile) # шлях до файлу класу
            if os.path.isfile(classfile): # якщо існує цей файл
                filename=classfile # працюємо з ним
            else: # якщо файлу класу немає
                return  # вийти
        f=open(filename, 'w')# відкрити файл
        all=self.txt.get('1.0', Tkinter.END)[0:-1] # весь текст окрім останнього символу
        f.write(all.encode('utf-8')) #записати у файл
        f.close() #закрити файл
           
    def treeOpen(self,event):
        '''Обробник події відкриття піддерева'''
        nodeId = self.tree.focus() # id вибраного елемента дерева
        self.tree.item(nodeId, open=1) # задати, що вузол відкритий
        path=os.path.join(self.tree.set(nodeId)['path'],self.classfile) # повний шлях
        if os.path.exists(path):# якщо файл існує
            f=ClassFile(path) # файл класу
            f.write(open=self.tree.item(nodeId, 'open').__str__()) # записати у файл класу
        
    def treeClose(self,event):
        '''Обробник події закриття піддерева'''
        nodeId = self.tree.focus() # id вибраного елемента дерева
        self.tree.item(nodeId, open=0) # задати, що вузол закритий
        path=os.path.join(self.tree.set(nodeId)['path'],self.classfile) # повний шлях
        if os.path.exists(path):# якщо файл існує
            f=ClassFile(path) # файл класу
            f.write(open=self.tree.item(nodeId, 'open').__str__()) # записати у файл класу
        
    def collapseExpand(self):
        '''Меню Collapse/Expand. Змінює стан'''
        nodeId = self.tree.focus() # id вибраного елемента дерева
        if self.tree.item(nodeId, 'open'):# якщо відкритий
            self.tree.item(nodeId, open=0) # закрити
        else: # якщо закритий
            self.tree.item(nodeId, open=1) # відкрити
        path=os.path.join(self.tree.set(nodeId)['path'],self.classfile) # повний шлях
        if os.path.exists(path):# якщо файл існує
            f=ClassFile(path) # файл класу
            f.write(open=self.tree.item(nodeId, 'open').__str__()) # записати в файл класу
                     
    def displayColumns(self):
        '''Меню. Сховати/Показати колонки'''
        if self.tree['displaycolumns']==('path',): # якщо показані
            self.tree['displaycolumns']=() # сховати
        else: # інакше
            self.tree['displaycolumns']=('path',) # показати
                
    def btn1dblClick(self,event):
        '''Обробник події відпускання кнопки 1 миші після подвійного натиску.
        Відкриває файл зовнішньою програмою'''
        nodeId = self.tree.focus() # id вибраного елемента дерева
        filename=self.tree.set(nodeId)['path'] # повний шлях
        
        pythonEditor=r"c:\Program Files\SciTE\SciTE.exe"
        #налаштуйте SciTE для показу *.pykb (в python.properties змініть file.patterns.py=*.py;*.pyw;*.pykb)
        pythonEditorCmd=pythonEditor+r' "-open:'+filename.replace("\\", r"\\")+'"'

#         #проблема
#         pythonEditor=r"d:\Portable\PyScripter\PyScripter.exe"
#         #налаштуйте PyScripter для показу *.pykb (Параметры среды разработки/Файловые фильтры)
#         pythonEditorCmd=pythonEditor+r" --PYTHON26 "+filename

        if os.path.isfile(filename):# якщо це файл, а не каталог
            if os.path.splitext(filename)[1] in ['.pykb','.py']: # якщо код python
                if os.path.exists(pythonEditor): # якщо є зовнішній редактор python
                    subprocess.Popen(pythonEditorCmd) # відкрити через нього
                else: # інакше    
                    os.system(r'start notepad.exe '+filename) # відкрити через notepad
            else: # інакше    
                os.startfile(filename) #виконує файл відповідним застосуванням

    def btn3Click(self,event):
        '''Обробник події натиску кнопки 3 миші. Викликає popup1'''
        self.tree.event_generate('<Button-1>', x=event.x, y=event.y) # генерувати подію
        if self.editedId==None: # якщо нічого не редагується
            self.popup1.post(event.x_root, event.y_root) # викликати popup1
            
    def txtBtn3Click(self,event):
        '''Обробник події натиску кнопки 3 миші. Викликає popup2'''
        if self.editedId!=None: # якщо щось редагується
            self.popup2.post(event.x_root, event.y_root) # викликати popup2
                  
    def btn2Click(self,event=None):
        '''Обробник події натиску кнопки 2 миші.
        Вставляє в поточну позицію txt посилання на вибраний елемент дерева'''

        if event:
            self.tree.event_generate('<Button-1>', x=event.x, y=event.y) # генерувати подію
        id=self.tree.focus() # id вибраного елемента дерева
        path=self.tree.set(id)['path'] # повний шлях
        
        if self.editedId!=None: # якщо щось редагується
            s='r"""'+os.path.relpath(path)+'"""' # рядок посилання на вибраний елемент
            self.txt.focus() # установити фокус на self.txt
            self.txt.insert(Tkinter.INSERT, s) # вставити в поточну позицію
        else: # інакше скопіювати в буфер
            self.clipboard_clear()             
            self.clipboard_append(os.path.relpath(path))
            
    def treeSelect(self,event):
        '''Обробник події вибору елемента'''
        nodeId = self.tree.focus() # id вибраного елемента дерева
        relPath=self.getRelPath(nodeId) # відносний шлях
        fullPath=os.path.join(self.KBdir,relPath) # повний шлях
        self.statusBarVar.set(relPath) # показати шлях в рядку стану
        if self.editedId==None: # якщо нічого не редагується у txt
            self.historyAppend(nodeId) # додати в історію
            self.readFile(fullPath) # читати файл
  
    def tagDblClick1(self,event):
        '''Подвійний натиск мишею на тезі. Знаходить відповідний елемент дерева або
        відриває URL чи файл відповідною програмою'''
        curInd=self.txt.index(Tkinter.CURRENT)#INSERT # індекс поточної позиції курсора
        curTag=self.txt.tag_names(curInd)[1] # тег за поточною позицією
        tagStart=self.txt.tag_ranges(curTag)[0] # індекс початку тега
        tagEnd=self.txt.tag_ranges(curTag)[1] # індекс кінця тега
        tagText=self.txt.get(tagStart,tagEnd) # текст тега
        
        # якщо URL
        if tagText.find("http://")==0:
            import webbrowser
            webbrowser.open(tagText) # відкрити в браузері
            #os.system(r'start firefox.exe '+tagText) # або так
            return
        
        # якщо файл
        # в кінці шляху (після #) можливий номер сторіки (місце в документі)
        filePath=tagText.split('#')[0] # відділити номер сторінки від шляху
        if os.path.isfile(filePath): # якщо файл
            fileExt=os.path.splitext(tagText)[1].split('#') # список [розширення, номер сторінки]
            if len(fileExt)==2: # якщо заданий номер сторінки
                # відкриває відповідною програмою з указанням номеру сторінки
                if fileExt[0] in ['.djvu','.djv']:
                    os.system(r'start c:\"Program Files"\WinDjView\WinDjView.exe '+'"'+tagText+'"')
                elif fileExt[0] in ['.pdf']:
                    os.system(r'start c:\"Program Files"\Adobe\"Reader 10.0"\Reader\AcroRd32.exe '+'/A "page='+fileExt[1]+'" "'+filePath+'"')
            else: # якщо не заданий номер сторінки
                os.startfile(tagText) # відкриває відповідною програмою
            return
        
        # інакше (якщо каталог)
        path=os.path.abspath(tagText) # перетворити в абсолютний шлях
        id=self.findItem(path,self.tree.get_children('')[0]) # знайти Id елемента в дереві
        if id==None:
            tkMessageBox._show('Not exist','Path not exist',icon=tkMessageBox.ERROR,type=tkMessageBox.OK)
        else:    
            self.tree.see(id)# прокрутити до id
            self.tree.focus(id)# знайти
            self.tree.tag_configure(id, background='yellow') # виділити знайдений
        return
             
    def findItem(self,path,item):
        '''Рекурсивно шукає Id вузла з path в дереві'''
        if self.tree.set(item)['path']==path: # якщо шлях=path
            return item # повертає ID
        elif len(self.tree.get_children(item))>0: # інакше якщо є діти
            for child in self.tree.get_children(item): # для усіх дітей
                item=self.findItem(path, child) # рекурсивно шукати
                if item: # якщо є ID
                    return item # повертає ID
                 
    def parseText_obsolete(self):
        '''Аналізує текст з посиланнями:
        - створює теги по заданому регулярному виразу,
        - конфігурує теги,
        - створює прив'язки'''
        text = self.txt.get(1.0, 'end') # весь текст
        tagName=0 # ім'я тега
        # для всіх знайдених об'єктів за заданим регулярним виразом
        for mo in re.finditer(r'""".*?"""', text):
            # добавити тег
            self.txt.tag_add(tagName,'1.0+%dc+3c'%mo.start(),'1.0+%dc-3c'%mo.end())
            # задати конфігурацію тега
            self.txt.tag_config(tagName, foreground='blue') #font=('arial', 12, 'bold')                        
            # створити прив'язки
            self.txt.tag_bind(tagName, '<Double-1>', self.tagDblClick1)
            self.txt.tag_bind(tagName, '<Enter>', lambda event: self.txt.config(cursor='arrow'))
            self.txt.tag_bind(tagName, '<Leave>', lambda event: self.txt.config(cursor='xterm'))  
            tagName+=1 # змінити ім'я тега
    
    def manualParseText(self,event):
        self.parseText() 
               
    def parseText(self):
        '''Проста підсвітка синтаксису Python. Не придатна для великих файлів!
        - створює теги по заданому регулярному виразу,
        - конфігурує теги,
        - створює прив'язки на посилання'''
        
        for tag in self.txt.tag_names(): # видалити усі тегі
            self.txt.tag_remove(tag, '1.0', 'end')
            
        kwLst=keyword.kwlist # список ключових слів Python
        kwStr=reduce(lambda x, y: x +'|'+ y, kwLst) # рядок ключових слів з розділювачем |
        # регулярні вирази:
        PY_KEYWORD_RE=r'\b(?:'+kwStr+r')\b' # ключові слова
        PY_COMMENT_RE=r'#.*' # коментар
        # рядковий літерал
        PY_STRING_LITERAL_RE = (
r"""[uU]?[rR]?(?:'''(?:[^'\\]|\\.|'{1,2}(?!'))*'''|'(?:[^'\n\\]|\\.)*'|"""+
r'''"""(?:[^"\\]|\\.|"{1,2}(?!"))*"""|"(?:[^"\n\\]|\\.)*")'''
)
        text = self.txt.get(1.0, 'end') # весь текст           
        tagName=0 # ім'я тега
        # для кожного знайденого об'єкта за регулярним виразом
        for mo in re.finditer(r'(?x)\#.*|'+PY_STRING_LITERAL_RE+'|'+PY_KEYWORD_RE, text, re.VERBOSE):
            if mo.group(0) in kwLst: # якщо ключове слово
                self.txt.tag_add('kw','1.0+%dc'%mo.start(),'1.0+%dc'%mo.end())# добавити тег
                self.txt.tag_config('kw', foreground='blue', font=('arial', 10, 'bold'))# задати конфігурацію тега                             
            elif mo.group(0)[0] =='#': # інакше якщо коментар
                self.txt.tag_add('comment','1.0+%dc'%mo.start(),'1.0+%dc'%mo.end())
                self.txt.tag_config('comment', foreground='darkgreen', font=('arial', 10, 'normal')) 
            elif mo.group(0)[0] in ['"',"'"] or mo.group(0)[0:2] in ['r"',"r'"]: # інакше якщо рядок
                self.txt.tag_add('string','1.0+%dc'%mo.start(),'1.0+%dc'%mo.end())
                self.txt.tag_config('string', foreground='red', font=('arial', 10, 'normal'))
            if mo.group(0)[0:4] =='r"""' and mo.group(0)[0:5] !='r"""\n': # якщо посилання
                self.txt.tag_add(tagName,'1.0+%dc+4c'%mo.start(),'1.0+%dc-3c'%mo.end())
                self.txt.tag_config(tagName, foreground='blue', font=('arial', 10, 'normal'))                      
                # створити прив'язки
                self.txt.tag_bind(tagName, '<Double-1>', self.tagDblClick1)
                self.txt.tag_bind(tagName, '<Enter>', lambda event: self.txt.config(cursor='arrow'))
                self.txt.tag_bind(tagName, '<Leave>', lambda event: self.txt.config(cursor='xterm'))  
                tagName+=1 # змінити ім'я тега
                
    def delChildren(self,id=''):
        '''Видаляє усіх дітей елемента id'''
        ch_list=self.tree.get_children(id) # діти елемента id
        if len(ch_list)!=0: # якщо є діти
            for ch in ch_list: # видалити усіх дітей
                self.tree.delete(ch)
                             
    def rebuildTree(self,rt=None):
        '''Перебудовує дерево з корнем rt'''
        if rt==None: rt=self.tree.focus() # якщо не задано, то id вибраного елемента дерева
        path=self.tree.set(rt)['path'] # повний шлях
        self.delChildren(rt) # видалити усіх дітей
        self.buildTree(path,rt) # будувати дерево
        self.tree.focus(rt) # установити фокус на rt
        self.tree.selection_set(rt) # виділити rt
        self.history=[] # очистити історію
        self.historyIndex=0
        
    def newTree(self,path):
        '''Перебудовує повне дерево зі шляхом path'''
        self.delChildren('') # видалити усіх дітей
        # добавити корінь
        rt=self.tree.insert('', 'end', text=os.path.basename(path), image=self.images[0], open=1)
        self.tree.set(rt, 'path', path) # задати значення в колонці 'path'  
        self.buildTree(path, rt) # будувати дерево    
        self.tree.focus(rt) # установити фокус на rt
        self.tree.selection_set(rt) # виділити rt
        self.history=[] # очистити історію
        self.historyIndex=0
    
    def getItemPathList(self,n,pathList=[]):
        """Повертає список компонентів відносного шляху вузла дерева з індексом n.
        Рекурсивна"""
        if n!='': # якщо не корінь
            pathList=[self.tree.item(n)['text']]+pathList
            p=self.tree.parent(n) # індекс батька
            pathList=self.getItemPathList(p, pathList) # рекурсія
        return pathList
    
    def getRelPath(self, n):
        """Повертає відносний шлях вузла дерева з індексом n"""
        pathList=self.getItemPathList(n)
        return u"\\".join(pathList[1:]) # корінь пропускаємо!
    
    def getFullPath(self, n):
        """Повертає повний шлях вузла дерева з індексом n"""
        relPath=self.getRelPath(n)
        return os.path.join(self.KBdir, relPath)
               
    def addItemPictire(self,fullname,n):
        # додаємо рисунок
        picfile=os.path.join(fullname, 'class.ppm')
        if os.path.exists(picfile): # якщо файл рисунку існує
            # рисунки потрібно зберігати в глобальній змінній self.images
            self.images.append(Tkinter.PhotoImage(file=picfile))
            self.tree.item(n,image=self.images[-1])
        else: # якщо файл рисунку не існує
            parentImage=self.tree.item(self.tree.parent(n))['image']
            self.tree.item(n,image=parentImage) # задати такий рисунок як у предка             
            #self.tree.item(n,image=self.images[0]) # стандартний рисунок
                   
    def buildTree(self,dir,parent=''):
        """Будує дерево каталогів у ttk.Treeview""" 
        # для усіх файлів pykb у дереві
        for root, dirs, files in os.walk(dir): #генератор os.walk
            for f in files:
                # вставити елемент-файл дерева
                n=self.tree.insert(parent, 'end', text=f, open=0)
            for f in dirs:
                # вставити елемент-каталог дерева    
                n=self.tree.insert(parent, 'end', text=f, open=1)
                fullname = os.path.join(root, f) # повний шлях
                
                self.addItemPictire(fullname, n) # додати рисунок

                self.buildTree(fullname,n) #рекурсія
            break
        
                
            
                       
    def buildTree2(self,dir,parent=''):
        '''Будує дерево каталогів у ttk.Treeview. Рекурсивна'''

        for f in os.listdir(dir): # для усіх файлів в каталозі 
            fullname = os.path.join(dir, f) # повний шлях
            #if type(fullname).__name__=='unicode':
            #    fullname=fullname.encode('utf-8')
            if os.path.isdir(fullname): # якщо каталог
                classfile=os.path.join(fullname, self.classfile) # файл класу
                if os.path.exists(classfile):# якщо файл класу (каталогу) існує
                    isOpened,fg,bg=self.readClassFile(classfile) # читати параметри
                else:# якщо файл не існує
                    isOpened,fg,bg=0,'black','white' # параметри за замовчуванням
                
                # вставити елемент-каталог дерева    
                n=self.tree.insert(parent, 'end', text=f.decode('utf-8'), open=isOpened)
                
                # додаємо рисунок
                picfile=os.path.join(fullname, 'class.ppm')
                if type(picfile).__name__!='unicode':
                    picfile=picfile.decode('utf-8')# має бути в unicode
                if os.path.exists(picfile): # якщо файл рисунку існує
                    # рисунки потрібно зберігати в глобальній змінній self.images
                    self.images.append(Tkinter.PhotoImage(file=picfile))
                    self.tree.item(n,image=self.images[-1])
                else: # якщо файл рисунку не існує
                    parentImage=self.tree.item(self.tree.parent(n))['image']
                    self.tree.item(n,image=parentImage) # задати такий рисунок як у предка             
                    #self.tree.item(n,image=self.images[0]) # стандартний рисунок
                
                self.tree.set(n, 'path', fullname.decode('utf-8')) # задати значення в колонці 'path'
                self.tree.item(n, tags=(n,)) # створити тег
                self.tree.tag_configure(n, foreground=fg,background=bg) # задати колір                
                self.buildTree(fullname,n) #рекурсія
            else: # якщо файл
                n=self.tree.insert(parent, 'end', text=f.decode('utf-8'), open=0) # вставити елемент-файл дерева
                self.tree.set(n, 'path', fullname.decode('utf-8')) # задати значення в колонці 'path'
                isOpened,fg,bg=self.readClassFile(fullname)
                self.tree.item(n, tags=(n,)) # створити тег
                self.tree.tag_configure(n, foreground=fg,background=bg) # задати колір
        
    def readClassFile(self,filename):
        '''Повертає кортеж опцій ('open','fg','bg') з файлу'''
        f=ClassFile(filename) # об'єкт файлу з опціями (.pykb)  
        d=f.read('open','fg','bg') # читати опції в словник d
        if 'open' in d: isOpened=d['open'] # якщо є ключ 'open', взяти значення
        else: isOpened=0 # інакше значення за замовчуванням
        if 'fg' in d: fg=d['fg']
        else: fg='black'
        if 'bg' in d: bg=d['bg']
        else: bg='white'
        return isOpened,fg,bg # повертає кортеж опцій
    
    def makeCode(self):
        '''Формує і повертає виконуваний Python код'''
        # передає також в виконуваний Python код змінну зі шляхом до редактора KB
        return MakeCode.makeCode(os.getcwdu(),self.programDir) # код для робочого каталогу
                                        
    def run(self):
        '''Меню File/Run. Виконує Python код в окремому просторі імен'''
        ns={} # простір імен
        code=self.makeCode() # отримати весь код
        self.iconify() # звернути
        exec(code, ns) # виконати код в просторі імен
        del ns
              
    def exportCode(self):
        '''Експортує код (класи, об'єкти, скрипти) в файл .py'''
        #filename = asksaveasfilename(defaultextension='py',
        #    filetypes=[('Python files', '.py')]) # діалогове вікно збереження файлу
        filename='generatedKBcode.py' # зберігає у папку з KB
        if filename: # якщо є ім'я файлу
            code=self.makeCode() # отримати весь код
            f=open(filename,'w') # відкрити файл для запису
            f.write(code) # зберегти
            f.close() 
                  
    def copyText(self):
        '''Меню Text/Copy. Копіює текст в буфер'''
        text = self.txt.get(Tkinter.SEL_FIRST, Tkinter.SEL_LAST)                  
        self.txt.clipboard_clear()             
        self.txt.clipboard_append(text)
        
    def cutText(self):
        '''Меню Text/Cut. Вирізає текст в буфер'''
        text = self.txt.get(Tkinter.SEL_FIRST, Tkinter.SEL_LAST)        
        self.txt.delete(Tkinter.SEL_FIRST, Tkinter.SEL_LAST)           
        self.txt.clipboard_clear()             
        self.txt.clipboard_append(text)
        
    def pasteText(self):
        '''Меню Text/Paste. Вставляє з буферу в задану позицію'''
        try:
            text = self.txt.clipboard_get()
            self.txt.insert(Tkinter.INSERT, text)
        except Tkinter.TclError:
            pass
                
    def new(self,ask=True):
        '''Меню File/New. Створює нову базу знань'''
        dir = askdirectory()# діалогове вікно вибору каталогу
        if not dir: return # якщо не вибрано, вийти
        subDir=tkSimpleDialog.askstring('Dir name', 'Enter dir name') # ввід назви каталогу
        # перевірити коректність назви каталогу
        if not subDir: return
        if not self.validFileName(subDir): return
        dir=os.path.join(dir,subDir)
        if os.path.exists(dir): # якщо шлях існує, вивести повідомлення
            tkMessageBox._show('Error','Dir '+dir+' exist',
                       icon=tkMessageBox.ERROR,type=tkMessageBox.OK)
        else: # інакше
            os.mkdir(dir) # створити каталог
            os.chdir(dir) # робочий каталог
            open(os.path.join(dir,self.classfile),'w').close() #створити файл класу
            self.newTree(os.getcwd()) # будувати дерево робочого каталогу
            self.writeLastPath(dir) # записати в ini файл шлях до останньої робочої папки
            self.title(os.getcwd()) # заголовок вікна
            
    def openKB(self,dir=None):
        '''Меню File/Open. Відкрити базу знань'''
        if dir==None:
            dir = askdirectory()# діалогове вікно вибору папки
        if dir: # якщо є ім'я папки
            os.chdir(dir) # робочий каталог
            self.KBdir=os.getcwdu()
            self.newTree(os.getcwdu()) # будувати дерево робочого каталогу
            self.writeLastPath(dir) # записати в ini файл шлях до останньої робочої папки
            self.title(os.getcwdu()) # заголовок вікна
    
    def writeLastPath(self,path):
        '''Записує в ini файл шлях до останньої робочої папки'''
        f=os.path.join(self.programDir,'TreePyKB2.ini')
        s=u'lastPath='+path
        open(f,'w').write(s.encode('utf-8'))
                   
    def exit(self):
        '''Меню File/Exit. Вихід'''
        self.destroy() # знищити віджет
        self.quit() # вийти з інтерпретатору Tcl
        
    def cut(self):
        '''Меню Edit/Cut. Вирізати піддерево'''
        nodeId=self.tree.focus() # id вибраного елемента дерева
        path=self.tree.set(nodeId)['path'] # повний шлях
        self.srcPath=(path,0) # запам'ятати шлях і позначити, що він вирізається
        
    def copy(self):
        '''Меню Edit/Copy. Копіювати піддерево'''
        nodeId=self.tree.focus() # id вибраного елемента дерева
        path=self.tree.set(nodeId)['path'] # повний шлях
        self.srcPath=(path,1) # запам'ятати шлях і позначити, що він копіюється
        
    def paste(self):
        '''Меню Edit/Paste. Вставити піддерево у каталог'''
        nodeId=self.tree.focus() # id вибраного елемента дерева
        path=self.tree.set(nodeId)['path'] # повний шлях каталогу, в який вставляємо
        dstPath=os.path.join(path,os.path.basename(self.srcPath[0])) # шлях призначення
        # якщо шлях пустий або dstPath вже існує або це не каталог, вийти
        if self.srcPath[0]=='' or os.path.exists(dstPath) or not os.path.isdir(path): return
        # інакше вставляємо:
        if self.srcPath[1]: # якщо копіюється
            if os.path.isdir(self.srcPath[0]): # якщо копіюється каталог
                shutil.copytree(self.srcPath[0], dstPath) # копіювати дерево
            else:
                shutil.copy(self.srcPath[0], dstPath) # копіювати файл
        else: # якщо вирізається
            shutil.move(self.srcPath[0], dstPath) # вирізати
            self.hiperLinksReplace(self.srcPath[0], dstPath) # замінити усюди посилання
        self.newTree(os.getcwd()) # перебудувати дерево !!!!!!! оптимізувати !!!!!!!   
        self.srcPath=('',1) # очистити
        
    def removeChild(self):
        '''Меню Edit/Delete. Видалити елемент'''
        nodeId=self.tree.focus() # id вибраного елемента дерева
        path=self.tree.set(nodeId)['path'] # повний шлях
        # діалогове вікно з запитанням
        answer = tkMessageBox._show('Delete','Delete the path?',icon=tkMessageBox.QUESTION,type=tkMessageBox.YESNO)
        if answer == 'yes':
            jp=JunctionPoints.LinkDestination(path)
            if jp: # якщо точка з'єднання (посилання на каталог)
                JunctionPoints.DeleteSymbolicLinks([path]) # видалити точку з'єднання
            elif os.path.isdir(path): # якщо каталог
                shutil.rmtree(path) # видалити каталог
            else: # інакше
                os.remove(path) # видалити файл
            self.tree.delete(nodeId)# повністю видалити вузол дерева
            
    def appendChildDir(self):
        '''Меню Edit/CreateChildDir. Добавити дочірній каталог'''
        nodeId=self.tree.focus() # id вибраного елемента дерева
        path=self.tree.set(nodeId)['path'] # повний шлях
        if not os.path.isdir(path): # якщо це не каталог, вивести попередження
            tkMessageBox._show('Error','Select a dir!',icon=tkMessageBox.ERROR,type=tkMessageBox.OK)
            return # вийти
        name=askstring2('Dir name', 'Enter dir name', 'new') # ввід назви
        if name==None: return # якщо ім'я None (вибрано Cancel), вийти
        if not self.validFileName(name): # якщо ім'я некоректне, вийти
            tkMessageBox._show('Warning','Incorrect file name',icon=tkMessageBox.WARNING,type=tkMessageBox.OK)
            return
        n=os.path.join(path,name)
        if os.path.exists(n): # якщо шлях інує, вивести попередження
            tkMessageBox._show('Error','Path '+n+' exist',icon=tkMessageBox.ERROR,type=tkMessageBox.OK)
            return # вийти
        os.mkdir(n) # створити каталог
        # вставити в дерево
        id=self.tree.insert(nodeId, 'end',text=os.path.basename(n),image=self.images[0])
        self.tree.set(id, 'path', n)
        open(os.path.join(n,self.classfile),'w').close()#створити файл класу
        classFileId=self.tree.insert(id, 'end',text=self.classfile)
        self.tree.set(classFileId, 'path', os.path.join(n,self.classfile))
        # прокрутити і вибрати щойно створений елемент
        self.tree.see(id)
        self.tree.focus(id)
        self.tree.selection_set(id)
        
    def appendChildJunction(self):
        '''Меню Edit/Create NTFS Junction Point. Добавити дочірню точку з'єднання на каталог'''
        nodeId=self.tree.focus() # id вибраного елемента дерева
        path=self.tree.set(nodeId)['path'] # повний шлях
        if not os.path.isdir(path): # якщо це не каталог, вивести попередження
            tkMessageBox._show('Error','Select a dir!',icon=tkMessageBox.ERROR,type=tkMessageBox.OK)
            return # вийти
        name=askstring2('Junction name', 'Enter junction name', 'new') # ввід назви
        if name==None: return # якщо ім'я None (вибрано Cancel), вийти
        if not self.validFileName(name): # якщо ім'я некоректне, вийти
            tkMessageBox._show('Warning','Incorrect file name',icon=tkMessageBox.WARNING,type=tkMessageBox.OK)
            return
        n=os.path.join(path,name)
        if os.path.exists(n): # якщо шлях інує, вивести попередження
            tkMessageBox._show('Error','Path '+n+' exist',icon=tkMessageBox.ERROR,type=tkMessageBox.OK)
            return # вийти
        
        dir = askdirectory()# діалогове вікно вибору каталогу
        if not dir: return # якщо не вибрано, вийти
        JunctionPoints.utilityPath=os.path.join(self.programDir, "junction.exe") # шлях до утіліти
        if os.path.exists(JunctionPoints.utilityPath):
            JunctionPoints.CreateSymbolicLinks([[os.path.normcase(dir), os.path.normcase(n)]]) # створити точку з'єднання
            self.rebuildTree() # перебудувати вузол
                            
    def appendChildFile(self):
        '''Меню Edit/CreateChildFile. Добавити дочірній файл'''
        nodeId=self.tree.focus() # id вибраного елемента дерева
        path=self.tree.set(nodeId)['path'] # повний шлях
        if not os.path.isdir(path): # якщо це не каталог, вивести попередження
            tkMessageBox._show('Error','Select a dir!',icon=tkMessageBox.ERROR,type=tkMessageBox.OK)
            return # вийти
        name=askstring2('File name', 'Enter file name', 'prop.pykb') # ввід назви
        if name==None: return # якщо ім'я None (вибрано Cancel), вийти
        if not self.validFileName(name): # якщо ім'я некоректне, вийти
            tkMessageBox._show('Warning','Incorrect file name',icon=tkMessageBox.WARNING,type=tkMessageBox.OK)
            return
        n=os.path.join(path,name)
        if os.path.exists(n): # якщо шлях інує, вивести попередження
            tkMessageBox._show('Error','Path '+n+' exist',icon=tkMessageBox.ERROR,type=tkMessageBox.OK)
            return # вийти
        f=open(n,'w')
        f.write("#open=0\n#fg=red\n#bg=white\n")
        f.close() # створити файл
        # вставити в дерево
        id=self.tree.insert(nodeId,'end',text=os.path.basename(n))
        self.tree.set(id,'path',n)            
        # прокрутити і вибрати щойно створений елемент
        self.tree.see(id)
        self.tree.focus(id)
        self.tree.selection_set(id)        
        
    def validFileName(self, baseName):
        '''Перевіряє коректність імені файла'''
        if baseName=='' or set(baseName).intersection('\\/:*?"<>|'): # якщо ім'я '' або некоректне
            return False
        else:
            return True
                       
    def rename(self):
        '''Меню Edit/Rename. Переименування елемента'''
        nodeId = self.tree.focus() # id вибраного елемента дерева
        path=self.tree.set(nodeId)['path'] # повний шлях
        oldPath=path # старий шлях
        dirName=os.path.dirname(path) # перша частина шляху (каталог)
        #baseName=tkSimpleDialog.askstring('Rename', 'Enter new name') # ввід назви
        baseName=askstring2('Rename', 'Enter new name',oldString=os.path.basename(path)) # ввід назви
        if baseName==None: return # якщо ім'я None (вибрано Cancel), вийти
        if not self.validFileName(baseName): # якщо ім'я некоректне
            tkMessageBox._show('Warning','Incorrect file name',icon=tkMessageBox.WARNING,type=tkMessageBox.OK)
            return
        path=os.path.join(dirName,baseName) # новий шлях
        if os.path.basename(oldPath)!=os.path.basename(path): # якщо введено нове ім'я
            if os.path.exists(path): # якщо новий шлях існує
                #вивести попередження
                tkMessageBox._show('Warning','Path exist',icon=tkMessageBox.WARNING,type=tkMessageBox.OK) 
                return # вийти
            # якщо старий шлях існує 
            if os.path.exists(oldPath):
                os.rename(oldPath, path) # переіменувати
                self.tree.item(nodeId, text=os.path.basename(path)) # змінити текст вузла
                #self.rn(nodeId,oldPath, path) # змінити значення колонки 'path' у вузла і дітей
                #або так:
                self.tree.set(nodeId,'path',path)
                if os.path.isdir(path): # якщо це каталог
                    self.rebuildTree(nodeId) # перебудувати його дерево
                self.hiperLinksReplace(oldPath, path) # замінити усюди посилання
                                    
    def hiperLinksReplace(self,oldPath,newPath):
        '''Замінює всюди старе гіперпосилання на нове'''
        old='r"""'+os.path.relpath(oldPath)+'\\' # старе гіперпосилання (початок шляху)
        new='r"""'+os.path.relpath(newPath)+'\\' # нове гіперпосилання (початок шляху)
        self.replaceText(os.getcwd(), old.encode('utf-8'), new.encode('utf-8')) #замінити всюди
        old='r"""'+os.path.relpath(oldPath)+'"""' # старе гіперпосилання
        new='r"""'+os.path.relpath(newPath)+'"""' # нове гіперпосилання
        self.replaceText(os.getcwd(), old.encode('utf-8'), new.encode('utf-8')) #замінити всюди
                
    def rn(self,id,oldpath,newpath): # функція ніде не використовується!
        '''Рекурсивно змінює значення колонки 'path' у вузла і дітей з oldpath на newpath'''
        old=self.tree.set(id)['path']
        new=old.replace(oldpath,newpath,1)
        self.tree.set(id, 'path', new)
        if self.tree.get_children(id):
            for i in self.tree.get_children(id):
                self.rn(i,oldpath,newpath)
                            
    def replaceText(self,dir,old,new,lst=None):
        '''Рекурсивно замінює у тексті всіх файлів '.pykb' дерева dir рядок old на new'''
        for f in os.listdir(dir): # для усіх файлів в каталозі 
            fullname = os.path.join(dir, f) # повний шлях
            if os.path.isdir(fullname): # якщо каталог                
                self.replaceText(fullname,old,new,lst) #рекурсія
            else: # якщо файл
                if os.path.splitext(f)[1]=='.pykb': #якщо розширення '.pykb'
                    file=open(fullname, 'r') #відкрити для читання
                    text=file.read() #прочитати все
                    newtext=text.replace(old, new) #замінити в тексті рядок old на new
                    file.close() #закрити
                    if newtext!=text: #якщо заміну виконано
                        file=open(fullname, 'w') #відкрити для запису
                        file.write(newtext) #записати новий варіант файлу
                        file.close() #закрити
                        if lst:
                            # добавити в Listbox
                            lst.insert(Tkinter.END,os.path.relpath(fullname))
                       
    def findText(self,dir,text,lst):
        '''Рекурсивно шукає текст у файлах '.pykb' дерева dir'''
        for f in os.listdir(dir): # для усіх файлів в каталозі 
            fullname = os.path.join(dir, f) # повний шлях
            if os.path.isdir(fullname): # якщо каталог                
                self.findText(fullname,text,lst) #рекурсія
            else: # якщо файл
                if os.path.splitext(f)[1]=='.pykb': #якщо розширення '.pykb'
                    file=open(fullname, 'r') #відкрити для читання
                    s=file.read() #прочитати все
                    if s.find(text)!=-1: # якщо є текст
                        # добавити в Listbox
                        lst.insert(Tkinter.END,os.path.relpath(fullname))
                    file.close() #закрити
                            
    def dialogFindReplaceText(self):
        '''Діалог пошука/заміни у тексті усіх файлів '.pykb' дерева dir
        Використовуйте заміну уважно!'''                
        def okClick(event=None): # якщо натискається кнопка або Enter
            text=entry.get().encode('utf-8') # текст у entry
            lst.delete(0, Tkinter.END) # очистити lst
            if chkButtonVar.get()==True: # якщо заміна
                textRn=entryRn.get().encode('utf-8')
                self.replaceText(path,text,textRn,lst) # замінити текст
            else: # інакше пошук
                self.findText(path,text,lst) # знайти текст
            
        def lstDblClick(event): # якщо подвійний натиск на lst
            if lst.size()==0: return # якщо lst чистий, вийти
            p=lst.get(lst.curselection()[0]) # вибраний елемент
            self.readFile(p) # читати файл
            i=self.findItem(os.path.abspath(p),self.tree.get_children('')[0]) # знайти id
            self.tree.see(i) # прокрутити
            self.tree.focus(i) # знайти
            
        id=self.tree.focus() # id вибраного елемента дерева
        path=self.tree.set(id)['path'] # повний шлях
        if type(path).__name__=='str':
            path=path.decode('utf-8')
        if not os.path.isdir(path): return # якщо не каталог вийти
                                              
        top = Tkinter.Toplevel() # створити вікно
        top.title("Find/Replace text") # заголовок
        top.grab_set() # зробити вікно модальним
        
        entry = Tkinter.Entry(top, width=85, fg='red') # поле вводу
        entry.pack(fill=Tkinter.X, expand=1,anchor=Tkinter.N) # розмістити
        entry.bind('<Return>',okClick) # обробник події <Return>
        entry.focus() # установити фокус
        
        entryRn = Tkinter.Entry(top, width=85, fg='blue') # поле вводу
        entryRn.pack(fill=Tkinter.X, expand=1) # розмістити
        entryRn.bind('<Return>',okClick) # обробник події <Return>
        
        frame=Tkinter.Frame(top) # фрейм
        frame.pack(fill=Tkinter.BOTH, expand=1) # розмістити
        lst=Tkinter.Listbox(frame, width=85, height=15, exportselection=0) # список
        lst.bind('<Double-ButtonRelease-1>', lstDblClick) # обробник події DblClick
        sbar_y = Tkinter.Scrollbar(frame) # створити вертикальну смугу прокручування
        sbar_x = Tkinter.Scrollbar(frame, orient=Tkinter.HORIZONTAL) # створити горизонтальну смугу прокручування
        sbar_y.pack(side=Tkinter.RIGHT, fill=Tkinter.Y) # розмістити компоненти
        sbar_x.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
        lst.pack(side=Tkinter.LEFT,fill=Tkinter.BOTH, expand=1)
        sbar_y['command'] = lst.yview # під час прокручування змінювати положення
        sbar_x['command'] = lst.xview
        lst['yscrollcommand'] = sbar_y.set # значення повзунка смуги прокручування
        lst['xscrollcommand'] = sbar_x.set
        
        chkButtonVar=Tkinter.BooleanVar() # булева змінна для chkButton
        chkButton=Tkinter.Checkbutton(top,text='Replace',variable=chkButtonVar)
        chkButton.pack(side=Tkinter.LEFT) # розмістити
        
        button = Tkinter.Button(top, text="Start", command=okClick) # кнопка
        button.pack(side=Tkinter.LEFT) # розмістити
        
    def about(self):
        '''Меню File/About'''
        top = Tkinter.Toplevel() # створити вікно
        top.title("about") # назва
        top.resizable(0,0) # не можна змінювати розмір
        top.focus_set() # установити фокус
        about = __doc__ # рядок документації модуля
        info = Tkinter.Label(top,text=about) # віджет надпису
        info.pack(side=Tkinter.TOP,padx=6) # розмістити
        button = Tkinter.Button(top, text="Dismiss", command=top.destroy) # кнопка
        button.pack(side=Tkinter.BOTTOM) # розмістити
        
    def dialogTemplate(self):
        '''Меню Text/InsTemplate. Створює діалогове вікно для заповнення шаблона коду. Вставляє шаблон'''
        # !!! поміняти місцями obj і subj
        def okClick(): # якщо натискається кнопка
            p1=entry1.get() # текст у entry1
            p2=lst1.get(lst1.curselection()[0]) # вибраний предикат
            p3=entry2.get() # текст у entry2
            p4=lst2.get(lst2.curselection()[0]) # вибраний ключ шаблону
            s=tempdic[p4] # вибраний шаблон
            s=s.format(obj=p1.encode('utf-8'),pred=p2.encode('utf-8'),subj=p3.encode('utf-8')) # форматувати шаблон
            if self.editedId!=None: # якщо щось редагується
                self.txt.insert(Tkinter.INSERT, s.decode('utf-8')) # вставити в txt
            else: # інакше скопіювати в буфер
                self.clipboard_clear()             
                self.clipboard_append(s.decode('utf-8'))
            exit() # знищити вікно
            
        def lst2Select(event): # якщо вибирається ключ шаблону 
            entry1['state']=Tkinter.DISABLED # зробити недоступним
            lst1['state']=Tkinter.DISABLED
            entry2['state']=Tkinter.DISABLED
            p=lst2.get(lst2.curselection()[0]) # вибраний ключ шаблону
            s=tempdic[p] # вибраний шаблон
            button['state']=Tkinter.NORMAL # зробити доступною
            if s.find('{obj}')!=-1: # якщо в шаблоні є текст '{obj}'
                entry1['state']=Tkinter.NORMAL # зробити доступним
            if s.find('{pred}')!=-1:
                lst1['state']=Tkinter.NORMAL
            if s.find('{subj}')!=-1:
                entry2['state']=Tkinter.NORMAL
        
        def exit(): # якщо знищується вікно
            self.dlgEntry=None # немає активних полів вводу
            top.destroy() # знищити вікно
            
        def entryFocusIn(event): # якщо поле вводу отримало фокус
            self.dlgEntry=event.widget # активне поле вводу
            
        from templates import tempdic # словник шаблонів
        keys= tempdic.keys() # список ключів
        keys.sort() # сортувати список
            
        top = Tkinter.Toplevel() # створити вікно
        top.title("Dialog Template") # заголовок
        top.protocol("WM_DELETE_WINDOW", exit) # при закритті
        top.attributes('-topmost',1) # завжди зверху
        
        lst2=Tkinter.Listbox(top, width=85, height=15, exportselection=0) # список
        for x in keys: # заповнити список ключами словника
            lst2.insert(Tkinter.END,x)
        lst2.pack(fill=Tkinter.X, expand=1) # розмістити
        lst2.bind('<<ListboxSelect>>', lst2Select) # обробник події вибору 
        
        entry1 = Tkinter.Entry(top, width=85, fg='blue') # поле вводу
        entry1.pack(fill=Tkinter.X, expand=1) # розмістити
        entry1.bind('<FocusIn>', entryFocusIn) # обробник події <FocusIn>
        
        if self.editedId!=None: # якщо щось редагується
            nodeID=self.editedId # id редагованого елемента
        else:
            nodeID=self.tree.focus() # id вибраного елемента дерева
        pth=os.path.relpath(self.tree.set(nodeID)['path']) # відносний шлях елементу
        if os.path.isfile(pth): # якщо це файл
            pth=os.path.dirname(pth) # використовувати лише шлях до каталогу
        entry1.delete(0, Tkinter.END) # очистити
        entry1.insert(0, pth) # вставити шлях
        #entry1.xview(Tkinter.END)
           
        lst1=Tkinter.Listbox(top, width=85, height=10, exportselection=0,fg='darkgreen') # список
        for x in ['isCause','isEffect','isReference','hasReference','isDependence','hasDependence','And','Or','Not','SubClassOf']: # заповнити список
            lst1.insert(Tkinter.END,x) # заповнити список
        lst1.pack(fill=Tkinter.X, expand=1) # розмістити
        lst1.selection_set(0) # вибрати перший
        
        entry2 = Tkinter.Entry(top, width=85, fg='red') # поле вводу
        entry2.pack(fill=Tkinter.X, expand=1) # розмістити
        entry2.bind('<FocusIn>', entryFocusIn) # обробник події <FocusIn>
        entry2.focus() # установити фокус (self.dlgEntry=entry2)
                
        button = Tkinter.Button(top, text="Insert", command=okClick) # кнопка
        button.pack() # розмістити
        button['state']=Tkinter.DISABLED # зробити недоступною
        if self.editedId==None: # якщо нічого не редагується
            button['text']="Copy to clipboard" # змінити текст
                                       
#####################################################################
class MyQueryString(tkSimpleDialog._QueryString):
    '''Клас діалога запиту рядка успадкований від tkSimpleDialog._QueryString.
    Додатково показує рядок oldString в entry при створенні діалога'''
    def __init__(self, title, prompt, oldString):
        self.__oldString = oldString # рядок, який показується в entry при створенні діалога
        tkSimpleDialog._QueryString.__init__(self, title, prompt)
    def body(self, master):
        entry = tkSimpleDialog._QueryString.body(self, master)
        entry.insert(Tkinter.END, self.__oldString) # вставити self.__oldString в entry
        return entry
def askstring2(title, prompt, oldString):
    '''Модифікована функція tkSimpleDialog.askstring().
    Додатково показує рядок oldString в entry при створенні діалога'''
    d = MyQueryString(title, prompt, oldString)
    return d.result
                            
#####################################################################
class DlgList(tkSimpleDialog.Dialog): # не використовується
    '''Клас DlgList. Діалогове вікно зі списком'''
    def __init__(self, parent, title = None,lst=[]):
        self.lst=lst # список
        tkSimpleDialog.Dialog.__init__(self, parent, title)
    def body(self, master): # перевизначений метод tkSimpleDialog.Dialog
        # створити список і смугу прокручування для нього
        self.listbox = Tkinter.Listbox(master,height=25)
        scrollbar_y = Tkinter.Scrollbar(master)
        self.listbox.pack(side=Tkinter.LEFT, fill=Tkinter.Y)
        scrollbar_y.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        scrollbar_y['command'] = self.listbox.yview
        self.listbox['yscrollcommand'] = scrollbar_y.set 
        for x in self.lst: # заповнити список
            self.listbox.insert(Tkinter.END,x)
    def apply(self): # перевизначений метод tkSimpleDialog.Dialog
        self.result=self.listbox.get(self.listbox.curselection()[0]) # результат
#####################################################################
class ClassFile(object):
    '''Описує файл з опціями на початку файлу .pykb
    Приклад файлу:
    #open=1
    #fg=blue
    #bg=white
    ...
    '''
    def __init__(self,path,rowsCount=3):
        self.path=path # шлях
        self.rowsCount=rowsCount # кількість рядків з опціями
    def readLines(self):
        '''Повертає список рядків файлу'''
        f=open(self.path, 'r') # відкрити для читання
        lines=f.readlines() # читати усі рядки
        f.close
        return lines
    def read(self,*opt):
        '''Повертає словник опцій з ключами opt. Приклад:
        d=f.read('open','fg','bg')'''
        res={} # словник опцій
        for line in self.readLines()[0:self.rowsCount]: # для заданої кількості рядків
            pair=line.split('=') # розділити рядок
            key=pair[0][1:] # ключ (усі символи окрім першого #)
            if key in opt: # якщо ключ є у opt
                # добавити в словник
                res[key]=pair[1][0:-1] # без останнього символу '\n' 
        return res
    def write(self,**dic):
        '''Дописує опції у файл. Приклад:
        f.write(open='1',fg='blue',bg='red')'''
        newlines=[] # список нових рядків
        all=self.readLines() # усі рядки
        for line in all[0:self.rowsCount]: # для заданої кількості рядків
            pair=line.split('=') # розділити рядок
            key=pair[0][1:] # ключ (усі символи окрім першого #)
            if key in dic.keys(): # якщо ключ є у dic
                # додати рядок з опцією до списку   
                newlines.append('#'+key+'='+dic[key]+'\n')
            else: # інакше
                newlines.append(line) # додати рядок line
        newlines=newlines+all[self.rowsCount:] # додати до рядків з опціями інші рядки
        f=open(self.path, 'w')
        f.writelines(newlines) # записати усі рядки у файл
        f.close()

import shelve        
class Options(object):
    def __init__(self):
        self.fileName="KBoptions.dat" # файл з опціями
        
    def read(self, key):
        """Читає опції під ключем key"""
        d = shelve.open(self.fileName) 
        if d.has_key(key):
            opts=d[key]
        else:
            opts=[0,'black','white']
        return opts
    
    def write(self, key, opts):
        """Записує опції під ключем key"""
        d = shelve.open(self.fileName) #відкрити файл полиці
        d[key]=opts
        d.close()
        
    def delete(self,key):
        """Видаляє опції під ключем key"""
        d = shelve.open(self.fileName)
        if d.has_key(key):
            del d[key]
        d.close()

                                         
if __name__ == '__main__':
    root=MyApp() # створити головне вікно
    root.mainloop() # головний цикл обробки подій          