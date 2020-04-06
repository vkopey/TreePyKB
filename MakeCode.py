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
    '''os.path.relpath() ��� Pyhon 2.5'''
    if sys.version_info[1]>5: # ��� Python 2.6 ��������������� os.path.relpath
        return os.path.relpath(path)
    return path[len(os.getcwdu())+1:] # ��� Python 2.5

def makeCode(dir,programDir=None):
    '''����� � ������� ����������� Python ���
    dir - ���� �� KB
    programDir - ���� �� ��������� KB'''
    # ���� �� ������ ���� �� ��������� KB, �� ��� ������ ������ ���������
    if programDir==None: programDir=dir
    def mkCode(dir):
        '''����� ����������� Python ���. ����������.
        �����! �� ����� ��������� ���� class.pykb'''
        for fl in os.listdir(dir): # ��� ��� ����� � �������
            path = os.path.join(dir, fl) # ������ ����
            basename=os.path.basename(path) # ��'� ��������/�����
            rpath=relpath(path) # �������� ���� (��� Python 2.5)
            #rpath=os.path.relpath(path) # �������� ���� (��� Python 2.6)
            classfile=os.path.join(path, 'class.pykb') # ���� �����
            # ���� ������� � � ���� �����
            if os.path.isdir(path) and os.path.isfile(classfile):
                f=open(classfile, 'r') # ������� ���� �����
                f.readline() # ���������� ������ �����
                try:
                    color=f.readline().split('=')[1][0:-1] # ���� � ������� �����
                except:
                    color='black'
                f.seek(0) # ������������ �� ������� �����
                if color in itemsPriorityList: #���� ���� � � itemsPriorityList
                    index=itemsPriorityList.index(color) # ������ color � itemsPriorityList
                    s[index]+='#path='+relpath(classfile)+'\n' # �������� ����� � ������
                    s[index]+=f.read().decode('cp1251')+'\n' # �������� � ����� s[������ ��������]
                    print index.__str__()+rpath.encode('cp1251')
                else: # ������ ������� ������������
                    print 'Item '+rpath.encode('cp1251')+' fg color not in the itemsPriorityList'
                f.close()                                        
                mkCode(path) #�������
            # ������ ���� ���� .pykb (���� class.pykb)    
            elif os.path.splitext(path)[1]=='.pykb' and basename!='class.pykb':
                f=open(path, 'r') # ������� ����
                f.readline() # ���������� ������ �����
                try:
                    color=f.readline().split('=')[1][0:-1] # ���� � ������� �����
                except:
                    color='black'
                f.seek(0) # ������������ �� ������� �����
                if color in itemsPriorityList: #���� ���� � � itemsPriorityList
                    index=itemsPriorityList.index(color) # ������ color � itemsPriorityList
                    #!!! � �������� ������� ����� ����� ���� ���� �������� s
                    s[index]+='#path='+relpath(path)+'\n'
                    s[index]+=f.read().decode('cp1251')+'\n' # �������� � ����� s[������ ��������]
                    print index.__str__()+rpath.encode('cp1251')
                else: # ������ ������� ������������
                    print 'Item '+rpath.encode('cp1251')+' fg color not in the itemsPriorityList'
                f.close()           
    itemsPriorityList=['black'] # ������ �� ������������� � �������� ���������� ����
    if os.path.isfile('itemsPriority.txt'): # ���� � ���������� ������� � ����� ����
        itemsPriorityList=eval(open('itemsPriority.txt').read().strip()) # �������� ������ � �����
    else: # ������
        # ������� ������������ ��� ���������
        print 'Warning! Default itemsPriorityList'
    s=['']*len(itemsPriorityList) # ������ ������ ����
    mkCode(dir) # ��������� ������������� ������ ������ ����
    code='' # ��� � ������ �����
    for x in s:
        if x: code=code+x.encode('cp1251')+'\n' # ��������� ��� � ������ �����
    rootClass=open('class.pykb','r').read() # ��������� ��������� ���� �����
    impMakeCode="""
import sys
if programDir not in sys.path: sys.path.append(programDir)
import MakeCode
"""
    code='#path=class.pykb\n'+rootClass+'\n'+'programDir="'+programDir+'"\n'+impMakeCode+code # �������� �� �����
    # �� ����� � ��� ����� programDir=<���� �� ��������� KB>
    return code

