# Lexer of Grammar
# Take a deep down to algoritm anaysis about how CYK reads the algorithm

import re
import os.path

rules = [
        ('for', 'FOR'),
        ('while', 'WHILE'),
        ('\/\/', 'SINGLE_LINE_COMMENT'),
        ('\/\*', 'MULTI_LINE_COMMENT_OPEN'),
        ('\*\/', 'MULTI_LINE_COMMENT_CLOSE'),
        ('===', 'TRIPLE_EQUAL'),
        ('==', 'DOUBLE_EQUAL'),
        ('=', 'EQUAL_SIGN'),
        ('!==', 'NOT_DOUBLE_EQUAL'),
        ('!=', 'NOT_EQUAL'),
        ('>=', 'GREATER_EQUAL'),
        ('>', 'GREATER'),
        ('<=', 'LESS_EQUAL'),
        ('<', 'LESS'),
        ('\?', 'TERNARY'),
        ('\+', 'PLUS'),
        ('\-', 'MINUS'),
        ('\*', 'MULTI'),
        ('\/', 'DIVIDE'),
        ('\*\*', 'EXPO'),
        ('%', 'MOD'),
        ('&&', 'AND'),
        ('\|\|', 'OR'),
        ('\?\?', 'NULLISH'),
        ('&', 'BITWISE_AND'),
        ('\|', 'BITWISE_OR'),
        ('\^', 'XOR'),
        ('<<', 'LEFT_SHIFT'),
        ('>>', 'RIGHT_SHIFT'),
        ('>>>', 'UNSIGNED_LEFT_SHIFT'),
        (';', 'SEMICOLON'),
        ('!', 'NOT'),
        (',', 'COMMA'),
        (r"\\'", 'SINGLE_QUOTE_ESCAPE_CHAR'),
        (r'\\"', 'DOUBLE_QUOTE_ESCAPE_CHAR'),
        ('null', 'NULL'),
        ('break', 'BREAK'),
        ('continue', 'CONTINUE'),
        ('return', 'RETURN'),
        ('function', 'FUNCTION'),
        ('\(', 'PAREN_OPEN'),
        ('\)', 'PAREN_CLOSE'),
        ('\{', 'CURFEW_OPEN'),
        ('\}', 'CURFEW_CLOSE'),
        ('"', 'DOUBLE_QUOTE'),
        ("'", 'SINGLE_QUOTE'),
        ('`', 'SMART_QUOTE'),
        ('true', 'TRUE'),
        ('false', 'FALSE'),
        ('if\W', 'IF'),
        ('else\W', 'ELSE'),
        ('switch', 'SWITCH'),
        ('case', 'CASE'),
        ('default', 'DEFAULT'),
        (':', 'COLON'),
        ('\.','DOT'),
        ('\d+\.\d+', 'TYPE_FLOAT'),
        ('\d+', 'TYPE_INT'),
        ('let\s+', 'LET'),
        ('var\s+', 'VAR'),
        ('const\s+', 'CONST'),
        ('in\s+', 'IN'),
        ('of\s+', 'OF'),
        ('as\s+', 'AS'),
        ('is\s+', 'IS'),
        ('throw', 'THROW'),
        ('delete', 'DELETE'),
        ('try', 'TRY'),
        ('catch', 'CATCH'),
        ('finally', 'FINALLY'),
        ('[a-zA-Z_]\w*', 'NAME')
    ]

class Token(object):
    def __init__(self, type, val, pos):
        self.type = type
        self.val = val
        self.pos = pos

    def __str__(self):
        return f"{self.type}({self.val}) at {self.pos}"

    def __repr__(self):
        return f"{self.type} "


class LexerError(Exception):
    def __init__(self, pos):
        self.pos = pos


class Lexer(object):
    def __init__(self, rules, skip_whitespace=True):
        idx = 1
        regex_parts = []
        self.group_type = {}

        for regex, type in rules:
            groupname = f"GROUP{idx}"
            regex_parts.append(f'(?P<{groupname}>{regex})')
            self.group_type[groupname] = type
            idx += 1
        self.regex = re.compile('|'.join(regex_parts))
        self.skip_whitespace = skip_whitespace
        self.re_ws_skip = re.compile('\S')

    def input(self, buf):
        source = ''
        if os.path.isfile(buf):
            with open(buf, "r") as file:
                lines = file.readlines()
                for line in lines:
                    source += line
                
        else:
            source = buf
        # print(source)
        self.buf = source
        self.pos = 0

    def token(self):
        if self.pos >= len(self.buf):
            return None
        else:
            if self.skip_whitespace:
                m = self.re_ws_skip.search(self.buf, self.pos)

                if m:
                    self.pos = m.start()
                else:
                    return None

            m = self.regex.match(self.buf, self.pos)
            if m:
                groupname = m.lastgroup
                tok_type = self.group_type[groupname]
                tok = Token(tok_type, m.group(groupname), self.pos)
                self.pos = m.end()
                return tok

            # if we're here, no rule matched
            raise LexerError(self.pos)

    def tokens(self):
        while 1:
            tok = self.token()
            if tok is None: break
            yield tok