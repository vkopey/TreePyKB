# -*- coding: CP1251 -*-
"""
Makes Python code of expert system from directory tree.
Run this module from the root directory of the knowledge base or run as:
makecode.py <root directory of the knowledge base>
Example:
makecode.py c:\MyKB
You can create button on the Total Commander tool bar.
Drag module to the Total Commander tool bar and enter parameter %P.
Open root directory of the knowledge base in Total Commander and press button.
Python code will be created in this directory.
Runs on Windows XP and Windows CE (PythonCE 2.5)
    
Kopey Vladimir, 2012
vkopey@gmail.com    
    
This software is distibuted under the Gnu-GPL. Please Visit
http://www.gnu.org/licenses/gpl.txt to see the license."""
import os,sys,re,subprocess

def relpath(path):
    '''os.path.relpath() для Pyhon 2.5'''
    if sys.version_info[1]>5: # для Python 2.6 використовувати os.path.relpath
        return os.path.relpath(path)
    return path[len(os.getcwdu())+1:] # для Python 2.5

def makeCode(dir,programDir=None):
    '''Формує і повертає виконуваний Python код
    dir - шлях до KB
    programDir - шлях до редактора KB'''
    # якщо не задано шлях до редактора KB, то цей модуль працює незалежно
    if programDir==None: programDir=dir
    def mkCode(dir):
        '''Формує виконуваний Python код. Рекурсивна.
        Увага! Не зчитує кореневий файл class.pykb'''
        for fl in os.listdir(dir): # для усіх файлів в каталозі
            path = os.path.join(dir, fl) # повний шлях
            basename=os.path.basename(path) # ім'я каталога/файлу
            rpath=relpath(path) # відносний шлях (для Python 2.5)
            #rpath=os.path.relpath(path) # відносний шлях (для Python 2.6)
            classfile=os.path.join(path, 'class.pykb') # файл класу
            # якщо каталог і є файл класу
            if os.path.isdir(path) and os.path.isfile(classfile):
                f=open(classfile, 'r') # відкрити файл класу
                f.readline() # пропустити перший рядок
                try:
                    color=f.readline().split('=')[1][0:-1] # колір з другого рядка
                except:
                    color='black'
                f.seek(0) # переміститись на початок файла
                if color in itemsPriorityList: #якщо колір є у itemsPriorityList
                    index=itemsPriorityList.index(color) # індекс color у itemsPriorityList
                    s[index]+='#path='+relpath(classfile)+'\n' # добавити рядок з шляхом
                    s[index]+=f.read().decode('cp1251')+'\n' # добавити у рядок s[індекс пріорітету]
                    print index.__str__()+rpath.encode('cp1251')
                else: # інакше вивести попередження
                    print 'Item '+rpath.encode('cp1251')+' fg color not in the itemsPriorityList'
                f.close()                                        
                mkCode(path) #рекурсія
            # інакше якщо файл .pykb (окрім class.pykb)    
            elif os.path.splitext(path)[1]=='.pykb' and basename!='class.pykb':
                f=open(path, 'r') # відкрити файл
                f.readline() # пропустити перший рядок
                try:
                    color=f.readline().split('=')[1][0:-1] # колір з другого рядка
                except:
                    color='black'
                f.seek(0) # переміститись на початок файла
                if color in itemsPriorityList: #якщо колір є у itemsPriorityList
                    index=itemsPriorityList.index(color) # індекс color у itemsPriorityList
                    #!!! у внутрішній функції можна міняти лише вміст елементів s
                    s[index]+='#path='+relpath(path)+'\n'
                    s[index]+=f.read().decode('cp1251')+'\n' # добавити у рядок s[індекс пріорітету]
                    print index.__str__()+rpath.encode('cp1251')
                else: # інакше вивести попередження
                    print 'Item '+rpath.encode('cp1251')+' fg color not in the itemsPriorityList'
                f.close()           
    itemsPriorityList=['black'] # список за замовчуванням з порядком формування коду
    if os.path.isfile('itemsPriority.txt'): # якщо в кореневому каталозі є такий файл
        itemsPriorityList=eval(open('itemsPriority.txt').read().strip()) # отримати список з файлу
    else: # інакше
        # вивести попередження про відсутність
        print 'Warning! Default itemsPriorityList'
    s=['']*len(itemsPriorityList) # список частин коду
    mkCode(dir) # формувати впорядкований список частин коду
    code='' # код у вигляді рядка
    for x in s:
        if x: code=code+x.encode('cp1251')+'\n' # формувати код у вигляді рядка
    rootClass=open('class.pykb','r').read() # прочитати кореневий файл класу
    impMakeCode="""
import sys
if programDir not in sys.path: sys.path.append(programDir)
import MakeCode
"""
    code='#path=class.pykb\n'+rootClass+'\n'+'programDir="'+programDir+'"\n'+impMakeCode+code # добавити до рядка
    # та вшити в код змінну programDir=<шлях до редактора KB>
    return code

