# -*- coding: CP1251 -*-
import subprocess,os

# шлях до утіліти
utilityPath=os.path.join(os.getcwd(), "junction.exe")

def CreateSymbolicLinks(lst):
    """Створює точки зєднання NTFS (NTFS Junction Points) за допомогою утиліти junction
    http://technet.microsoft.com/en-us/sysinternals
    Для Windows 7 можна стандартною утілітою: mklink /j <посилання> <шлях>
    Інша утілита linkd.exe підтримуює тільки ASCII символи в назві папки.
    Створення точки зєднання для папки: junction.exe <посилання> <шлях>
    lst - список пар шлях-посилання"""
    for x in lst:
        p=subprocess.Popen([utilityPath, x[1], x[0]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # надіслати дані в stdin, отримати дані з stdout, чекати завершення процесу
        stdout, stderr = p.communicate()
        print stdout, stderr
        
def DeleteSymbolicLinks(lst):
    """Видаляє точки зєднання NTFS (NTFS Junction Points) за допомогою утиліти junction
    Видалення точки зєднання: junction.exe -d <посилання>
    lst - список посилань"""
    for x in lst:
        p=subprocess.Popen([utilityPath, "-d", x],stdout= subprocess.PIPE, stderr= subprocess.PIPE)
        # надіслати дані в stdin, отримати дані з stdout, чекати завершення процесу
        stdout, stderr = p.communicate()
        print stdout, stderr

def LinkDestination(path):
    """Повертає шлях до каталогу для посилання path"""
    p=subprocess.Popen([utilityPath, path],stdout= subprocess.PIPE, stderr= subprocess.PIPE)
    # надіслати дані в stdin, отримати дані з stdout, чекати завершення процесу
    stdout, stderr = p.communicate()
    print stdout, stderr
    stdoutList=stdout.splitlines()
    if "No reparse points found."==stdoutList[5]:
        #print "No reparse points found."
        return False
    elif ': JUNCTION' in stdoutList[5]:
        path=stdoutList[6]
        path=path.split("Substitute Name: ")[1] 
        return path
    else:
        #print "No matching files were found."
        return False
    
# Приклад використання:
#d=[["c:\\2", "c:\\xxx"], ["c:\\2", "c:\\xxx2"]]
#CreateSymbolicLinks(d)
#DeleteSymbolicLinks([x[1] for x in d])
#print LinkDestination("c:\\xxx")