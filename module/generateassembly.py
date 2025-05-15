class GenerateAssembly:
    def __init__(self):
        self.assembly_code = []  # Lista para almacenar las instrucciones de ensamblador
        self.data_section = []  # Sección .data para variables
        self.temp_counter = 0    # Contador para registros temporales (enteros)
        self.temp_float_counter = 0 # Contador para registros temporales (float)
        self.label_counter = 0   # Contador para etiquetas

    def generateAssembly(self, tree) -> str:
        # Genera el código ensamblador MIPS a partir del árbol de análisis sintáctico/semántico.

        # Generar la sección de datos
        self.generate_data_section(tree)

        # Generar el código ensamblador
        for node in tree:
            self.translate_node(node, tree)

        # Combinar la sección de datos y el código ensamblador
        return "\n".join([".data"] + self.data_section + [".text"] + self.assembly_code)

    def generate_data_section(self, tree):
        # Genera la sección .data para las variables utilizadas en el árbol.

        declared_variables = set()
        for node in tree:
            if node['type'] in ['declaration', 'assignment']:
                identifier = node['identifier'][0]
                if identifier not in declared_variables:
                    declared_variables.add(identifier)
                    data_type = node.get('data_type')

                    if node['type'] == 'declaration':
                        if data_type and data_type[0] == 'string':
                            self.data_section.append(f"{identifier}: .space 32")
                        elif data_type and data_type[0] == 'float':
                            self.data_section.append(f"{identifier}: .float 0.0")
                        else:
                            self.data_section.append(f"{identifier}: .word 0")
                    elif node['type'] == 'assignment':
                        if data_type and data_type[0] == 'string':
                            self.data_section.append(f"{identifier}: .space 32")
                        elif data_type and data_type[0] == 'float':
                            # Initial value will be set in .text
                            self.data_section.append(f"{identifier}: .float 0.0")
                        else:
                            self.data_section.append(f"{identifier}: .word 0")
            elif node['type'] == 'for' and 'initialization' in node:
                init_node = node['initialization']
                if init_node['type'] == 'assignment':
                    identifier = init_node['identifier'][0]
                    if identifier not in declared_variables:
                        declared_variables.add(identifier)
                        self.data_section.append(f"{identifier}: .word 0")

    def new_temp(self):
        # Genera un nuevo registro temporal ($t0-$t9).
        temp = f"$t{self.temp_counter}"
        self.temp_counter = (self.temp_counter + 1) % 10  # Usa $t0-$t9 de forma cíclica
        return temp

    def new_temp_float(self):
        # Genera un nuevo registro temporal de punto flotante ($f0-$f30, saltando de 2 en 2 para doubles si es necesario).
        temp = f"$f{self.temp_float_counter}"
        self.temp_float_counter = (self.temp_float_counter + 2) % 32
        return temp

    def new_label(self):
        # Genera una nueva etiqueta única.
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def get_node_type(self, identifier, tree):
        for node in tree:
            if (node['type'] == 'declaration' or node['type'] == 'assignment') and node['identifier'][0] == identifier:
                return node.get('data_type')[0]
            elif node['type'] == 'for' and 'initialization' in node:
                init_node = node['initialization']
                if init_node['type'] == 'assignment' and init_node['identifier'][0] == identifier:
                    return init_node.get('data_type')[0]
        return None

    def translate_expression(self, expression, tree):
        if expression['type'] == 'factor':
            value = expression['value'][0]
            data_type = expression['value'][1]
            temp = self.new_temp_float() if data_type == 'Flotante' else self.new_temp()
            if data_type == 'Cadena':
                # Las cadenas se manejan directamente en las asignaciones
                stripped_value = value.strip('"')  # Realiza el strip fuera del f-string
                return f"\"{stripped_value}\""
            else:
                temp = self.new_temp()
                self.assembly_code.append(f"li {temp}, {value}")
                return temp
        elif expression['type'] == 'binary_operation':
            left = self.translate_expression(expression['left'], tree)
            right = self.translate_expression(expression['right'], tree)
            operator = expression['operator'][0]
            is_float = self.is_float_expression(expression, tree)
            if is_float:
                temp = self.new_temp_float()
                if operator == '+':
                    self.assembly_code.append(f"add.s {temp}, {left}, {right}")
                elif operator == '-':
                    self.assembly_code.append(f"sub.s {temp}, {left}, {right}")
                elif operator == '*':
                    self.assembly_code.append(f"mul.s {temp}, {left}, {right}")
                elif operator == '/':
                    self.assembly_code.append(f"div.s {temp}, {left}, {right}")
                return temp
            else:
                temp = self.new_temp()
                if operator == '+':
                    self.assembly_code.append(f"add {temp}, {left}, {right}")
                elif operator == '-':
                    self.assembly_code.append(f"sub {temp}, {left}, {right}")
                elif operator == '*':
                    self.assembly_code.append(f"mul {temp}, {left}, {right}")
                elif operator == '/':
                    self.assembly_code.append(f"div {temp}, {left}, {right}")
                return temp
        elif expression['type'] == 'group':
            return self.translate_expression(expression['expression'], tree)
        elif expression['type'] == 'comparison_operation':
            left = self.translate_expression(expression['left'], tree)
            right = self.translate_expression(expression['right'], tree)
            operator = expression['operator'][0]
            is_float = self.is_float_comparison(expression, tree)
            temp = self.new_temp()
            if is_float:
                if operator == '==':
                    self.assembly_code.append(f"seq.s {temp}, {left}, {right}")
                elif operator == '<=':
                    self.assembly_code.append(f"sle.s {temp}, {left}, {right}")
                elif operator == '>=':
                    self.assembly_code.append(f"sge.s {temp}, {left}, {right}")
                elif operator == '<':
                    self.assembly_code.append(f"slt.s {temp}, {left}, {right}")
                elif operator == '>':
                    self.assembly_code.append(f"sgt.s {temp}, {left}, {right}")
            else:
                if operator == '==':
                    self.assembly_code.append(f"seq {temp}, {left}, {right}")
                elif operator == '<=':
                    self.assembly_code.append(f"sle {temp}, {left}, {right}")
                elif operator == '>=':
                    self.assembly_code.append(f"sge {temp}, {left}, {right}")
                elif operator == '<':
                    self.assembly_code.append(f"slt {temp}, {left}, {right}")
                elif operator == '>':
                    self.assembly_code.append(f"sgt {temp}, {left}, {right}")
            return temp
        elif expression['type'] == 'factor' and expression['value'][1] == 'Identificador':
            return expression['value'][0]
        return None

    def is_float_expression(self, expression, tree):
        def check_node(node):
            if 'value' in node and self.get_node_type(node['value'][0], tree) == 'float':
                return True
            if 'left' in node and check_node(node['left']):
                return True
            if 'right' in node and check_node(node['right']):
                return True
            if 'expression' in node and check_node(node['expression']):
                return True
            return False
        return check_node(expression)

    def is_float_comparison(self, comparison_node, tree):
        left_identifier = comparison_node['left'].get('value', [None, None])[0]
        right_identifier = comparison_node['right'].get('value', [None, None])[0]
        left_type = self.get_node_type(left_identifier, tree)
        right_type = self.get_node_type(right_identifier, tree)
        return left_type == 'float' or right_type == 'float'

    def translate_node(self, node, tree):
        if node['type'] == 'assignment':
            identifier = node['identifier'][0]
            expression = self.translate_expression(node['expression'], tree)
            data_type = self.get_node_type(identifier, tree)
            if data_type == 'string' and expression.startswith('"'):
                value = expression.strip('"')
                for i, char in enumerate(value):
                    temp = self.new_temp()
                    self.assembly_code.append(f"li {temp}, {ord(char)}")
                    self.assembly_code.append(f"sb {temp}, {identifier}+{i}")
                temp_null = self.new_temp()
                self.assembly_code.append(f"li {temp_null}, 0")
                self.assembly_code.append(f"sb {temp_null}, {identifier}+{len(value)}")
            elif data_type == 'float':
                self.assembly_code.append(f"s.s {expression}, {identifier}")
            else:
                self.assembly_code.append(f"sw {expression}, {identifier}")
        elif node['type'] == 'declaration':
            pass  # Ya se maneja en generate_data_section
        elif node['type'] == 'while':
            start_label = self.new_label()
            end_label = self.new_label()
            self.assembly_code.append(f"{start_label}:")
            left_expr = {'type': 'factor', 'value': [node['condition']['left']['value'][0], self.get_node_type(node['condition']['left']['value'][0], tree) == 'float' and 'Flotante' or 'Entero']}
            right_expr = {'type': 'factor', 'value': [node['condition']['right']['value'][0], node['condition']['right']['value'][1]]}
            comparison = {'type': 'comparison_operation', 'operator': node['condition']['operator'], 'left': left_expr, 'right': right_expr}
            condition_temp = self.translate_expression(comparison, tree)
            self.assembly_code.append(f"beqz {condition_temp}, {end_label}")
            for statement in node['body']:
                self.translate_node(statement, tree)
            self.assembly_code.append(f"j {start_label}")
            self.assembly_code.append(f"{end_label}:")
        elif node['type'] == 'if':
            condition_temp = self.translate_expression(node['condition'], tree)
            else_label = self.new_label()
            end_label = self.new_label()
            self.assembly_code.append(f"beqz {condition_temp}, {else_label}")
            for statement in node['body']:
                self.translate_node(statement, tree)
            self.assembly_code.append(f"j {end_label}")
            self.assembly_code.append(f"{else_label}:")
            if 'else_body' in node:
                for statement in node['else_body']:
                    self.translate_node(statement, tree)
            self.assembly_code.append(f"{end_label}:")
        elif node['type'] == 'for':
            self.translate_node(node['initialization'], tree)
            start_label = self.new_label()
            end_label = self.new_label()
            self.assembly_code.append(f"{start_label}:")
            condition_temp = self.translate_expression(node['condition'], tree)
            self.assembly_code.append(f"beqz {condition_temp}, {end_label}")
            for statement in node['body']:
                self.translate_node(statement, tree)
            self.translate_node(node['increment'], tree)
            self.assembly_code.append(f"j {start_label}")
            self.assembly_code.append(f"{end_label}:")
        elif node['type'] == 'increment_decrement':
            identifier = node['identifier'][0]
            operator = node['operator'][0]
            data_type = self.get_node_type(identifier, tree)
            increment_value = 1
            if operator == '++':
                instruction = "addi" if data_type != 'float' else "add.s"
            elif operator == '--':
                instruction = "subi" if data_type != 'float' else "sub.s"

            if data_type != 'float':
                temp = self.new_temp()
                self.assembly_code.append(f"{instruction} {identifier}, {identifier}, {increment_value}")
            else:
                temp_one = self.new_temp_float()
                self.assembly_code.append(f"li.s {temp_one}, 1.0")
                self.assembly_code.append(f"{instruction} {identifier}, {identifier}, {temp_one}")
        elif node['type'] == 'comparison_operation' and \
             node['left'].get('value') and node['left']['value'][1] == 'Identificador' and \
             self.get_node_type(node['left']['value'][0], tree) == 'string' and \
             node['right'].get('value') and node['right']['value'][1] == 'Cadena':
            left_identifier = node['left']['value'][0]
            right_string = node['right']['value'][0].strip('"')
            operator = node['operator'][0]
            result_temp = self.new_temp()
            label_start = self.new_label()
            label_equal = self.new_label()
            label_not_equal = self.new_label()
            label_continue = self.new_label()
            index_temp = self.new_temp()
            char1_temp = self.new_temp()
            char2_temp = self.new_temp()

            self.assembly_code.append(f"li {index_temp}, 0")
            self.assembly_code.append(f"{label_start}:")
            self.assembly_code.append(f"lb {char1_temp}, {left_identifier}({index_temp})")
            if right_string:
                char_to_compare = ord(right_string[0]) if len(right_string) > 0 else 0
                right_string_remaining = right_string[1:]
                self.assembly_code.append(f"li {char2_temp}, {char_to_compare}")
            else:
                self.assembly_code.append(f"li {char2_temp}, 0")
                right_string_remaining = ""

            if operator == '==':
                self.assembly_code.append(f"bne {char1_temp}, {char2_temp}, {label_not_equal}")
                self.assembly_code.append(f"beqz {char1_temp}, {label_equal}") # Both null, strings are equal
                self.assembly_code.append(f"addi {index_temp}, {index_temp}, 1")
                # Re-evaluate right_string (simplified for this example)
                # A more robust solution would involve a loop and indexing for the right string
                if right_string_remaining:
                    # In a real scenario, you'd continue comparing character by character
                    # For this example, we'll just check the first char and then assume equality or inequality
                    if not right_string_remaining and char1_temp == 0:
                        self.assembly_code.append(f"j {label_equal}")
                    elif right_string_remaining and char1_temp == 0:
                        self.assembly_code.append(f"j {label_not_equal}")
                    elif not right_string_remaining and char1_temp != 0:
                        self.assembly_code.append(f"j {label_not_equal}")
                    else:
                        # For simplicity, if there's remaining in right and left isn't null, assume not equal
                        self.assembly_code.append(f"j {label_not_equal}")
            else:
                # Left string ended, right might have more characters
                self.assembly_code.append(f"bnez {char2_temp}, {label_not_equal}")
                self.assembly_code.append(f"j {label_equal}")

            self.assembly_code.append(f"{label_equal}:")
            self.assembly_code.append(f"li {result_temp}, 1")
            self.assembly_code.append(f"j {self.new_label()}") # Jump to end

            self.assembly_code.append(f"{label_not_equal}:")
            self.assembly_code.append(f"li {result_temp}, 0")
            # No jump to end here, let it fall through

            end_comparison = self.new_label()
            self.assembly_code.append(f"{end_comparison}:")

            return result_temp
    
        elif node['type'] == 'comparison_operation':
            left = self.translate_expression(node['left'], tree)
            right = self.translate_expression(node['right'], tree)
            operator = node['operator'][0]
            temp = self.new_temp()
            is_float = self.is_float_comparison(node, tree)
            float_suffix = ".s" if is_float else ""
            if operator == '==':
                self.assembly_code.append(f"seq{float_suffix} {temp}, {left}, {right}")
            elif operator == '<=':
                self.assembly_code.append(f"sle{float_suffix} {temp}, {left}, {right}")
            elif operator == '>=':
                self.assembly_code.append(f"sge{float_suffix} {temp}, {left}, {right}")
            elif operator == '<':
                self.assembly_code.append(f"slt{float_suffix} {temp}, {left}, {right}")
            elif operator == '>':
                self.assembly_code.append(f"sgt{float_suffix} {temp}, {left}, {right}")
            return temp
        
        elif node['type'] == 'factor' and expression['value'][1] == 'Identificador':
            return expression['value'][0]
        
        return None