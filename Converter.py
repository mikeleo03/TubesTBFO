# Converter from CFG to CNF
# By taking refrences from https://github.com/RobMcH/CYK-Parser/blob/master/grammar_converter.py

RULE_DICT = {}

def read_grammar(grammar_file):
    with open(grammar_file) as cfg:
        lines = cfg.readlines()
    return [x.replace("->", "").split() for x in lines]

def add_rule(rule):
    global RULE_DICT

    if rule[0] not in RULE_DICT:
        RULE_DICT[rule[0]] = []
    RULE_DICT[rule[0]].append(rule[1:])

def convert_grammar(grammar):
    # Remove all the productions of the type A -> X B C or A -> B a.
    global RULE_DICT
    unit_productions, result = [], []
    res_append = result.append
    index = 0

    for rule in grammar:
        new_rules = []
        if len(rule) == 2 and rule[1][0] != "'":
            # Rule is in form A -> X, so back it up for later and continue with the next rule.
            unit_productions.append(rule)
            add_rule(rule)
            continue
        elif len(rule) > 2:
            # Rule is in form A -> X B C [...] or A -> X a.
            terminals = [(item, i) for i, item in enumerate(rule) if item[0] == "'"]
            if terminals:
                for item in terminals:
                    # Create a new non terminal symbol and replace the terminal symbol with it.
                    # The non terminal symbol derives the replaced terminal symbol.
                    rule[item[1]] = f"{rule[0]}{str(index)}"
                    new_rules += [f"{rule[0]}{str(index)}", item[0]]
                index += 1
            while len(rule) > 3:
                new_rules.append([f"{rule[0]}{str(index)}", rule[1], rule[2]])
                rule = [rule[0]] + [f"{rule[0]}{str(index)}"] + rule[3:]
                index += 1
        # Adds the modified or unmodified (in case of A -> x i.e.) rules.
        add_rule(rule)
        res_append(rule)
        if new_rules:
            result.extend(new_rules)
    # Handle the unit productions (A -> X)
    while unit_productions:
        rule = unit_productions.pop()
        if rule[1] in RULE_DICT:
            for item in RULE_DICT[rule[1]]:
                new_rule = [rule[0]] + item
                if len(new_rule) > 2 or new_rule[1][0] == "'":
                    result.insert(0, new_rule)
                else:
                    unit_productions.append(new_rule)
                add_rule(new_rule)
    # Write result to external file named 'CNF.txt'
    with open('CNF.txt', 'w') as file:
        for element in result:
            if len(element)==3:
                file.write(f'{element[0]} -> {element[1]} {element[2]}\n')
            elif len(element)==2:
                file.write(f'{element[0]} -> {element[1]}\n')
    
    return result

# Main program
coba = read_grammar('CFG.txt')
convert_grammar(coba)