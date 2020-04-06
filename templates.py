# -*- coding: CP1251 -*-
# Шаблони коду: {obj},{pred},{subj}
tempdic={
'HeaderClass': # заголовок класу
'''#open=1
#fg=purple
#bg=white
''',

'HeaderObject': # заголовок об'єкту
'''#open=1
#fg=blue
#bg=white
''',

'HeaderProperty': # заголовок властивості
'''#open=0
#fg=red
#bg=white
''',

'HeaderPost': # заголовок правил виведення
'''#open=1
#fg=darkgreen
#bg=white
''',

'HeaderQuery': # заголовок запитів
'''#open=1
#fg=brown
#bg=white
''',

'LinkQuoted': # посилання в лапках
'''
r"""{obj}"""
''',

'Link': # посилання
'''
{obj}
''', 
          
'Class': # клас
'''
class X(KB[r"""{subj}"""]):
    def __init__(self):
        KB[r"""{subj}"""].__init__(self)

KB[r"""{obj}"""]=X; del X
''',

'Object': # об'єкт
'''
KB[r"""{obj}"""]=KB[r"""{subj}"""]()
''',

'ObjectFactor': # фактор
'''#open=1
#fg=blue
#bg=white

KB[r"""{obj}"""]=KB[r"""Base\Фактор"""]()
''',

'ObjectFact': # факт
'''
KB[r"""{obj}"""]=KB[r"""Base\Факт"""]()
''',

'PropertyAddValue': # додати властивість об'єкту
'''
KB[r"""{obj}"""].__dict__["{pred}"].add(KB[r"""{subj}"""])
''',

'FactCreate': # задати властивості факту
'''
X.create(
r"""{obj}""",
'{pred}',
r"""{subj}"""
)
''',

'tempObj': # тимчасовий об'єкт X
'''
X=KB[r"""{obj}"""]
''',

'Query': # простий запит
'''
for k,v in KB.iteritems():
    print k
''',

'RGBcolor':'#00F' # колір RGB
}

if __name__=='__main__':
    print tempdic