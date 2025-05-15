import re

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.errors = []

    def current_token(self):
        return self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None
    
    def before_token(self):
        return self.tokens[self.current_token_index - 1] if self.current_token_index > 0 else None
    
    def next_token(self):
        return self.tokens[self.current_token_index + 1] if self.current_token_index + 1 < len(self.tokens) else None

    def advance(self):
        self.current_token_index += 1

    def parse(self):
        self.errors.clear()
        tree = self.program()
        return tree, self.errors
    
    def program(self):
        nodes = []  

        while self.current_token():
            if self.current_token()[1] == 'Llave cerrada':
                return nodes
            else:
                node = self.assignment() or self.control_structure()

                if node:
                    nodes.append(node)
                else:
                    self.advance()      
        return nodes

    def assignment(self):
        token = self.current_token()

        # Caso 1: Declaración con tipo de dato
        if token and token[1] in ['Palabra reservada int', 
                                  'Palabra reservada float', 
                                  'Palabra reservada char', 
                                  'Palabra reservada string']:
            data_type = token
            self.advance()

            if self.current_token() and self.current_token()[1] == 'Identificador':
                identifier = self.current_token()
                self.advance()

                if self.current_token() and self.current_token()[1] == 'Asignación':
                    self.advance()
                    expression = self.expression()

                    if self.current_token() and self.current_token()[1] == 'Punto y coma':
                        self.advance()
                        return {
                            'type': 'assignment',
                            'data_type': data_type,
                            'identifier': identifier,
                            'expression': expression
                        }
                    else:
                        self.report_error("Falta punto y coma al final de la asignación")
                else:
                    # Declaración sin asignación
                    if self.current_token() and self.current_token()[1] == 'Punto y coma':
                        self.advance()
                        return {
                            'type': 'declaration',
                            'data_type': data_type,
                            'identifier': identifier
                        }
                    else:
                        self.report_error("Falta punto y coma al final de la declaración")
            else:
                self.report_error("Falta identificador después del tipo de dato")
            return None

        # Caso 2: Asignación sin tipo de dato
        elif token and token[1] == 'Identificador':
            identifier = token
            self.advance()

            if self.current_token() and self.current_token()[1] in ['Operador incremento', 'Operador decremento']:
                operator = self.current_token()
                self.advance()

                if self.current_token() and self.current_token()[1] == 'Punto y coma':
                    self.advance()
                    return {
                        'type': 'increment_decrement',
                        'identifier': identifier,
                        'operator': operator
                    }
                else:
                    self.report_error("Falta punto y coma al final de la operación de incremento o decremento")

            elif self.current_token() and self.current_token()[1] == 'Asignación':
                self.advance()
                expression = self.expression()

                if self.current_token() and self.current_token()[1] == 'Punto y coma':
                    self.advance()
                    return {
                        'type': 'assignment',
                        'identifier': identifier,
                        'expression': expression
                    }
                else:
                    self.report_error("Falta punto y coma al final de la asignación")
            else:
                self.report_error("Falta operador de asignación '=' en la asignación")
        return None

    def increment_for(self):
        token = self.current_token()
        
        if token and token[1] == 'Identificador':
            identifier = token
            self.advance()

            if self.current_token() and self.current_token()[1] in ['Operador incremento', 'Operador decremento']:
                operator = self.current_token()
                self.advance()

                return {
                    'type': 'increment_decrement',
                    'identifier': identifier,
                    'operator': operator
                }

            elif self.current_token() and self.current_token()[1] == 'Asignación':
                self.advance()
                expression = self.expression()

                return {
                    'type': 'assignment',
                    'identifier': identifier,
                    'expression': expression
                }

            else:
                self.report_error("Falta operador de asignación '=' en la asignación")
        return None
    
    def expression(self):
        left = self.term()

        while self.current_token() and self.current_token()[1] in ['Operador suma', 'Operador resta']:
            operator = self.current_token()
            self.advance()
            right = self.term()
            left = {'type': 'binary_operation', 'operator': operator, 'left': left, 'right': right}
        return left

    def term(self):
        left = self.factor()

        while self.current_token() and self.current_token()[1] in ['Operador multiplicación', 'Operador división']:
            operator = self.current_token()
            self.advance()
            right = self.factor()
            left = {'type': 'binary_operation', 'operator': operator, 'left': left, 'right': right}
        return left

    def factor(self):
        token = self.current_token()

        if token and token[1] in ['Identificador', 'Entero', 'Real', 'Cadena']:
            self.advance()
            return {'type': 'factor', 'value': token}
        elif token and token[1] == 'Paréntesis abierto':
            self.advance()
            expr = self.expression()
            if self.current_token() and self.current_token()[1] == 'Paréntesis cerrado':
                self.advance()
                return {'type': 'group', 'expression': expr}
            else:
                self.report_error("Falta paréntesis de cierre en la expresión")
                self.advance()
        else:
            self.report_error("Expresión no válida")
            self.advance()
        return None

    def control_structure(self):
        token = self.current_token()

        if token and token[1] == 'Palabra reservada if':
            return self.if_structure()
        elif token and token[1] == 'Palabra reservada while':
            return self.while_structure()
        elif token and token[1] == 'Palabra reservada for':
            return self.for_structure()
        return None

    def comparison_expression(self):
        left = self.expression()

        while self.current_token() and self.current_token()[1] in ['Operación igualdad', 'Operador relacional']:
            operator = self.current_token()
            self.advance()
            right = self.expression()
            left = {'type': 'comparison_operation', 'operator': operator, 'left': left, 'right': right}
        return left

    def if_structure(self):
        self.advance()

        if self.current_token() and self.current_token()[1] == 'Paréntesis abierto':
            self.advance()
            condition = self.comparison_expression()
            
            if self.current_token() and self.current_token()[1] == 'Paréntesis cerrado':
                self.advance()
                if self.current_token() and self.current_token()[1] == 'Llave abierta':

                    self.advance()
                    body = self.program()

                    if self.current_token() and self.current_token()[1] == 'Llave cerrada':
                        self.advance()
                        else_body = []
                        if self.current_token() and self.current_token()[1] == 'Palabra reservada else':
                            self.advance()
                            if self.current_token() and self.current_token()[1] == 'Llave abierta':
                                self.advance()
                                else_body = self.program()
                                if self.current_token() and self.current_token()[1] == 'Llave cerrada':
                                    self.advance()
                                else:
                                    self.report_error("Falta llave de cierre en el bloque 'else'")
                            else:
                                self.report_error("Falta llave de apertura en el bloque 'else'")
                        return {'type': 'if', 'condition': condition, 'body': body, 'else_body': else_body}
                    else:
                        self.report_error("Falta llave de cierre en la estructura 'if'")
                else:
                    self.report_error("Falta llave de apertura en la estructura 'if'", "if")
            else:
                self.report_error("Falta paréntesis de cierre en la condición del 'if'")
        else:
            self.report_error("Falta paréntesis de apertura en la condición del 'if'", "if")
        return None

    def while_structure(self):
        self.advance()

        if self.current_token() and self.current_token()[1] == 'Paréntesis abierto':
            self.advance()
            condition = self.comparison_expression()

            if self.current_token() and self.current_token()[1] == 'Paréntesis cerrado':
                self.advance()

                if self.current_token() and self.current_token()[1] == 'Llave abierta':
                    self.advance()
                    body = self.program()

                    if self.current_token() and self.current_token()[1] == 'Llave cerrada':
                        self.advance()
                        return {'type': 'while', 'condition': condition, 'body': body}
                    else:
                        self.report_error("Falta llave de cierre en la estructura 'while'")
                else:
                    self.report_error("Falta llave de apertura en la estructura 'while'")
            else:
                self.report_error("Falta paréntesis de cierre en la condición del 'while'")
        else:
            self.report_error("Falta paréntesis de apertura en la condición del 'while'")
        return None

    def for_structure(self):
        self.advance()

        if self.current_token() and self.current_token()[1] == 'Paréntesis abierto':
            self.advance()
            initialization = self.assignment()            
            # Ya no se verifica el punto y coma aquí de la inicialización, 
            # ya que es parte de la asignación

            condition = self.comparison_expression()

            if self.current_token() and self.current_token()[1] == 'Punto y coma':
                self.advance()
                increment = self.increment_for()

                if self.current_token() and self.current_token()[1] == 'Paréntesis cerrado':
                    self.advance()

                    if self.current_token() and self.current_token()[1] == 'Llave abierta':
                        self.advance()
                        body = self.program()

                        if self.current_token() and self.current_token()[1] == 'Llave cerrada':
                            self.advance()
                            return {
                                'type': 'for',
                                'initialization': initialization,
                                'condition': condition,
                                'increment': increment,
                                'body': body
                            }
                        else:
                            self.report_error("Falta llave de cierre en la estructura 'for'")
                    else:
                        self.report_error("Falta llave de apertura en la estructura 'for'")
                else:
                    self.report_error("Falta paréntesis de cierre en la estructura 'for'")
            else:
                self.report_error("Falta punto y coma después de la condición en la estructura 'for'")
        else:
            self.report_error("Falta paréntesis de apertura en la estructura 'for'")
        return None

    def function_declaration(self):
        token = self.current_token()

        if token and token[1] in ['Palabra reservada int', 
                                  'Palabra reservada float', 
                                  'Palabra reservada char', 
                                  'Palabra reservada void', 
                                  'Palabra reservada string']:
            return_type = token
            self.advance()

            if self.current_token() and self.current_token()[1] == 'Identificador':
                function_name = self.current_token()
                self.advance()

                if self.current_token() and self.current_token()[1] == 'Paréntesis abierto':
                    self.advance()

                    parameters = self.parameters()

                    if self.current_token() and self.current_token()[1] == 'Paréntesis cerrado':
                        self.advance()

                        if self.current_token() and self.current_token()[1] == 'Llave abierta':
                            self.advance()

                            body = []
                            while self.current_token() and self.current_token()[1] != 'Llave cerrada':
                                statement = self.assignment() or self.control_structure() or self.return_statement()
                                if statement:
                                    body.append(statement)
                                else:
                                    self.report_error("Instrucción no válida en el cuerpo de la función")
                                    self.advance()

                            if self.current_token() and self.current_token()[1] == 'Llave cerrada':
                                self.advance()
                                return {
                                    'type': 'function_declaration',
                                    'return_type': return_type,
                                    'name': function_name,
                                    'parameters': parameters,
                                    'body': body
                                }
                            else:
                                self.report_error("Falta llave de cierre en la declaración de la función")
                        else:
                            self.report_error("Falta llave de apertura en la declaración de la función")
                    else:
                        self.report_error("Falta paréntesis de cierre en la declaración de la función")
                else:
                    self.report_error("Falta paréntesis de apertura en la declaración de la función")
        return None

    def parameters(self):
        parameters = []

        while self.current_token() and self.current_token()[1] in ['Palabra reservada int', 'Palabra reservada float', 'Palabra reservada char', 'Palabra reservada void', 'Palabra reservada string']:
            param_type = self.current_token()
            self.advance()

            if self.current_token() and self.current_token()[1] == 'Identificador':
                param_name = self.current_token()
                self.advance()
                parameters.append({'type': param_type, 'name': param_name})

                if self.current_token() and self.current_token()[1] == 'Coma':
                    self.advance()
                else:
                    break
            else:
                self.report_error("Falta identificador para el parámetro")
                break
        return parameters

    def report_error(self, message, type=None):
        token = None

        if type == "if":
            token = self.before_token()
        else:
            token = self.current_token()

        line = token[2] if token else "desconocida"
        self.errors.append(f"{message} en la línea {line}")
        self.advance()
    
    def return_statement(self):
        self.advance()
        
        expression = self.expression()
        if self.current_token() and self.current_token()[1] == 'Punto y coma':
            self.advance()
            return {'type': 'return', 'expression': expression}
        else:
            self.report_error("Falta punto y coma al final de la declaración 'return'")
        return None