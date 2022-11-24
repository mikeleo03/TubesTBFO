# Finite Automata to check the variable name
# JavaScript has only a few rules for variable names:
# 1. The first character must be a letter or an underscore (_). 
# 2. You can't use a number as the first character.
# 3. The rest of the variable name can include any letter, any number, or the underscore. 
# You can't use any other characters, including spaces, symbols, and punctuation marks.
# 4. As with the rest of JavaScript, variable names are case sensitive.
# 5. There's no limit to the length of the variable name.

def checkCharacter(x):
    # Cek secara alfabetik dari A-Z dan a-z
    if ((x >= 'a' and x <= 'z') or (x >= 'A' and x <= 'Z')):
        return True
    else:
        return False

def checkNumber(x):
    # Cek angka 1 digit dari 0 - 9
    if(x >= 0 and x <= 9):
        return True
    else:
        return False

def checkVariable(Var):
    # Validasi nama variabel sesuai rules
    if (not checkCharacter(Var[0]) and not Var[0] == '_' and not Var[0] == '$'):
        return False
    for i in range(len(Var) - 1):
        if not(checkCharacter(Var[i]) or Var[i] == '_' or Var[i] == '$'):
            try :
                not checkNumber(Var[i])
            except:
                return False
        else:
            return True