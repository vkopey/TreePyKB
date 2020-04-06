# -*- coding: CP1251 -*-
# ������� ����: {obj},{pred},{subj}
tempdic={
'HeaderClass': # ��������� �����
'''#open=1
#fg=purple
#bg=white
''',

'HeaderObject': # ��������� ��'����
'''#open=1
#fg=blue
#bg=white
''',

'HeaderProperty': # ��������� ����������
'''#open=0
#fg=red
#bg=white
''',

'HeaderPost': # ��������� ������ ���������
'''#open=1
#fg=darkgreen
#bg=white
''',

'HeaderQuery': # ��������� ������
'''#open=1
#fg=brown
#bg=white
''',

'LinkQuoted': # ��������� � ������
'''
r"""{obj}"""
''',

'Link': # ���������
'''
{obj}
''', 
          
'Class': # ����
'''
class X(KB[r"""{subj}"""]):
    def __init__(self):
        KB[r"""{subj}"""].__init__(self)

KB[r"""{obj}"""]=X; del X
''',

'Object': # ��'���
'''
KB[r"""{obj}"""]=KB[r"""{subj}"""]()
''',

'ObjectFactor': # ������
'''#open=1
#fg=blue
#bg=white

KB[r"""{obj}"""]=KB[r"""Base\������"""]()
''',

'ObjectFact': # ����
'''
KB[r"""{obj}"""]=KB[r"""Base\����"""]()
''',

'PropertyAddValue': # ������ ���������� ��'����
'''
KB[r"""{obj}"""].__dict__["{pred}"].add(KB[r"""{subj}"""])
''',

'FactCreate': # ������ ���������� �����
'''
X.create(
r"""{obj}""",
'{pred}',
r"""{subj}"""
)
''',

'tempObj': # ���������� ��'��� X
'''
X=KB[r"""{obj}"""]
''',

'Query': # ������� �����
'''
for k,v in KB.iteritems():
    print k
''',

'RGBcolor':'#00F' # ���� RGB
}

if __name__=='__main__':
    print tempdic