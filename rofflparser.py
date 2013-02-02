import ply.yacc as yacc


class RofflParser:

    start = 'roff'

    def p_roff_line_roff(self, p):
        'roff : line roff'
        p[0] = [p[1]] + p[2]

    def p_roff_empty(self, p):
        'roff : '
        p[0] = []

    def p_line_command_NEWLINE(self, p):
        'line : command NEWLINE'
        p[0] = p[1]

    def p_line_comment_NEWLINE(self, p):
        'line : comment NEWLINE'
        p[0] = p[1]

    def p_line_phrase(self, p):
        'line : phrase NEWLINE'
        p[0] = p[1]

    def p_line_COMMENT_phrase_NEWLINE(self, p):
        'comment : COMMENT phrase'
        p[0] = ("comment", p[2])

    def p_command_MACRO_compoundstatement(self, p):
        'command : MACRO compoundstatement'
        p[0] = ("macro", p[1], p[2])

    def p_compoundstatement_statements(self, p):
        'compoundstatement : statements'
        p[0] = p[1]

    def p_statements_empty(self, p):
        'statements : '
        p[0] = []

    def p_statements_statement_statements(self, p):
        'statements : statement statements'
        p[0] = [p[1]] + [p[2]]

    def p_statement_compoundstatement(self, p):
        'statement : MACRO compoundstatement'
        p[0] = ("macro", p[1], p[2])

    def p_statement_phrase(self, p):
        'statement : phrase'
        p[0] = p[1]

    def p_phrase_word_phrase(self, p):
        'phrase : word phrase'
        p[0] = [p[1]] + p[2]

    def p_phrase_empty(self, p):
        'phrase : '
        p[0] = []

    def p_phrase_ESCAPE(self, p):
        'word : ESCAPE'
        p[0] = ("escape", p[1])

    def p_phrase_WORD(self, p):
        'word : WORD'
        p[0] = ("word", p[1])

    def p_phrase_NUMBER(self, p):
        'word : NUMBER'
        p[0] = ("number", p[1])

    def p_phrase_STRING(self, p):
        'word : STRING'
        p[0] = ("string", p[1])

    def p_error(self, p):
        print "Syntax error at '%s'" % p.value

    def build(self, lexer, **kwargs):
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self, **kwargs)

    def test_parser(self, input_string):
        parse_tree = self.parser.parse(input_string)
        return parse_tree
