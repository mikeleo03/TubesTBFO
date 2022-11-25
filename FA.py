# Finite Automata to check the variable name and operations
# JavaScript has only a few rules for variable names:
# 1. The first character must be a letter or an underscore (_). 
# 2. You can't use a number as the first character.
# 3. The rest of the variable name can include any letter, any number, or the underscore. 
# You can't use any other characters, including spaces, symbols, and punctuation marks.
# 4. As with the rest of JavaScript, variable names are case sensitive.
# 5. There's no limit to the length of the variable name.

import re

def FA(readstring):
    # Inisialization
    countvarerror = 0
    hasil = []
    hasil1 = []
    hasil2 = []
    
    # Defining the DFA States
    hurufkecil =[chr(c) for c in range(97,123)]
    hurufkapital = [chr(c) for c in range(65,91)]
    angka = [chr(c) for c in range(48,58)]
    comment = ['//','/*','*/']
    batas = ['&','?','@','^','~']
    pembanding = ['=','>','<','!']
    aritmetik = ['+','-','/','*','%']
    pembuka = ['{','[','(',',']
    penutup = ['}',']',')']
    dfa = {0:{},1:{},2:{},3:{},4:{},5:{}}

    # State 0
    for x in hurufkecil:
        dfa[0][x] = 2
    for x in hurufkapital:
        dfa[0][x] = 2
    for x in angka:
        dfa[0][x] = 3
    for x in comment:
        dfa[0][x] = 1
    for x in batas:
        dfa[0][x] = 4
    for x in pembanding:
        dfa[0][x] = 0
    for x in pembuka:
        dfa[0][x] = 0
    for x in penutup:
        dfa[0][x] = 0
    for x in aritmetik:
        dfa[0][x] = 0
    dfa[0]['_'] = 2
    dfa[0]['$'] = 2
    dfa[0]['.'] = 0
    dfa[0][':'] = 0
    
    # State 1
    for x in hurufkecil:
        dfa[1][x] = 1
    for x in hurufkapital:
        dfa[1][x] = 1
    for x in angka:
        dfa[1][x] = 1
    for x in comment:
        dfa[1][x] = 0
    for x in batas:
        dfa[1][x] = 1
    for x in pembanding:
        dfa[1][x] = 1
    for x in pembuka:
        dfa[1][x] = 1
    for x in penutup:
        dfa[1][x] = 1
    for x in aritmetik:
        dfa[1][x] = 1
    dfa[1]['_'] = 1
    dfa[1]['$'] = 1
    dfa[1]['.'] = 1
    dfa[1][':'] = 1
    
    # State 2
    for x in hurufkecil :
        dfa[2][x] = 2
    for x in hurufkapital:
        dfa[2][x] = 2
    for x in angka:
        dfa[2][x] = 2
    for x in comment:
        dfa[2][x] = 1
    for x in batas:
        dfa[2][x] = 4
    for x in pembanding:
        dfa[2][x] = 0
    for x in pembuka:
        dfa[2][x] = 0
    for x in penutup:
        dfa[2][x] = 0
    for x in aritmetik:
        dfa[2][x] = 0
    dfa[2]['_'] = 2
    dfa[2]['$'] = 2
    dfa[2]['.'] = 0
    dfa[2][':'] = 0

    # State 3
    for x in hurufkecil :
        dfa[3][x] = 4
    for x in hurufkapital:
        dfa[3][x] = 4
    for x in angka:
        dfa[3][x] = 3
    for x in comment:
        dfa[3][x] = 0
    for x in batas:
        dfa[3][x] = 4
    for x in pembanding:
        dfa[3][x] = 0
    for x in pembuka:
        dfa[3][x] = 4
    for x in penutup:
        dfa[3][x] = 0
    for x in aritmetik:
        dfa[3][x] = 0
    dfa[3]['_'] = 4
    dfa[3]['$'] = 4
    dfa[3]['.'] = 5
    dfa[3][':'] = 0
    
    # State 5
    for x in hurufkecil :
        dfa[5][x] = 4
    for x in hurufkapital:
        dfa[5][x] = 4
    for x in angka:
        dfa[5][x] = 5
    for x in comment:
        dfa[5][x] = 0
    for x in batas:
        dfa[5][x] = 4
    for x in pembanding:
        dfa[5][x] = 0
    for x in pembuka:
        dfa[5][x] = 4
    for x in penutup:
        dfa[5][x] = 4
    for x in aritmetik:
        dfa[5][x] = 0
    dfa[5]['_'] = 4
    dfa[5]['$'] = 4
    dfa[5]['.'] = 5
    dfa[5][':'] = 0

    # Defining how a combination accepted
    def accepts(transition, start, s):
        states = start
        for char in s:
            try:
                states = transition[states][char]
            except KeyError:
                return False
        return (states != 4)

    for i in readstring:
        thisstring = re.sub('&&','=',i)
        hasil.append(thisstring)
    for j in hasil:
        thisstring1 = re.sub('\|\|','=',j)
        hasil1.append(thisstring1)
    for k in hasil1:
        thisstring2 = re.sub('\s+','',k)
        hasil2.append(thisstring2)
    for l in range(len(hasil2)):
        if (accepts(dfa,0,hasil2[l])):
            consider = 'Accepted'
        else:
            consider = 'Rejected'
            countvarerror += 1
            print(hasil[l], consider)
            
    return consider, hasil, hasil1, hasil2

""" consider = FA('3 + 2 = 5')
print(f"Hasil : {consider}") """