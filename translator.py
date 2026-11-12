from PyQt5.QtWidgets import (QApplication, QWidget, QTextEdit, QComboBox, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QStackedWidget, QListWidget)
from googletrans import Translator
from PyQt5.QtGui import QFont
from languages import *
from gtts import gTTS
import asyncio
import os


#start van app maken
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
        self.copybutton = QPushButton("Copy to clipboard")
        self.history_button = QPushButton("History")
        self.input_option = QComboBox()
        self.output_option = QComboBox()
        self.speechbutton = QPushButton("Pronounce text")
        self.slow_speechbutton = QPushButton("Pronounce text slowly")

        #dropdown menu's available languages
        self.input_option.addItems(values)
        self.output_option.addItems(values)

        self.title = QLabel("Le Translator")
        self.title.setFont(QFont("Times new Roman", 35))

        self.master_layout = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        col1.addWidget(self.title)
        col1.addWidget(self.input_option)
        col1.addWidget(self.output_option)
        col1.addWidget(self.submit)
        col1.addWidget(self.reset)
        col1.addWidget(self.copybutton)
        col1.addWidget(self.speechbutton)
        col1.addWidget(self.slow_speechbutton)

        col2.addWidget(self.input_box)
        col2.addWidget(self.output_box)
        col2.addWidget(self.reverse_button)
        col2.addWidget(self.history_button)

        self.master_layout.addLayout(col1, 10)
        self.master_layout.addLayout(col2, 90)


        self.setStyleSheet("""
        QWidget {
            background-color: #333;
            color: #4db8db;
        }
        
        QPushButton {
            background-color: #66a3ff;
            color: #333;
            border: 1px solid #632273;
            border-radius: 5px;
            padding: 5px 10px;
            }
            
        QPushButton:hover {
            background-color: #3399ff;
            }
        """)

        # Main screen
        self.translator_screen = QWidget()
        self.translator_screen.setLayout(self.master_layout)

        #history screen
        self.history_screen = QWidget()
        history_layout = QVBoxLayout()
        self.history_title = QLabel("Translation history")
        self.history_title.setFont(QFont("Times new Roman", 25))
        self.history_list = QListWidget()
        self.return_button = QPushButton("Return to translate")

        history_layout.addWidget(self.history_title)
        history_layout.addWidget(self.history_list)
        history_layout.addWidget(self.return_button)
        self.history_screen.setLayout(history_layout)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.translator_screen)
        self.stack.addWidget(self.history_screen)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)




    def settings(self):
        self.setWindowTitle("Translator")
        self.setGeometry(250, 250, 800, 700)

    def button_click(self):
        self.submit.clicked.connect(self.translate_click)
        self.reset.clicked.connect(self.reset_app)
        self.reverse_button.clicked.connect(self.reverse)
        self.copybutton.clicked.connect(self.copy_to_clipboard)
        self.history_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.history_screen))
        self.return_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.translator_screen))
        self.speechbutton.clicked.connect(self.pronounce_text)
        self.slow_speechbutton.clicked.connect(self.slowly_pronounce_text)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_box.toPlainText())

    def pronounce_text(self):
        text = self.output_box.toPlainText()
        language_code = self.output_option.currentText()
        lang = [key for key, value in LANGUAGES.items() if value == language_code][0]
        if text:
            tts = gTTS(text=text, lang = lang, slow=False)
            tts.save("output.mp3")
            os.system("start output.mp3")

    def slowly_pronounce_text(self):
        text = self.output_box.toPlainText()
        language_code = self.output_option.currentText()
        lang = [key for key, value in LANGUAGES.items() if value == language_code][0]
        if text:
            tts = gTTS(text=text, lang=lang, slow=True)
            tts.save("output_slow.mp3")
            os.system("start output_slow.mp3")

    def translate_click(self):
        value_to_key1 = self.output_option.currentText()
        value_to_key2 = self.input_option.currentText()

        key_to_value1 = [key for key, value in LANGUAGES.items() if value == value_to_key1][0]
        key_to_value2 = [key for key, value in LANGUAGES.items() if value == value_to_key2][0]

        print("Destination language:", key_to_value1)
        print("Source language:", key_to_value2)


        self.script = self.translate_text(self.input_box.toPlainText(), key_to_value1, key_to_value2)
        self.output_box.setText(self.script)
        self.history_list.addItem(f"{self.input_box.toPlainText()} ({value_to_key2}) -> {self.script} ({value_to_key1})")

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