def genHTML(path, dic=None):
    """Генерує HTML з тексту вихідного коду
    path - відносний шлях до файлу вихідного коду .pykb
    dic - словник зі значеннями змінних в шаблонах
    приклад використання:
    dic={
    u'рисунок1':u'<img src="рисунок1.jpg" alt="рисунок1" width="600">',
    u'рисунок2':u'<img src="рисунок1.jpg">'}
    genHTML(r'Base\Модель\class.pykb',dic)"""
    from pygments import highlight # повертає відформатований текст
    from pygments.lexers import PythonLexer # лексичний аналізатор Python
    from pygments.formatters import HtmlFormatter # для форматування у вигляді HTML
    # для отримання файлу стилів python.css
    #highlight('', PythonLexer(), HtmlFormatter(full=True,cssfile='python.css'))
    f=open(path, 'r')
    lines=f.readlines() # прочитати усі рядки у список
    f.close()
    n=len(path.split('\\'))-1 # глибина файла відносно базового каталога
    # '../'*n - кількість повернень до базового каталога в посиланні
    allHTML=u"""
<!DOCTYPE html>
<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
<title>Untitled 1</title>
<style type="text/css">
@import url('{deep}python.css');
</style>
</head>
<body>
"""[1:].format(deep=u'../'*n) # рядок усього HTML (початок документу)
    TMPlines=[] # тимчасовий список рядків
    isHTML=False # чи ми знаходимось в блоці HTML ?
    prevLine=u'' # попередній рядок
    i=0 # лічильник рядків
    for line in lines: # для усіх рядків
        line=line.decode('cp1251') # конвертувати рядок в Юнікод
        TMPlines.append(line) # добавити в тимчасовий список
        i+=1 # збільшити лічильник на 1
        # якщо розпочався блок HTML
        if line==u'#html\n':
            isHTML=True # ми знаходимось в блоці HTML
            # генерувати HTML з підсвічуванням коду
            HTMLpython=highlight(u''.join(TMPlines[:-1]), PythonLexer(), HtmlFormatter())
            TMPlines=[] # очистити тимчасовий список рядків
            allHTML+=HTMLpython # добавити в рядок усього HTML
        # якщо закінчився блок HTML або він останній та закінчився символами """
        if (line==u'"""\n' and isHTML==True and prevLine!=u'#html\n') or (line==u'"""' and isHTML==True and prevLine!=u'#html\n' and i==len(lines)):
            isHTML=False # ми знаходимось не в блоці HTML 
            HTML=u''.join(TMPlines[1:-1]) # об'єднати рядки в HTML
            TMPlines=[] # очистити тимчасовий список рядків
            allHTML+=HTML # добавити в рядок усього HTML
        if i==len(lines) and TMPlines: # якщо це останій рядок і є рядки у тимчасовому списку
            HTMLpython=highlight(u''.join(TMPlines), PythonLexer(), HtmlFormatter())
            allHTML+=HTMLpython
        prevLine=line # запам'ятати попередній рядок
    allHTML+=u'</body></html>'
    
    # добавити гіперпосилання за допомогою re
    pattern=r'&quot;&quot;&quot;(.*?)&quot;&quot;&quot;' # що заміняти
    repl=r'<a href="'+'../'*n+r'\g<1>\\class.pykb">&quot;&quot;&quot;\g<1>&quot;&quot;&quot;</a>' # чим заміняти
    allHTML=re.sub(pattern,repl,allHTML) # замінити все
    
    allHTML=latex2mathmlAll(allHTML) # замінити всі формули LaTeX на MathML
    
    # тут можна добавити оброблення шаблонів (jinja2, mako ...)
    # наприклад, оброблення простих шаблонів:
    import string
    strTemplate=string.Template(allHTML)
    if dic!=None:
        allHTML=strTemplate.safe_substitute(**dic)
    
    HTMLpath=os.path.splitext(path)[0]+'.html' # шлях до HTML
    open(HTMLpath,'w').write(allHTML.encode('utf-8')) # зберегти HTML (кодування 'utf-8')
    return HTMLpath # повертає відносний шлях до HTML

def latex2mathml(latex):
    """Повертає рядок MathML за рядком LaTeX
    Повинен бути установлений в c:\\TtMdir\\ttm.exe
    TtM, a TeX to MathML translator http://hutchinson.belmont.ma.us/tth/mml/
    """
    texf=open(r"c:\TtMdir\temporary.tex",'w') # створити LaTeX файл
    texf.write(latex)
    texf.close()
    subprocess.call([r"c:\TtMdir\ttm.exe", "-L", "-r", r"c:\TtMdir\temporary.tex"]) # перетворити в MathML
    xmlf=open(r"c:\TtMdir\temporary.xml",'r') # відкрити MathML
    s=xmlf.read() # прочитати MathML
    xmlf.close()
    match = re.search(r"<math[^>]*>(.*?)</math>", s, re.DOTALL) # знайти в ньому безпосередньо MathML
    if match: # якщо є
        s=match.group(0) # s=MathML
    else: # інакше
        s=latex # s=LaTeX
    return s

def latex2mathmlAll(s):
    r"""Конвертує весь Юнікод html документ з LaTeX формулами в Юнікод html документ з MathML формулами
    s - Юнікод html документ (сумісний з cp1251) з LaTeX формулами у вигляді {\[формула\]}"""
    def repl(mo): # функція для заміни
        return latex2mathml(mo.group(0)[1:-1]) # конвертує одну формулу без символів {}
    s=s.encode('cp1251') # конвертувати в cp1251
    # замінити все і конвертувати в Юнікод    
    return re.sub(r"{\\\[(.*?)\\\]}", repl, s).decode('cp1251')

if __name__ == '__main__':
    if len(sys.argv)>1: # якщо передані аргументи через командний рядок
        os.chdir(sys.argv[1]) # задати робочий каталог - перший аргумент командного рядка
    if os.path.exists('generatedKBcode.py'): # якщо такий файл вже є
        print 'Path code.py already exists!'
        sys.exit() # вийти
    code=makeCode(os.getcwdu()) # формувати код для робочого каталогу
    f=open('generatedKBcode.py','w') # відкрити файл для запису
    f.write(code) # зберегти
    f.close()
