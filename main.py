from os.path import isfile as isExist
""" import lexer
import cyk """

isBlockComment = False
isSkipUntilNextBC = False
isDef = False
isAccepted = True
isIfLevel = []
level = 0

print('JAVASCRIPT PARSER (beta version)')
print('[lebih ke blm ngapa2in sih]\n')

inputfile = input('Insert file name (.js): ')
if isExist(inputfile):
    """ lx = lexer.Lexer(lexer.rules, skip_whitespace=True)
    CYK = cyk.Parser('cnf.txt') """
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
        # lx.input(line)
        
    # Results
    print("\nResult:", end = " ")
    if isAccepted:
        print('\033[92m' + "Accepted")
    else:
        print('\033[93m' + f"\nSyntax Error at line {i+1}:")
        print('\033[93m' + f"   >> {line.strip()}\n")
        print(f"Readed: {lexered}")
    print('\033[0m')
    
else:
    print("There's no such file in directory!")