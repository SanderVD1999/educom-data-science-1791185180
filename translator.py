from PyQt5.QtWidgets import (QApplication, QWidget, QTextEdit, QComboBox, QPushButton, QLabel, QHBoxLayout, QVBoxLayout)
from googletrans import Translator
from PyQt5.QtGui import QFont
from languages import *
import asyncio
# maken van app


class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.settings()
        self.button_click()

    def initUI(self):
        self.input_box = QTextEdit()
        self.output_box = QTextEdit()
        self.reverse_button = QPushButton("Reverse")
        self.reset = QPushButton("Reset")
        self.submit = QPushButton("Translate text")
        self.input_option = QComboBox()
        self.output_option = QComboBox()


        self.input_option.addItems(values)
        self.output_option.addItems(values)

        self.title = QLabel("Le Translator")
        self.title.setFont(QFont("Times new Roman", 40))

        self.master_layout = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        col1.addWidget(self.title)
        col1.addWidget(self.input_option)
        col1.addWidget(self.output_option)
        col1.addWidget(self.submit)
        col1.addWidget(self.reset)

        col2.addWidget(self.input_box)
        col2.addWidget(self.output_box)
        col2.addWidget(self.reverse_button)

        self.master_layout.addLayout(col1, 20)
        self.master_layout.addLayout(col2, 80)

        self.setLayout(self.master_layout)

        self.setStyleSheet("""
        QWidget {
            background-color: #333;
            color: #fff;
        }
        
        QPushButton {
            background-color: #66a3ff;
            color: #333;
            border: 1px solid #fff;
            border-radius: 5px;
            padding: 5px 10px;
            }
            
        QPushButton:hover {
            background-color: #3399ff;
            }
        """)



    def settings(self):
        self.setWindowTitle("Translator")
        self.setGeometry(250, 250, 600, 500)

    def button_click(self):
        self.submit.clicked.connect(self.translate_click)
        self.reset.clicked.connect(self.reset_app)
        self.reverse_button.clicked.connect(self.reverse)

    def translate_click(self):
        value_to_key1 = self.output_option.currentText()
        value_to_key2 = self.input_option.currentText()

        key_to_value1 = [key for key, value in LANGUAGES.items() if value == value_to_key1][0]
        key_to_value2 = [key for key, value in LANGUAGES.items() if value == value_to_key2][0]

        print("Destination language:", key_to_value1)
        print("Source language:", key_to_value2)


        self.script = self.translate_text(self.input_box.toPlainText(), key_to_value1, key_to_value2)
        self.output_box.setText(self.script)

    def reset_app(self):
        self.input_box.clear()
        self.output_box.clear()
        self.input_option.setCurrentIndex(0)
        self.output_option.setCurrentIndex(0)

    def translate_text(self, text, dest_taal, src_taal):
        async def do_translate():
            async with Translator() as speaker:
                translation = await speaker.translate(text, dest=dest_taal, src=src_taal)
                print("Input text:", text)
                print("Source language:", src_taal)
                print("Destination language:", dest_taal)
                print("Translated text:", translation.text)
                print("Detected language:", translation.src)
                return translation.text
        return asyncio.run(do_translate())

    def reverse(self):
        s1, l1 = self.input_box.toPlainText(), self.input_option.currentText()
        s2, l2 = self.output_box.toPlainText(), self.output_option.currentText()

        self.input_box.setText(s2)
        self.output_box.setText(s1)

        self.input_option.setCurrentText(l2)
        self.output_option.setCurrentText(l1)


# running the app
if __name__ == "__main__":
    app = QApplication([])
    main = Home()
    main.show()
    app.exec_()