def genHTML(path, dic=None):
    """������ HTML � ������ ��������� ����
    path - �������� ���� �� ����� ��������� ���� .pykb
    dic - ������� � ���������� ������ � ��������
    ������� ������������:
    dic={
    u'�������1':u'<img src="�������1.jpg" alt="�������1" width="600">',
    u'�������2':u'<img src="�������1.jpg">'}
    genHTML(r'Base\������\class.pykb',dic)"""
    from pygments import highlight # ������� �������������� �����
    from pygments.lexers import PythonLexer # ��������� ��������� Python
    from pygments.formatters import HtmlFormatter # ��� ������������ � ������ HTML
    # ��� ��������� ����� ����� python.css
    #highlight('', PythonLexer(), HtmlFormatter(full=True,cssfile='python.css'))
    f=open(path, 'r')
    lines=f.readlines() # ��������� �� ����� � ������
    f.close()
    n=len(path.split('\\'))-1 # ������� ����� ������� �������� ��������
    # '../'*n - ������� ��������� �� �������� �������� � ��������
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
"""[1:].format(deep=u'../'*n) # ����� ������ HTML (������� ���������)
    TMPlines=[] # ���������� ������ �����
    isHTML=False # �� �� ����������� � ����� HTML ?
    prevLine=u'' # ��������� �����
    i=0 # �������� �����
    for line in lines: # ��� ��� �����
        line=line.decode('cp1251') # ������������ ����� � �����
        TMPlines.append(line) # �������� � ���������� ������
        i+=1 # �������� �������� �� 1
        # ���� ���������� ���� HTML
        if line==u'#html\n':
            isHTML=True # �� ����������� � ����� HTML
            # ���������� HTML � ������������ ����
            HTMLpython=highlight(u''.join(TMPlines[:-1]), PythonLexer(), HtmlFormatter())
            TMPlines=[] # �������� ���������� ������ �����
            allHTML+=HTMLpython # �������� � ����� ������ HTML
        # ���� ��������� ���� HTML ��� �� ������� �� ��������� ��������� """
        if (line==u'"""\n' and isHTML==True and prevLine!=u'#html\n') or (line==u'"""' and isHTML==True and prevLine!=u'#html\n' and i==len(lines)):
            isHTML=False # �� ����������� �� � ����� HTML 
            HTML=u''.join(TMPlines[1:-1]) # ��'������ ����� � HTML
            TMPlines=[] # �������� ���������� ������ �����
            allHTML+=HTML # �������� � ����� ������ HTML
        if i==len(lines) and TMPlines: # ���� �� ������ ����� � � ����� � ����������� ������
            HTMLpython=highlight(u''.join(TMPlines), PythonLexer(), HtmlFormatter())
            allHTML+=HTMLpython
        prevLine=line # �����'����� ��������� �����
    allHTML+=u'</body></html>'
    
    # �������� ������������� �� ��������� re
    pattern=r'&quot;&quot;&quot;(.*?)&quot;&quot;&quot;' # �� �������
    repl=r'<a href="'+'../'*n+r'\g<1>\\class.pykb">&quot;&quot;&quot;\g<1>&quot;&quot;&quot;</a>' # ��� �������
    allHTML=re.sub(pattern,repl,allHTML) # ������� ���
    
    allHTML=latex2mathmlAll(allHTML) # ������� �� ������� LaTeX �� MathML
    
    # ��� ����� �������� ���������� ������� (jinja2, mako ...)
    # ���������, ���������� ������� �������:
    import string
    strTemplate=string.Template(allHTML)
    if dic!=None:
        allHTML=strTemplate.safe_substitute(**dic)
    
    HTMLpath=os.path.splitext(path)[0]+'.html' # ���� �� HTML
    open(HTMLpath,'w').write(allHTML.encode('utf-8')) # �������� HTML (��������� 'utf-8')
    return HTMLpath # ������� �������� ���� �� HTML

def latex2mathml(latex):
    """������� ����� MathML �� ������ LaTeX
    ������� ���� ������������ � c:\\TtMdir\\ttm.exe
    TtM, a TeX to MathML translator http://hutchinson.belmont.ma.us/tth/mml/
    """
    texf=open(r"c:\TtMdir\temporary.tex",'w') # �������� LaTeX ����
    texf.write(latex)
    texf.close()
    subprocess.call([r"c:\TtMdir\ttm.exe", "-L", "-r", r"c:\TtMdir\temporary.tex"]) # ����������� � MathML
    xmlf=open(r"c:\TtMdir\temporary.xml",'r') # ������� MathML
    s=xmlf.read() # ��������� MathML
    xmlf.close()
    match = re.search(r"<math[^>]*>(.*?)</math>", s, re.DOTALL) # ������ � ����� ������������� MathML
    if match: # ���� �
        s=match.group(0) # s=MathML
    else: # ������
        s=latex # s=LaTeX
    return s

def latex2mathmlAll(s):
    r"""�������� ���� ����� html �������� � LaTeX ��������� � ����� html �������� � MathML ���������
    s - ����� html �������� (������� � cp1251) � LaTeX ��������� � ������ {\[�������\]}"""
    def repl(mo): # ������� ��� �����
        return latex2mathml(mo.group(0)[1:-1]) # �������� ���� ������� ��� ������� {}
    s=s.encode('cp1251') # ������������ � cp1251
    # ������� ��� � ������������ � �����    
    return re.sub(r"{\\\[(.*?)\\\]}", repl, s).decode('cp1251')

if __name__ == '__main__':
    if len(sys.argv)>1: # ���� ������� ��������� ����� ��������� �����
        os.chdir(sys.argv[1]) # ������ ������� ������� - ������ �������� ���������� �����
    if os.path.exists('generatedKBcode.py'): # ���� ����� ���� ��� �
        print 'Path code.py already exists!'
        sys.exit() # �����
    code=makeCode(os.getcwdu()) # ��������� ��� ��� �������� ��������
    f=open('generatedKBcode.py','w') # ������� ���� ��� ������
    f.write(code) # ��������
    f.close()
