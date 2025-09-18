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
QScrollBar::add-page, QScrollBar::sub-page{
    background: none;
    border: 1px;
    border-color: white;
}
/* Линия scroll bar */
QScrollBar{
    background: transparent;
    margin: 0;
}
/* Цвет scroll элемента */
QScrollBar::handle{
    margin: 5;
    background: #505A6E;
}
/* Удаление дополнительных кнопок прокрутки vertical scroll */
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
/* Удаление дополнительных кнопок прокрутки horizontal scroll */
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal  {
    width: 0px;
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