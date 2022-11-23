# Main program 
# The main program and all syntax checking problems, calling exteernal functions

from os.path import isfile as isExist
import LexerGrammar
import CYK

isBlockComment = False
isSkipUntilNextBC = False
isDef = False
isAccepted = True
isIfLevel = []
level = 0

print('JAVASCRIPT PARSER (gamma version)')
print('[better version tapi masih gws]\n')

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
        if "DEF" in lexered:
            level+=1
            isDef = True
        """
        
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
        print(f"Readed: {lexered}")
    print('\033[0m')
    
else:
    print("There's no such file in directory!")