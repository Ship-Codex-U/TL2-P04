from module.lexicalanalizer import LexicalAnalizer
from module.parser import Parser
from module.semanticanalyzer import SemanticAnalyzer

class Compiler:
    def __init__(self):
        self.__code = ""
        self.__tokensFound = []
        self.__tree = None

    def lexicalAnalyser(self, code : str) -> tuple[list, list]:
        lexicalAnalizer = LexicalAnalizer()
        [self.__tokensFound, errors] = lexicalAnalizer.analyze(code)
        
        return (self.__tokensFound, errors)
    
    def parser(self):
        parser = Parser(self.__tokensFound)

        [self.__tree, errors] = parser.parse()

        return (self.__tree, errors[0] if errors else None)
    
    def semanticAnalyser(self):
        semanticAnalyzer = SemanticAnalyzer(self.__tree)
        errors = semanticAnalyzer.analyze()

        return errors if errors else None
        
