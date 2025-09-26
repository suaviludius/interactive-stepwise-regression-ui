"""
Централизованный модуль стилей для всего приложения.
"""
# -- Таблица -- #
StyleSheetTableDatabase = """
*{
    color: rgb(255, 255, 255);
    background-color: #3e4556;
    border: none;
    margin: 0px;
    font: 75 11pt \"MS Shell Dlg 2\";
}
QTableWidget::item:selected {
	background-color: #3c90a4;
}
QHeaderView::section{
    Background-color:#3e4556;
}
QTableCornerButton::section {
    background-color:'#3e4556';
}
"""

# -- Меню -- #
StyleSheetMenu = """
QMenuBar::item::selected{
    background-color: #505A6E;
}
QMenu{
	background-color: #1f232a;
	color: white;
}
QMenu::item{
	padding: 5px 70px 5px 30px; /* сверху / справа / снизу / слева*/
	border-radius:  2px;
}
QMenu::item::selected{
	background-color: #505A6E;
}
"""

# -- Полоса прокрутки -- #
StyleSheetScrollBar = """
/* Удаление фона до и после scroll элемента */
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
    border: none;
}

/* Основная линия scroll bar */
QScrollBar:vertical, QScrollBar:horizontal {
    background: transparent;
    margin: 0px;
    border: none;
}

/* Цвет scroll элемента в нормальном состоянии */
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    margin: 3px;
    background: #505A6E;
    border-radius: 3px;
}

/* Цвет scroll элемента при наведении */
QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
    background: #60708C;  /* Более светлый оттенок */
    margin: 3px;
    border-radius: 3px;
}

/* Цвет scroll элемента при нажатии */
QScrollBar::handle:vertical:pressed, QScrollBar::handle:horizontal:pressed {
    background: #3c90a4;  /* Акцентный цвет */
    margin: 3px;
    border-radius: 3px;
}

/* Удаление дополнительных кнопок прокрутки vertical scroll */
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
    border: none;
}

/* Удаление дополнительных кнопок прокрутки horizontal scroll */
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
    border: none;
}

/* Дополнительно: стиль для фона всей полосы прокрутки при наведении */
QScrollBar:vertical:hover, QScrollBar:horizontal:hover {
    background: rgba(80, 90, 110, 0.1);  /* Легкий фон при наведении на всю полосу */
}

/* Стиль для углового элемента (пересечение вертикальной и горизонтальной полосы) */
QScrollBar::corner {
    background: transparent;
    border: none;
}
"""

# -- Полоса со статусом -- #
StyleSheetStatusBar = """
*{
    background-color: #2c313c;
    font: 500 9pt;
    padding: 8px;
    color: #8F8F8F;
}
"""
# -- Стиль рамки всего окна -- #
StyleSheetApp = """
/* Панель заголовка */
TitleBar {
    background-color: #2c313c;
}
/* Минимизировать кнопку `Максимальное выключение` Общий фон по умолчанию */
#buttonMinimum,#buttonMaximum,#buttonClose, #buttonMy {
    border: none;
    background-color: #2c313c;
}
/* Выделение */
#buttonMinimum:hover,#buttonMaximum:hover {
    background-color: #525252;
}
#buttonClose:hover {
    color: white;
    background-color: rgb(232, 17, 35);
}
#buttonMy:hover {
    color: white;
    background-color: green;   /* rgb(232, 17, 35) */
}
/* Нажатие мыши */
#buttonMinimum:pressed,#buttonMaximum:pressed {
    background-color: #3c90a4;
}
#buttonClose:pressed {
    color: white;
    background-color: rgb(161, 73, 92);
}
QLabel{
	/*font: 800 9pt;*/
    padding: 8px;
    color: #8F8F8F;
}
"""