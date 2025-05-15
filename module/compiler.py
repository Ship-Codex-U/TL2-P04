from module.lexicalanalizer import LexicalAnalizer
from module.parser import Parser
from module.semanticanalyzer import SemanticAnalyzer
from module.generateassembly import GenerateAssembly

class Compiler:
    def __init__(self):
        self.__tokensFound = []
        self.__tree = None

        self.__found_errors = False

    def lexicalAnalyser(self, code : str) -> tuple[list, list]:
        lexicalAnalizer = LexicalAnalizer()
        [self.__tokensFound, errors] = lexicalAnalizer.analyze(code)

        if errors:
            self.__found_errors = True 

        return (self.__tokensFound, errors)
    
    def parser(self):
        parser = Parser(self.__tokensFound)
        [self.__tree, errors] = parser.parse()

        if errors:
            self.__found_errors = True

        return (self.__tree, errors[0] if errors else None)
    
    def semanticAnalyser(self):
        semanticAnalyzer = SemanticAnalyzer(self.__tree)
        errors = semanticAnalyzer.analyze()

        if errors:
            self.__found_errors = True

        return errors if errors else None
    
    def generateAssembly(self):
        if self.__found_errors:
            return "No es posible generar el código de ensamblador debido a errores en el codigo."

        generator = GenerateAssembly()
        assembly_code = generator.generateAssembly(self.__tree)

        return assembly_code
        
