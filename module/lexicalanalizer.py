import re

class LexicalAnalizer:
    def __init__(self):
        self.__tokens = [
                (r'\bif\b',                'Palabra reservada if'),
                (r'\bwhile\b',             'Palabra reservada while'),
                (r'\breturn\b',            'Palabra reservada return'),
                (r'\belse\b',              'Palabra reservada else'),
                (r'\bfor\b',               'Palabra reservada for'),
                (r'\bint\b',               'Palabra reservada int'),
                (r'\bfloat\b',             'Palabra reservada float'),
                (r'\bchar\b',              'Palabra reservada char'),
                (r'\bvoid\b',              'Palabra reservada void'),
                (r'\bstring\b',            'Palabra reservada string'),
                (r'\bPI\b',                'Constante'),
                (r'[A-Za-z_][A-Za-z0-9_]*','Identificador'),
                (r';',                     'Punto y coma'),
                (r',',                     'Coma'),
                (r'\(',                    'Paréntesis abierto'),
                (r'\)',                    'Paréntesis cerrado'),
                (r'\{',                    'Llave abierta'),
                (r'\}',                    'Llave cerrada'),
                (r'\+\+',                  'Operador incremento'),
                (r'--',                    'Operador decremento'),
                (r'\+',                    'Operador suma'),
                (r'-',                     'Operador resta'),
                (r'\*',                    'Operador multiplicación'),
                (r'/',                     'Operador división'),
                (r'&&',                    'Operador AND'),
                (r'\|\|',                  'Operador OR'),
                (r'<=|>=|<|>',             'Operador relacional'),
                (r'==|!=',                 'Operación igualdad'),
                (r'=',                     'Asignación'),
                (r'\d+\.\d+',              'Real'),
                (r'\d+',                   'Entero'),
                (r'\".*?\"',               'Cadena'),
                (r'[ \n\t]+',              None),                     
            ]
    
    def analyze(self, code):
        token_regex = '|'.join(f'(?P<TOKEN_{i}>{pattern})' for i, (pattern, _) in enumerate(self.__tokens))
        compiled_re = re.compile(token_regex)
        
        pos = 0
        line_num = 0
        tokens_found = []
        errors = []

        while pos < len(code):
            match = compiled_re.match(code, pos)

            if match:
                for i, (_, tokenType) in enumerate(self.__tokens):
                    lexeme = match.group(f'TOKEN_{i}')
                    if lexeme:
                        if tokenType:
                            tokens_found.append((lexeme, tokenType, line_num + 1))
                        pos = match.end()
                        line_num += lexeme.count('\n')
                        break
            else:
                error_message = f"Error LEXICO: token no reconocido '{code[pos]}' en la linea {line_num + 1}"
                errors.append(error_message)
                pos += 1
       
        return tokens_found, errors