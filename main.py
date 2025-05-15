import sys
import os
import json

from module import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.compiler = Compiler()

        self.ui.button_compile.clicked.connect(self.codeCompile)

        self.show()

    @Slot()
    def codeCompile(self):
        self.ui.output_messages.clear()

        code = self.ui.input_code.toPlainText()

        # Analisis lexico
        tokensFound, lexicalErrors = self.compiler.lexicalAnalyser(code)

        if lexicalErrors:
            for i, error in enumerate(lexicalErrors):
                self.showOutputMessage(f'{str(i + 1)}) {error}', QColor(230,25,25))
        else:
            self.showOutputMessage("Lexical analysis completed with no errors", QColor("green"))
            # self.showOutputMessage("Tokens total = " + str(len(tokensFound)), QColor("green"))   


        self.ui.output_table_result.setColumnCount(2)
        self.ui.output_table_result.setRowCount(len(tokensFound))
        self.ui.output_table_result.setHorizontalHeaderLabels(["Lexema", "Token"])

        for pos, (lexema, tokenType, line) in enumerate(tokensFound):
            lexemaWidget = QTableWidgetItem(str(lexema))
            tokenTypeWidget = QTableWidgetItem(str(tokenType))
            
            self.ui.output_table_result.setItem(pos, 0, lexemaWidget)
            self.ui.output_table_result.setItem(pos, 1, tokenTypeWidget)


        # Analisis sintactico
        tree, parseErrors = self.compiler.parser()
        self.ui.output_sintax_analyzer.clear()
        
        if parseErrors:
            self.showOutputMessage(f'{str(1)}) {parseErrors}', QColor(230,25,25))
        else:
            json_tree = json.dumps(tree, indent=4)

            self.ui.output_sintax_analyzer.setPlainText(json_tree)
            self.ui.output_sintax_analyzer.setReadOnly(True)
            self.showOutputMessage("Syntax analysis completed with no errors", QColor("green"))
        
        # Analisis semantico

        semanticErrors = self.compiler.semanticAnalyser()
        self.ui.output_semantic_analyzer.clear()
        self.ui.output_semantic_analyzer.setReadOnly(True)

        if semanticErrors:
            self.ui.output_semantic_analyzer.setPlainText("NO OK")

            for i, error in enumerate(semanticErrors):
                self.showOutputMessage(f'{str(i + 1)}) {error}', QColor(230,25,25))
        else:
            self.ui.output_semantic_analyzer.setPlainText("OK")
            self.showOutputMessage("Semantic analysis completed with no errors", QColor("green"))

    def showOutputMessage(self, text, color):
        cursor = self.ui.output_messages.textCursor()
        cursor.movePosition(QTextCursor.End)

        char_format = QTextCharFormat()
        char_format.setForeground(color)

        cursor.setCharFormat(char_format)
        cursor.insertText(text + "\n")

        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())