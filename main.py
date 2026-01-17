from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                              QLabel, QHBoxLayout, QLineEdit, QListWidget, 
                              QTextEdit, QInputDialog,)
from PyQt5.QtGui import QFont, QIcon

import json
import os

NOTESFILE = "notes_data.json"

if os.path.exists(NOTESFILE):
    with open(NOTESFILE, "r", encoding="utf-8") as file:
        notes_data = json.load(file)
else:
    notes_data = {
        "welcome":{
            "text": "Лоїх",
            "tags": []
        }
    }
    with open(NOTESFILE, "w", encoding="utf-8") as file:
        json.dump(notes_data, file, ensure_ascii=False, indent = 2)

app = QApplication([])
window = QWidget()
window.setWindowTitle("Not Very Smart Notes")
window.resize(1200, 800)
list_notes = QListWidget()
list_notes_label = QLabel("Список заміток")
btn_note_create = QPushButton("Створити замітку")
btn_note_del = QPushButton("Видалити замітку")  
btn_note_save = QPushButton("Зберегти замітку")
field_tag = QLineEdit("")
field_tag.setPlaceholderText("Введіть тег....")
field_text = QTextEdit()
btn_tag_add = QPushButton("Додати тег")
btn_tag_del = QPushButton("Видалити тег")
btn_tag_siorch = QPushButton("Пошук за тегом")
list_tags = QListWidget()
list_tags_label = QLabel("Список тегів")

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)
col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()  
row_1.addWidget(btn_note_create)
row_1.addWidget(btn_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(btn_note_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(btn_tag_add)
row_3.addWidget(btn_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(btn_tag_siorch)
col_2.addLayout(row_3)
col_2.addLayout(row_4)
layout_notes.addLayout(col_1, 2)
layout_notes.addLayout(col_2, 1)
window.setLayout(layout_notes)

icon = QIcon("assets/icon.ico")
window.setWindowIcon(icon)


window.show()




def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes_data[key]["text"])
    list_tags.clear()
    list_tags.addItems(notes_data[key]["tags"])

def add_note():
    note_name, ok = QInputDialog.getText(window, "Додати замітку", "Назва замітки:")
    if ok and note_name.strip() != "":
        notes_data[note_name] = {"text": "", "tags": []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes_data[note_name]["tags"])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes_data[key]["text"] = field_text.toPlainText()
        with open(NOTESFILE, "w", encoding="utf-8") as file:
            json.dump(notes_data, file, ensure_ascii=False, indent = 2)

def delete_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes_data[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes_data)
        with open(NOTESFILE, "w", encoding="utf-8") as file:
            json.dump(notes_data, file, ensure_ascii=False, indent = 2)

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes_data[key]["tags"] and tag.strip() != "":
            notes_data[key]["tags"].append(tag)
            field_tag.clear()
            list_tags.addItem(tag)
            with open(NOTESFILE, "w", encoding="utf-8") as file:
                json.dump(notes_data, file, ensure_ascii=False, indent = 2)
                
def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes_data[key]["tags"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes_data[key]["tags"])
        with open(NOTESFILE, "w", encoding="utf-8") as file:
            json.dump(notes_data, file, ensure_ascii=False, indent = 2)

def search_by_tag():
    tag = field_tag.text()
    if btn_tag_siorch.text() == "Пошук за тегом" and tag:
        notes_filtered = {}
        for note in notes_data:
            if tag in notes_data[note]["tags"]:
                notes_filtered[note] = notes_data[note]
        btn_tag_siorch.setText("Скинути пошук")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    else:
        btn_tag_siorch.setText("Пошук за тегом")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_data)
        field_tag.clear()
        
btn_note_create.clicked.connect(add_note)
btn_note_save.clicked.connect(save_note)
btn_note_del.clicked.connect(delete_note)
btn_tag_add.clicked.connect(add_tag)
btn_tag_del.clicked.connect(del_tag)
btn_tag_siorch.clicked.connect(search_by_tag)

list_notes.itemClicked.connect(show_note)

with open(NOTESFILE, "r", encoding="utf-8") as file:
    notes_data = json.load(file)

list_notes.addItems(notes_data)

app.exec_()



# Test function for merge conflict
def add_two_numbers(a, b):
    return a * b + 2