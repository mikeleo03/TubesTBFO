# Main program 
# The main program and all syntax checking problems, calling exteernal functions

from os.path import isfile as isExist
import time
import LexerGrammar
import CYK
import FA

isAccepted = True
isBlockComment = False
isFunc = False
isLoop = False
isForLoop = False
isIf = False
isTry = False
isCatch = False
isSwitch = False
isCase = False
isString = False
ifgagal = False
breakgagal = False
switchgagal = False
continuegagal = False
returngagalloop = False
returngagalfunc = False
eos = False
startString = ''
curfew = []
levelif = []
levelcase = []
levelfunc = []
levelloop = []
level = 0

print('''
    $$$$$\          === TUGAS BESAR TBFO IF2124 ===           $$\          $$\     
   \__$$ |                                                    \__|         $$ |    
      $$ |$$$$$$\$$\    $$\$$$$$$\  $$$$$$$\ $$$$$$$\ $$$$$$\ $$\ $$$$$$\$$$$$$\   
      $$ |\____$$\$$\  $$  \____$$\$$  _____$$  _____$$  __$$\$$ $$  __$$\_$$  _|  
$$\   $$ |$$$$$$$ \$$\$$  /$$$$$$$ \$$$$$$\ $$ /     $$ |  \__$$ $$ /  $$ |$$ |    
$$ |  $$ $$  __$$ |\$$$  /$$  __$$ |\____$$\$$ |     $$ |     $$ $$ |  $$ |$$ |$$\ 
\$$$$$$  \$$$$$$$ | \$  / \$$$$$$$ $$$$$$$  \$$$$$$$\$$ |     $$ $$$$$$$  |\$$$$  |
 \______/ \_______|  \_/   \_______\_______/ \_______\__|     \__$$  ____/  \____/ 
                                                                 $$ |              
        P   A   R   S   E   R               -- Made by LSN       $$ |              
                                                                 \__|              
        ''')

