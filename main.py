# Main program 
# The main program and all syntax checking problems, calling exteernal functions

from os.path import isfile as isExist
import LexerGrammar
import CYK

isAccepted = True
isBlockComment = False
isSkipUntilNextBC = False
isFuction = False
isCase = False
breakgagal = False
continuegagal = False
returngagal = False
isIfLevel = []
level = 0

print('JAVASCRIPT PARSER (hampi rilis version)')
print('[udah keren yey dikit lagi]\n')

inputfile = input('Insert file name (.js): ')
if isExist(inputfile):
    lex = LexerGrammar.Lexer(LexerGrammar.rules, skip_whitespace=True)
    cyk = CYK.Parser('cnf2.txt')
    file = open(inputfile, "r", encoding="utf8")
    lineArr = []
    
    # Mencetak hasil bacaan file ke layar
    print("==================================================\n")
    for line in file:
        if line != "\n" or line != "":
            lineArr.append([line, len(line) - len(line.lstrip())])
            print(line, end = "")
    file.close()
    print("\n==================================================")
    
    # Pengecekan error, parsing files
    with open(inputfile, 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        lexered = ''
        lex.input(line)
        try:
            for tok in lex.tokens():
                lexered += f'{tok!r}'
        except LexerGrammar.LexerError as err:
            print(f'LexerError at position {err.pos}')

        """ if "BBCOMMENT" in lexered:
            lexered = lexered.replace("BBCOMMENT ","")
        if "BCOMMENT" in lexered:
            if not isSkipUntilNextBC:
                isBlockComment = True
                posBC = lexered.find("BCOMMENT")
                if posBC == 0:
                    lexered = ''
                else:
                    lexered = lexered[:posBC:]
            else:
                isSkipUntilNextBC = False
                posBC = lexered.find("BCOMMENT")
                lexered = lexered[posBC+9::]

        if isSkipUntilNextBC:
            continue
        if "COMMENT" in lexered:
            lexered = lexered.replace("COMMENT ","")
        """
        if "FUNCTION" in lexered:
            isFuction = True
            
        if "CASE" in lexered:
            isCase = True
            
        if "BREAK" in lexered:
            if (not isFuction and not isCase):
                isAccepted = False
                breakgagal = True
                break
            elif (not isCase):
                isAccepted = False
                breakgagal = True
                break
            elif (isCase and isIfLevel == []) :
                isAccepted = False
                breakgagal = False
                isCase = False
                break
            else :
                isAccepted = True
                breakgagal = False
                isCase = False
        
        if (not isFuction and not isCase) :
            if "CONTINUE" in lexered:
                isAccepted = False
                continuegagal = True
                break
            if "RETURN" in lexered:
                isAccepted = False
                returngagal = True
                break
        
        if "CURFEW_CLOSE" in lexered:
            if level not in isIfLevel:
                isAccepted = False
                break
            elif "CURFEW_CLOSE" in lexered:
                isIfLevel.remove(level)
                level-=1
        if "CURFEW_OPEN" in lexered:
            level+=1
            isIfLevel.append(level)
            
        # print(isIfLevel, isCase)

        cyk(lexered,parse=True)
        isAccepted = cyk.print_tree(output=False)
        # print(isIfLevel)
        if not isAccepted:
            break
        if isBlockComment:
            isSkipUntilNextBC = True
            isBlockComment = False
            
    print("\nResult:", end = " ")
    if isAccepted and isIfLevel == []:
        print('\033[92m' + "Accepted")
    else:
        print('\033[93m' + f"\nSyntax Error at line {i+1}:")
        print('\033[93m' + f"   >> {line.strip()}\n")
        if breakgagal:
            print('\033[93m' + f"Tidak dapat menambahkan break di luar function\n")
        if continuegagal:
            print('\033[93m' + f"Tidak dapat menambahkan continue di luar function\n")
        if returngagal:
            print('\033[93m' + f"Tidak dapat menambahkan return di luar function\n")
        print(f"Readed: {lexered}")
    print('\033[0m')
    
else:
    print("There's no such file in directory!")