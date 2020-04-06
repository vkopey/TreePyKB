# -*- coding: CP1251 -*-
import subprocess,os

# ���� �� �����
utilityPath=os.path.join(os.getcwd(), "junction.exe")

def CreateSymbolicLinks(lst):
    """������� ����� ������� NTFS (NTFS Junction Points) �� ��������� ������ junction
    http://technet.microsoft.com/en-us/sysinternals
    ��� Windows 7 ����� ����������� ������: mklink /j <���������> <����>
    ���� ������ linkd.exe ��������� ����� ASCII ������� � ���� �����.
    ��������� ����� ������� ��� �����: junction.exe <���������> <����>
    lst - ������ ��� ����-���������"""
    for x in lst:
        p=subprocess.Popen([utilityPath, x[1], x[0]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # �������� ��� � stdin, �������� ��� � stdout, ������ ���������� �������
        stdout, stderr = p.communicate()
        print stdout, stderr
        
def DeleteSymbolicLinks(lst):
    """������� ����� ������� NTFS (NTFS Junction Points) �� ��������� ������ junction
    ��������� ����� �������: junction.exe -d <���������>
    lst - ������ ��������"""
    for x in lst:
        p=subprocess.Popen([utilityPath, "-d", x],stdout= subprocess.PIPE, stderr= subprocess.PIPE)
        # �������� ��� � stdin, �������� ��� � stdout, ������ ���������� �������
        stdout, stderr = p.communicate()
        print stdout, stderr

def LinkDestination(path):
    """������� ���� �� �������� ��� ��������� path"""
    p=subprocess.Popen([utilityPath, path],stdout= subprocess.PIPE, stderr= subprocess.PIPE)
    # �������� ��� � stdin, �������� ��� � stdout, ������ ���������� �������
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
    
# ������� ������������:
#d=[["c:\\2", "c:\\xxx"], ["c:\\2", "c:\\xxx2"]]
#CreateSymbolicLinks(d)
#DeleteSymbolicLinks([x[1] for x in d])
#print LinkDestination("c:\\xxx")