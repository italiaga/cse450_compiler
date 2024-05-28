from .lexing import do_source_lexing
from .parsing import do_source_parsing
from .exceptions import SourceLexingException
from .symbol_table import CompilerSymbolTable

def filter_source_tokens(tok):
    if tok.name == 'ERROR':
        raise SourceLexingException('Error token found in token stream.')
    else:
        return not tok.name.startswith('COMMENT')



def lex_source(src):
    tokens, possible_tokens = do_source_lexing(src)
    tokens = list(filter(filter_source_tokens, tokens))
    possible_tokens = set(filter(lambda x: not x.startswith('COMMENT'), possible_tokens))
    return tokens, possible_tokens


def parse_source(src):
    tokens, possible_tokens = lex_source(src)
    return do_source_parsing(tokens, possible_tokens)


def compile_source_intermediate(src):
    ast_root = parse_source(src)
    st = CompilerSymbolTable()
    output = []
    ast_root.compile(st, output)
    return '\n'.join(output) + '\n'