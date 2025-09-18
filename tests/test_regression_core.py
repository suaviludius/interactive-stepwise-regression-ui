# tests/test_regression_core.py
import pytest
import numpy as np
import pandas as pd
from pathlib import Path
from src.core.regression_core import StepwiseRegressionEngine

@pytest.fixture
def perfect_linear_data(tmp_path):
    """Создает тестовый Excel файл с идеальной линейной зависимостью Y ~ X1."""
    data = {
        'X1': [1, 2, 3, 4, 4],
        'X2': [5, 23, 3, 2, 1],  # Отрицательная корреляция с X1
        'X3': [2, 3, 7, 33, 6],  # Слабая корреляция с Y
        'Y': [2.1, 4.2, 6.3, 8.4, 10.5]  # Y ~= 2.1 * X1
    }
    df = pd.DataFrame(data)
    test_file = tmp_path / "test_data_perfect.xlsx"
    df.to_excel(test_file, sheet_name='Лист1', index=False, engine='openpyxl')
    return str(test_file)

def test_full_backward_elimination_flow(perfect_linear_data):
    """
    Интеграционный тест, проверяющий полный цикл обратного исключения.
    Шаги: 1) Инициализация, 2) Заполнение таблицы, 3) Многократное исключение.
    Проверяет, что итоговая модель содержит только значимые предикторы.
    """
    # 1. ARRANGE: Подготовка
    engine = StepwiseRegressionEngine(perfect_linear_data, Sheet=1)
    engine.readExel(ColumnsY=1)
    engine.Const_R2 = 0.5  # Устанавливаем низкий порог для демонстрации

    # 2. ACT: Действие - выполняем полный цикл обратного исключения
    # Начинаем со всей модели
    engine.filledTable()
    initial_r2 = engine.R2
    initial_predictors_count = engine.ColumnsX

    # Запускаем алгоритм, пока он не остановится сам
    # (пока R2 > Const_R2 и есть что исключать)
    steps_taken = 0
    max_steps = engine.ColumnsX  # Защита от бесконечного цикла

    while (engine.R2 > engine.Const_R2 and
           len(engine.IndX_ADD) > 1 and
           steps_taken < max_steps):
        engine.DELXK()
        steps_taken += 1

    # 3. ASSERT: Проверяем результаты
    # Убедимся, что алгоритм сделал хотя бы один шаг
    assert steps_taken > 0, "Алгоритм не выполнил ни одного шага исключения"
    # R2 итоговой модели должен быть выше порогового значения
    assert engine.R2 > engine.Const_R2
    # Количество предикторов должно уменьшиться
    assert engine.ColumnsX < initial_predictors_count
    # Списки добавленных/удаленных предикторов должны быть согласованы
    assert len(engine.IndX_ADD) + len(engine.IndX_DEL) == initial_predictors_count
    # Для нашего идеального набора данных ожидаем, что в модели останется только X1
    # (engine.IndX_ADD должен содержать индекс столбца X1, который равен 0)
    assert 0 in engine.IndX_ADD
    # ...а X2 и X3 должны быть удалены (их индексы 1 и 2 - в списке удаленных)
    assert 1 in engine.IndX_DEL
    assert 2 in engine.IndX_DEL

    # Дополнительно: проверяем, что массивы истории изменились
    assert len(engine.R2_DEL) == steps_taken
    # R2 на каждом шаге не должен был катастрофически падать
    # (в идеале должен монотонно убывать, но это не всегда строгое правило)
    assert all(r2 <= initial_r2 for r2 in engine.R2_DEL)
