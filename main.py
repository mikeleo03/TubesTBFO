# Main program 
# The main program and all syntax checking problems, calling exteernal functions

from os.path import isfile as isExist
import LexerGrammar
import CYK

isAccepted = True
isBlockComment = False
isFunc = False
isLoop = False
isIf = False
isCase = False
ifgagal = False
breakgagal = False
continuegagal = False
returngagalloop = False
returngagalfunc = False
curfew = []
levelif = []
levelcase = []
levelfunc = []
levelloop = []
level = 0

print('JAVASCRIPT PARSER (hampi rilis version)')
print('[udah keren yey dikit lagi]\n')

inputfile = input('Insert file name (.js): ')
if isExist(inputfile):
    lex = LexerGrammar.Lexer(LexerGrammar.rules, skip_whitespace=True)
    cyk = CYK.Parser('cnf.txt')
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

        if "SINGLE_LINE_COMMENT" in lexered:
            lexered = lexered.replace(lexered,"")
            isBlockComment = True
        """
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
        """
        
        if "WHILE" in lexered:
            isLoop = True
            levelloop.append(level+1)
            
        if "FOR" in lexered:
            isLoop = True
            levelloop.append(level+1)
            
        if "IF" in lexered:
            isIf = True
            levelif.append(level+1)
            
        if "ELSE" in lexered:
            if (not isIf):
                ifgagal = True
                break
            
        if "CASE" in lexered:
            isCase = True
            levelcase.append(level+1)
            
        if "FUNCTION" in lexered:
            isFunc = True
            levelfunc.append(level+1)
            
        if "BREAK" in lexered:
            if (len(levelloop) == 0 and len(levelcase) == 0):
                isAccepted = False
                breakgagal = True
                break
            elif (len(levelloop) != 0):
                isAccepted = True
                breakgagal = False
                
        if "CONTINUE" in lexered:
            if (len(levelloop) == 0):
                isAccepted = False
                continuegagal = True
                break
            else :
                isAccepted = True
                continuegagal = False
        
        if "RETURN" in lexered:
            if (len(levelfunc) == 0 and len(levelloop) == 0):
                isAccepted = False
                returngagalloop = True
                returngagalfunc = True
                break
            elif (len(levelfunc) == 0 and len(levelloop) != 0):
                isAccepted = True
                returngagalfunc = True
                isLoop = False
            elif (len(levelloop) == 0 and len(levelfunc) != 0):
                isAccepted = True
                returngagalloop = True
                isFunc = False
            else :
                isAccepted = True
                returngagalfunc = False
                returngagalloop = False
        
        if "CURFEW_CLOSE" in lexered:
            if level not in curfew:
                isAccepted = False
                break
            elif "CURFEW_CLOSE" in lexered:
                curfew.remove(level)
                if level in levelif:
                    levelif.remove(level)
                if level in levelfunc:
                    levelfunc.remove(level)
                if level in levelloop:
                    levelloop.remove(level)
                level-=1
        if "CURFEW_OPEN" in lexered:
            level+=1
            curfew.append(level)

        # print(lexered)
        cyk(lexered,parse=True)
        isAccepted = cyk.print_tree(output=False)
        if not isAccepted:
            break
        if isBlockComment:
            isSkipUntilNextBC = True
            isBlockComment = False
    
        # print(isFunc,isLoop,returngagalfunc,returngagalloop)
        print("terbaca",curfew)
        print("lexered",levelif,levelfunc,levelloop)
        print("\n")
    print("\nResult:", end = " ")
    if isAccepted and curfew == []:
        print('\033[92m' + "Accepted")
    else:
        print('\033[93m' + f"\nSyntax Error at line {i+1}:")
        print('\033[93m' + f"   >> {line.strip()}\n")
        if breakgagal:
            print('\033[93m' + f"Tidak dapat menambahkan break di luar loop\n")
        if continuegagal:
            print('\033[93m' + f"Tidak dapat menambahkan continue di luar loop\n")
        if returngagalloop and returngagalfunc:
            print('\033[93m' + f"Tidak dapat menambahkan return di luar loop dan function\n")
        elif returngagalloop:
            print('\033[93m' + f"Tidak dapat menambahkan return di luar loop\n")
        elif returngagalfunc:
            print('\033[93m' + f"Tidak dapat menambahkan return di luar function\n")
        if ifgagal:
            print('\033[93m' + f"Tidak dapat menambahkan else sebelum ada if\n")
        print(f"Readed: {lexered}")
    print('\033[0m')
    
else:
    print("There's no such file in directory!")