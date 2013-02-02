import ply.lex as lex


class RofflLexer:
    tokens = (
        'STRING',   # "synopsis banana! syzygy)).%"
        'ESCAPE',   # \&(
        'MACRO',    # .TH .Af .sp
        'TAG',      # \fB \f(R
        'NUMBER',   # 1
        'NEWLINE',  # \n
        'WORD',     # synopsis banana syzygy
        'COMMENT',  # .\" Ignore this!
    )

    t_ignore = " \t"

    def t_STRING(self, t):
        r'"[^"]*"'
        t.value = t.value[1:-1].replace('\\', '')
        return t

    def t_COMMENT(self, t):
        r'\.\\\"'
        return t

    def t_ESCAPE(self, t):
        r'\\\*\([A-Za-z]{1,2}'
        t.value = t.value[-2:]
        return t

    def t_MACRO(self, t):
        r'(?:\.[A-Z][a-z]|\.[A-Z]{2}|\.[a-z]{2}|\.[A-Z]|[A-Z][a-z])(?=\s)'
        if len(t.value) == 2:
            if t.value[0] == ".":
                t.value = t.value[-1:]
        else:
            t.value = t.value[-2:]
        return t

    """
    def t_FLAG(self, t):
        r'-[a-z]+'
        t.value = t.value[1:]
        return t
    """

    """
    def t_TAGCLOSE(self, t):
        r'\\fP|\\x0cP'
        return t
    """

    def t_TAG(self, t):
        r'\f[A-Z]|\x0c[A-Z]'
        t.value = t.value[1:]
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
        return t

    def t_WORD(self, t):
        r'[^\n\ ]+'
        t.value = t.value.replace('\\', '')
        return t

    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, string):
        self.lexer.input(string)
        result = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            result = result + [(tok.type, tok.value)]
        return result