inputfile = input('Insert file name (.js): ')
if isExist(inputfile):
    lex = LexerGrammar.Lexer(LexerGrammar.rules, skip_whitespace=True)
    cyk = CYK.Parser('CNF.txt')
    file = open(inputfile, "r", encoding="utf8")
    lineArr = []
    
    # Mencetak hasil bacaan file ke 
    print("\n")
    print("====================================  PARSING  ====================================\n")
    linecount = 0
    for line in file:
        if line != "\n" or line != "":
            lineArr.append([line, len(line) - len(line.lstrip())])
            print(line, end = "")
            linecount += 1
    file.close()
    print("\n")
    print("====================================  VERDICT  ====================================")
    print("")
    print(f"Compiling {linecount} line(s) of code from {inputfile}....")
    print("Get a result....")
    timestart = time.time()
    # Pengecekan error, parsing files
    with open(inputfile, 'r') as file:
        lines = file.readlines()
    lexList = []
    for i, line in enumerate(lines):
        lexered = ''
        if (eos) :
            eos = False
        lex.input(line)
        try:
            for tok in lex.tokens():
                lexered += f'{tok!r}'
        except LexerGrammar.LexerError as err:
            print(f'LexerError at position {err.pos}')

        lexList += lexered.split(" ")
        for j in range(len(lexList)) :
            if lexList[j] == "SINGLE_LINE_COMMENT" :
                lexList[j:] = []
                break

            if isBlockComment:
                if lexList[j] == "MULTI_LINE_COMMENT_CLOSE" :
                    lexList[j] = ""
                    isBlockComment = False
                    isAccepted = True
                    continue
                else :
                    lexList[j] = ""
                    isBlockComment = True
                    isAccepted = True
                    continue
            
            elif isString :
                if (lexList[j] == startString) :
                    isString = False
                    isAccepted = True
                    continue
                else :
                    lexList[j] = "NAME"
                    isAccepted = True
                    continue

            if lexList[j] == "MULTI_LINE_COMMENT_OPEN" :
                lexList[j] = ""
                isBlockComment = True
                continue
            
            if (lexList[j] == "SINGLE_QUOTE" or lexList[j] == "DOUBLE_QUOTE" or lexList[j] == "SMART_QUOTE") and not isString :
                isString = True
                isAccepted = True
                startString = lexList[j]
                continue
            
            if lexList[j] == "SEMICOLON" and not isForLoop :
                eos = True
                break
            
            if lexList[j] == "PAREN_CLOSE" and isForLoop :
                isForLoop = False

            if lexList[j] == "WHILE" :
                isLoop = True
                levelloop.append(level+1)
                
            if lexList[j] == "FOR" :
                isLoop = True
                isForLoop = True
                levelloop.append(level+1)
                
            if lexList[j] == "IF" :
                isIf = True
                levelif.append(level+1)
                
            if lexList[j] == "ELSE" :
                if (not (level+1) in levelif):
                    ifgagal = True
                    isAccepted = False
                    break
                else :
                    levelif.remove(level+1)
                
            if lexList[j] == "TRY" :
                isTry = True
                
            if lexList[j] == "CATCH" :
                if (not isTry):
                    trygagal = True
                    isAccepted = False
                    break
                else :
                    isCatch = True
            
            if lexList[j] == "FINALLY" :
                if (not isTry and not isCatch) :
                    trygagal = True
                    isAccepted = False
                    break
                else :
                    isTry = False
                    isCatch = False
                
            if lexList[j] == "CASE" :
                isCase = True
                eos = True
                levelcase.append(level+1)
            
            if lexList[j] == "DEFAULT" :
                isCase = True
                eos = True
                levelcase.append(level+1)
                
            if lexList[j] == "FUNCTION" :
                isFunc = True
                levelfunc.append(level+1)
                
            if lexList[j] == "BREAK" :
                if (not isLoop and not isCase):
                    isAccepted = False
                    breakgagal = True
                    break
                else :
                    isAccepted = True
                    breakgagal = False
                    
            if lexList[j] == "CONTINUE" :
                if (not isLoop):
                    isAccepted = False
                    continuegagal = True
                    break
                else :
                    isAccepted = True
                    continuegagal = False
            
            if lexList[j] == "RETURN" :
                if (not isFunc and not isLoop):
                    isAccepted = False
                    returngagalloop = True
                    returngagalfunc = True
                    break
                else :
                    isAccepted = True
                    returngagalfunc = False
                    returngagalloop = False
                    
            if lexList[j] == "WRONGNAME" :
                isAccepted = False
                break
            
            if lexList[j] == "CURFEW_CLOSE" :
                eos = True
                if level not in curfew:
                    print("Kurang kurung kurawal")
                    isAccepted = False
                    break
                elif lexList[j] == "CURFEW_CLOSE" :
                    curfew.remove(level)
                    if level in levelfunc:
                        levelfunc.remove(level)
                    if level in levelloop:
                        levelloop.remove(level)
                    if level in levelcase:
                        levelcase.remove(level)
                    level-=1
                    if levelloop == [] :
                        isLoop = False
                    if levelfunc == [] :
                        isFunc = False
                    if levelcase == [] :
                        isCase = False
                    if level+2 in levelif :
                        levelif.remove(level+2)
            if lexList[j] == "CURFEW_OPEN" :
                eos = True
                level+=1
                curfew.append(level)
        if eos or (not isAccepted) :
            lexered = ''
            if (lexList != []) :
                for k in range(j) :
                    if (lexList[k] != '') :
                        lexered += lexList[k] + " "
                if (lexList[j] != '') :
                    lexered += lexList[j]
                lexList[:j+1] = []
                cyk(lexered,parse=True)
        
        if not isAccepted:
            break
        if (eos) :
            isAccepted = cyk.print_tree(output=False)
            if not isAccepted:
                break
    
        """ print("terbaca",curfew)
        print("lexered",levelif,levelfunc,levelloop) """
    
    if (isString or isBlockComment) :
        isAccepted = False
    timefinish = time.time()
    print("\nResult:", end = " ")
    if isAccepted and curfew == []:
        print('\033[92m' + "Accepted")
    else:
        print('\033[93m' + f"\nSyntax Error at line {i+1}:")
        print('\033[93m' + f"   >> {line.strip()}\n")
        print(f"Readed: {lexered}")
    print('\033[0m')
    print('Execution time :',timefinish - timestart,'second(s)')
    print('')
    
else:
    print("There's no such file in directory!")