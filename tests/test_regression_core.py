# tests/test_regression_exact_excel.py
import pytest
import numpy as np
import pandas as pd
from pathlib import Path
from src.core.regression_core import StepwiseRegressionEngine

# Путь к тестовому файлу
TEST_EXCEL_PATH = Path(__file__).parent / "test_data" / "regression_test_data.xlsx"

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
    engine = StepwiseRegressionEngine(str(TEST_EXCEL_PATH), sheet=1)
    engine.readExel(ColumnsY=1)
    return engine

def test_matrix_multiplication(excel_engine):
    """Тестирует умножение матриц X'X и X'Y."""
    engine = excel_engine
    engine.filledTable()

    # Читаем ожидаемые значения из Excel
    expected_xtx = read_range_values('Расчет', 'A29', 'K39')  # Матрица X'X
    expected_xty = read_range_values('Расчет', 'A41', 'A51')  # Вектор X'Y

    # Рассчитываем фактически
    X1 = np.column_stack((np.ones((engine.Lines, 1)), engine.X))
    actual_xtx = np.dot(X1.T, X1).flatten()
    actual_xty = np.dot(X1.T, engine.Y[:, engine.Ynum])

    # Сравниваем
    np.testing.assert_allclose(actual_xtx, expected_xtx, rtol=1e-10)
    np.testing.assert_allclose(actual_xty, expected_xty, rtol=1e-10)

def test_regression_coefficients(excel_engine):
    """Тестирует коэффициенты регрессии."""
    engine = excel_engine
    engine.filledTable()
    engine.VKR()

    # Читаем ожидаемые коэффициенты из Excel (вектор оценок)
    expected_coeffs = read_range_values('Расчет', 'A53', 'A63')

    # Сравниваем
    np.testing.assert_allclose(engine.REE, expected_coeffs, rtol=1e-5)

def test_r_squared(excel_engine):
    """Тестирует R-квадрат."""
    engine = excel_engine
    engine.filledTable()
    engine.VKR()
    engine.APUR()

    # Читаем R² из Excel
    expected_r2 = read_cell_value('Расчет', 'B97')  # Ячейка R2

    assert abs(engine.R2 - expected_r2) < 1e-10

def test_f_statistic(excel_engine):
    """Тестирует F-статистику."""
    engine = excel_engine
    engine.filledTable()
    engine.VKR()
    engine.APUR()

    # Читаем F-статистику из Excel
    expected_f = read_cell_value('Расчет', 'B99')  # Ячейка F

    assert abs(engine.FSKF - expected_f) < 1e-5

def test_residuals(excel_engine):
    """Тестирует остатки регрессии."""
    engine = excel_engine
    engine.filledTable()
    engine.VKR()
    engine.APUR()

    # Читаем Y(x) из Excel (столбец Y(x))
    expected_y_pred = read_range_values('Расчет', 'H2', 'H27')

    # Сравниваем предсказанные значения
    np.testing.assert_allclose(engine.Y_REE, expected_y_pred, rtol=1e-5)