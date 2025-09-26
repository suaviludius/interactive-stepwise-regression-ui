# tests/test_regression_exact_excel.py
import pytest
import numpy as np
import pandas as pd
from pathlib import Path
from src.core.regression_core import StepwiseRegressionEngine

# Путь к тестовому файлу
TEST_EXCEL_PATH = Path(__file__).parent / "regression_test_data.xlsx"

def read_cell_value(sheet_name, cell_address):
    """Читает значение из конкретной ячейки Excel."""
    df = pd.read_excel(TEST_EXCEL_PATH, sheet_name=sheet_name, header=None)
    # Конвертируем адрес ячейки в координаты (например, "A1" -> (0,0))
    col_letter = ''.join(filter(str.isalpha, cell_address))
    row_num = int(''.join(filter(str.isdigit, cell_address))) - 1

    # Конвертируем букву столбца в номер
    col_num = 0
    for char in col_letter:
        col_num = col_num * 26 + (ord(char.upper()) - ord('A') + 1)
    col_num -= 1

    return df.iloc[row_num, col_num]

def read_range_values(sheet_name, start_cell, end_cell):
    """Читает диапазон значений из Excel."""
    df = pd.read_excel(TEST_EXCEL_PATH, sheet_name=sheet_name, header=None)

    # Конвертируем адреса ячеек в координаты
    start_col_letter = ''.join(filter(str.isalpha, start_cell))
    start_row = int(''.join(filter(str.isdigit, start_cell))) - 1
    end_col_letter = ''.join(filter(str.isalpha, end_cell))
    end_row = int(''.join(filter(str.isdigit, end_cell))) - 1

    def letter_to_number(letter):
        num = 0
        for char in letter:
            num = num * 26 + (ord(char.upper()) - ord('A') + 1)
        return num - 1

    start_col = letter_to_number(start_col_letter)
    end_col = letter_to_number(end_col_letter)

    # Извлекаем значения
    values = df.iloc[start_row:end_row+1, start_col:end_col+1].values
    return values.flatten()  # Преобразуем в 1D массив

@pytest.fixture
def excel_engine():
    """Создает движок регрессии из данных на первом листе."""
    engine = StepwiseRegressionEngine(str(TEST_EXCEL_PATH), Sheet=1)
    engine.readExel(ColumnsY=1)
    return engine

def test_matrix_multiplication(excel_engine):
    """Тестирует перенос данных."""
    engine = excel_engine
    engine.filledTable()

    # Читаем ожидаемые значения из Excel
    expected_x = read_range_values('Расчет', 'B2', 'K27')  # Матрица X
    expected_y = read_range_values('Расчет', 'L2', 'L27')  # Матрица Y

    # Сравниваем
    np.testing.assert_allclose(engine.X.flatten(), expected_x.astype(float), rtol=1e-10)
    np.testing.assert_allclose(engine.Y.flatten(), expected_y.astype(float), rtol=1e-10)

def test_regression_coefficients(excel_engine):
    """Тестирует коэффициенты регрессии."""
    engine = excel_engine
    engine.filledTable()
    engine.VKR()

    # Читаем ожидаемые коэффициенты из Excel (вектор оценок)
    expected_coeffs = read_range_values('Расчет', 'A53', 'A63')

    # Сравниваем
    np.testing.assert_allclose(engine.REE, expected_coeffs.astype(float), rtol=1e-5)

def test_r_squared(excel_engine):
    """Тестирует R-квадрат."""
    engine = excel_engine
    engine.filledTable()
    engine.VKR()
    engine.APUR()

    # Читаем R² из Excel
    expected_r2 = read_cell_value('Расчет', 'B102')  # Ячейка R2

    # Относительная погрешность
    np.testing.assert_allclose(engine.R2, expected_r2.astype(float), rtol=1e-3)

def test_f_statistic(excel_engine):
    """Тестирует F-статистику."""
    engine = excel_engine
    engine.filledTable()
    engine.VKR()
    engine.APUR()

    # Читаем F-статистику из Excel
    expected_f = read_cell_value('Расчет', 'B105')  # Ячейка F

    # Относительная погрешностьы
    np.testing.assert_allclose(engine.FSKF, expected_f.astype(float), rtol=1e-3)

def test_residuals(excel_engine):
    """Тестирует кэффициенты эластичности."""
    engine = excel_engine
    engine.filledTable()
    engine.VKR()
    engine.APUR()

    # Читаем частные коэффициенты эластичности из Excel (столбец E)
    expected_pac = read_range_values('Расчет', 'B109', 'B118')

    # Сравниваем предсказанные значения
    np.testing.assert_allclose(engine.PAC, expected_pac.astype(float), rtol=1e-5)