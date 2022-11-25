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
        P   A   R   S   E   R               -- Made by XXXX      $$ |              
                                                                 \__|              
        ''')

inputfile = input('Insert file name (.js): ')
if isExist(inputfile):
    lex = LexerGrammar.Lexer(LexerGrammar.rules, skip_whitespace=True)
    cyk = CYK.Parser('cnf.txt')
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
    for i, line in enumerate(lines):
        lexered = ''
        lex.input(line)
        try:
            for tok in lex.tokens():
                lexered += f'{tok!r}'
        except LexerGrammar.LexerError as err:
            print(f'LexerError at position {err.pos}')

        lexList = lexered.split(" ")
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
            
            if isString :
                if (lexList[j] == "SINGLE_QUOTE" or lexList[j] == "DOUBLE_QUOTE" or lexList[j] == "SMART_QUOTE") :
                    isString = False
                isAccepted = True
                continue

            if lexList[j] == "MULTI_LINE_COMMENT_OPEN" :
                lexList[j] = ""
                isBlockComment = True
                continue
            
            if (lexList[j] == "SINGLE_QUOTE" or lexList[j] == "DOUBLE_QUOTE" or lexList[j] == "SMART_QUOTE") and not isString :
                isString = True
                isAccepted = True
                continue

            if lexList[j] == "WHILE" :
                isLoop = True
                levelloop.append(level+1)
                
            if lexList[j] == "FOR" :
                isLoop = True
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
                    
            if lexList[j] == "WRONGNAME" :
                isAccepted = False
                break
            
            if lexList[j] == "CURFEW_CLOSE" :
                if level not in curfew:
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
                        isFunc = False
            if lexList[j] == "CURFEW_OPEN" :
                level+=1
                curfew.append(level)
        lexered = ''
        for j in range(len(lexList)) :
            lexered += lexList[j] + " "
        # print(lexered)
        if (isString or isBlockComment) :
            isAccepted = False
        cyk(lexered,parse=True)
        if not isAccepted:
            break
        isAccepted = cyk.print_tree(output=False)
        if not isAccepted:
            break
    
        # print(isFunc,isLoop,returngagalfunc,returngagalloop)
        """ print("terbaca",curfew)
        print("lexered",levelif,levelfunc,levelloop) """
        
    timefinish = time.time()
    print("\nResult:", end = " ")
    if isAccepted and curfew == []:
        print('\033[92m' + "Accepted")
    else:
        print('\033[93m' + f"\nSyntax Error at line {i+1}:")
        print('\033[93m' + f"   >> {line.strip()}\n")
        """ if breakgagal:
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
            print('\033[93m' + f"Tidak dapat menambahkan else sebelum ada if\n") """
        print(f"Readed: {lexered}")
    print('\033[0m')
    print('Execution time :',timefinish - timestart,'second(s)')
    print('')
    
else:
    print("There's no such file in directory!")