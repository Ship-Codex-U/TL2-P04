# Comentar todo el codigo de la clase SemanticAnalyzer en español

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.errors = []

    def analyze(self):
        self.errors.clear()
        # Inicia el análisis desde el nodo raíz
        self._analyze_node(self.ast, scope={})

        return self.errors

    def _analyze_node(self, node, scope):
        if isinstance(node, list):
            for child in node:
                self._analyze_node(child, scope)
        
        # Si el nodo es un diccionario, analizar según su tipo
        elif isinstance(node, dict):  
            node_type = node.get('type')
            if node_type == 'declaration':
                self._handle_declaration(node, scope)

            elif node_type == 'assignment':
                self._handle_assignment(node, scope)

            elif node_type == 'while':
                self._handle_while(node, scope)

            elif node_type == 'if':
                self._handle_if(node, scope)

            elif node_type == 'for':
                self._handle_for(node, scope)

            elif node_type == 'binary_operation':
                self._handle_binary_operation(node, scope)

            elif node_type == 'comparison_operation':
                self._handle_comparison_operation(node, scope)

            elif node_type == 'increment_decrement':
                self._handle_increment_decrement(node, scope)

            else:
                self.errors.append(f"Tipo de nodo desconocido: {node_type}")

    def _handle_declaration(self, node, scope):
        data_type = node['data_type'][0]
        identifier = node['identifier'][0]
        line = node['identifier'][2]

        if identifier in scope:
            self.errors.append(f"Linea {line}: La variable '{identifier}' ya está declarada en este ámbito.")
        else:
            scope[identifier] = data_type

    def _handle_assignment(self, node, scope):    
        if 'data_type' in node:
            data_type = node['data_type'][0]
            identifier = node['identifier'][0]
            line = node['identifier'][2]

            if identifier in scope:
                self.errors.append(f"Linea {line}: La variable '{identifier}' ya está declarada en este ámbito.")
            else:
                scope[identifier] = data_type
                
        identifier = node['identifier'][0]
        line = node['identifier'][2]

        if identifier not in scope:
            self.errors.append(f"Linea {line}: La variable '{identifier}' no está declarada.")

        else:
            expected_type = scope[identifier]
            expression_type = self._evaluate_expression(node['expression'], scope)

            if not self._is_compatible(expected_type, expression_type):
                self.errors.append(f"Linea {line}: Asignación incompatible. Se esperaba '{expected_type}' pero se obtuvo '{expression_type}' en la linea {line}.")

    def _handle_while(self, node, scope):
        condition_type = self._evaluate_expression(node['condition'], scope)

        if condition_type != 'int':
            self.errors.append("La condición del 'while' debe ser de tipo 'int'.")

        new_scope = scope.copy()

        for statement in node['body']:
            self._analyze_node(statement, new_scope)

    def _handle_if(self, node, scope):
        condition_type = self._evaluate_expression(node['condition'], scope)

        if condition_type is None:
            self.errors.append("La condición del 'if' no es válida.")
            return
        
        if condition_type != 'int':
            self.errors.append("La condición del 'if' debe ser de tipo 'int'.")

        new_scope = scope.copy()

        for statement in node['body']:
            self._analyze_node(statement, new_scope)

        if 'else_body' in node:
            for statement in node['else_body']:
                self._analyze_node(statement, new_scope)

    def _handle_for(self, node, scope):
        new_scope = scope.copy()
        self._analyze_node(node['initialization'], new_scope)
        condition_type = self._evaluate_expression(node['condition'], new_scope)
        
        if condition_type != 'int':
            self.errors.append("La condición del 'for' debe ser de tipo 'int'.")

        self._analyze_node(node['increment'], new_scope)

        for statement in node['body']:
            self._analyze_node(statement, new_scope)

    def _handle_binary_operation(self, node, scope):
        left_type = self._evaluate_expression(node['left'], scope)
        right_type = self._evaluate_expression(node['right'], scope)
        operator = node['operator'][0]

        if operator in ['+', '-', '*', '/']:
            if left_type in ['int', 'float'] and right_type in ['int', 'float']:
                if operator == '/' and node['right']['type'] == 'factor' and node['right']['value'][1] == 'Entero' and node['right']['value'][0] == '0':
                    self.errors.append("División por cero detectada, esta operacion no se puede realizar.")
                    return None

                return 'float' if 'float' in [left_type, right_type] else 'int'
            else:
                self.errors.append("Operación aritmética con operandos no numéricos.")
                return None
            
        return None
    
    def _handle_increment_decrement(self, node, scope):
        identifier = node['identifier'][0]
        line = node['identifier'][2]
        operator = node['operator'][0]

        if identifier not in scope:
            self.errors.append(f"Linea {line}: La variable '{identifier}' no está declarada.")
            return

        if operator not in ['++', '--']:
            self.errors.append(f"Linea {line}: Operador de incremento/decremento inválido '{operator}'.")

    def _handle_comparison_operation(self, node, scope):
        left_type = self._evaluate_expression(node['left'], scope)
        right_type = self._evaluate_expression(node['right'], scope)

        if left_type != right_type:
            self.errors.append("Comparación entre tipos incompatibles.")
            return None
        
        return 'int'

    def _evaluate_expression(self, expression, scope):
        if expression['type'] == 'factor':
            value_type = expression['value'][1]

            if value_type == 'Identificador':
                identifier = expression['value'][0]
                

                if identifier in scope:
                    return scope[identifier]
                
                else:
                    self.errors.append(f"La variable '{identifier}' no está declarada.")
                    return None
                
            elif value_type in ['Entero', 'Real', 'Cadena']:
                return {'Entero': 'int', 'Real': 'float', 'Cadena': 'string'}[value_type]
            
        elif expression['type'] == 'binary_operation':
            return self._handle_binary_operation(expression, scope)
        
        elif expression['type'] == 'comparison_operation':
            return self._handle_comparison_operation(expression, scope)
        
        elif expression['type'] == 'group':
            return self._evaluate_expression(expression['expression'], scope)
        
        else:
            self.errors.append("Expresión no válida.")
            return None

    def _is_compatible(self, expected_type, actual_type):
        if expected_type == actual_type:
            return True
        
        if expected_type == 'float' and actual_type == 'int':
            return True
        
        return False