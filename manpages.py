from roffllexer import RofflLexer
from rofflparser import RofflParser
import gzip

MANPATH = "/usr/share/man/man1/"

grep = MANPATH + "grep.1"
python = MANPATH + "python.1.gz"
ruby = MANPATH + "ruby.1.gz"

with gzip.open(ruby, 'r') as g:
    manpage = g.read()

print manpage

roffl_lexer = RofflLexer()
roffl_lexer.build(debug=1)
roffl_lexer.test('.He Banana')

roffl_parser = RofflParser()
roffl_parser.build(roffl_lexer, debug=1)

ptree = roffl_parser.test_parser(manpage)

i = 1
for l in ptree[:50]:
    print i, l
    i += 1
