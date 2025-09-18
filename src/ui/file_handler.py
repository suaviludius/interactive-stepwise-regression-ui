# -------------------------------------------------------
# File work
#
# (C) 2022 Artem Shishov, SPb, Russia
# Released under GNU Public License (GPL)
# email powerranger1912@gmail.com
# -------------------------------------------------------

# -- Import ---------------------------------------------
import os
import shutil
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *

# -- Import Design -------------------------------------------------
from src.ui.styles import StyleSheetScrollBar, StyleSheetMenu  # Дополнительные стили элементов окна

# -- File class -----------------------------------------
class FileHandler():
# -- Methods -------------------------------------------
    def __init__(self, window, tree, model, action1, action2):
        self.window = window    # Window Application
        self.tree = tree        # Tree view
        self.model = model      # File System Model
        self.action1 = action1  # Action for ".xlsx" file extension
        self.action2 = action2  # Action for ".rep" file extension

# -- Создание файлового дерева -----------------------
    def setFT(self, path):
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(path))
        self.tree.setStyleSheet(StyleSheetScrollBar)
        # Прячем ненужные столбцы и заголовки
        self.tree.setHeaderHidden(1)
        self.tree.setColumnHidden (1,1)
        self.tree.setColumnHidden (2,1)
        self.tree.setColumnHidden (3,1)

        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.setCM)

# -- Создание контекстного меню -----------------------
    def setCM(self, point):
        # Получаем путь к выбранному элементу
        index = self.tree.indexAt(point)
        file_path = self.model.filePath(index)

        # Создаем контекстное меню
        context_menu = QMenu()
        context_menu.setStyleSheet(StyleSheetMenu)

        # Действие - Открыть файл
        open_action = QAction("Открыть файл")
        open_action.triggered.connect(lambda: self.openFile(file_path))
        context_menu.addAction(open_action)

        # Действие - Создать файл
        create_action = QAction("Создать файл")
        create_action.triggered.connect(lambda: self.createFile(file_path))
        context_menu.addAction(create_action)

        # Действие - Копировать файл
        copy_action = QAction("Копировать файл")
        copy_action.triggered.connect(lambda: self.copyFile(file_path))
        context_menu.addAction(copy_action)

        # Действие - Переименовать файл
        rename_action = QAction("Переименовать файл")
        rename_action.triggered.connect(lambda: self.renameFile(file_path))
        context_menu.addAction(rename_action)

        # Действие - Удалить файл
        delete_action = QAction("Удалить файл")
        delete_action.triggered.connect(lambda: self.deleteFile(file_path))
        context_menu.addAction(delete_action)

        # Показываем контекстное меню в указанной позиции
        context_menu.exec_(self.tree.mapToGlobal(point))

# -- Команды работы с файлами -----------------------
# [ Открыть файл ]
    def openFile(self, file_path):
        file_extension = ".none"
        file_name, file_extension = os.path.splitext(file_path)
        # Открываем файл
        try:
            if file_extension == ".xlsx":
                self.action1.trigger()   # Генерируем исполнение действия "Анализ" в меню "Окно"
                self.window.MRInit(file_path)
            elif file_extension == ".rep":
                self.action2.trigger()    # Генерируем исполнение действия "Отчет" в меню "Окно"
                self.window.openReport(file_path)
            else: return
        except OSError:
            QMessageBox.critical(self.window, "Ошибка", "Не удалось открыть файл.")

# [ Переименовать файл ]
    def renameFile(self, file_path):
        # Переименовываем файл
        new_file_name, _ = QInputDialog.getText(self.window, "Переименовать файл", "Введите новое имя файла:", text=os.path.basename(file_path))
        if new_file_name:
            new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
            try:
                os.rename(file_path, new_file_path)
            except OSError:
                QMessageBox.critical(self.window, "Ошибка", "Не удалось переименовать файл.")

# [ Удалить файл ]
    def deleteFile(self, file_path):
        # Удаляем файл
        reply = QMessageBox.question(self.window, "Удалить файл", f"Вы действительно хотите удалить файл:\n{file_path}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                os.remove(file_path)
            except OSError:
                QMessageBox.critical(self.window, "Ошибка", "Не удалось удалить файл.")

# [ Создать файл ]
    def createFile(self, parent_dir):
        # Создаем новый файл
        file_name, _ = QInputDialog.getText(self.window, "Создать файл", "Введите имя нового файла:", QLineEdit.Normal, "example.xlsx" )
        if file_name:
            file_path = os.path.join(parent_dir, file_name)
            try:
                file = open(file_path, 'w')
                file.close()
            except OSError:
                QMessageBox.critical(self.window, "Ошибка", "Не удалось создать файл.")

# [ Копировать файл ]
    def copyFile(self, file_path):
        # Копируем файл
        destination_dir = QFileDialog.getExistingDirectory(self.window, "Выберите папку назначения", QtCore.QDir.homePath(), QFileDialog.ShowDirsOnly)
        if destination_dir:
            try:
                shutil.copy(file_path, destination_dir)
            except OSError:
                QMessageBox.critical(self.window, "Ошибка", "Не удалось скопировать файл.")