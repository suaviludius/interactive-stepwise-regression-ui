# ----------------------------------------------------------
# line regression
#
# (C) 2022 Artem Shishov, SPb, Russia
# Released under GNU Public License (GPL)
# email powerranger1912@gmail.com
# ----------------------------------------------------------

# -- Properties Exel ---------------------------------------
# |-------------------------------------|
# |     Values    |     Restrictions    |
# |-------------------------------------|
# |   ColumnsX    |       [0 - N]       |
# |   ColumnsY    |       [N - V]       |
# |-------------------------------------|

# -- Import ------------------------------------------------
import numpy as np
import pandas as pd
import copy                     # Копирование объекта класса

# -- Class Regression --------------------------------------
class StepwiseRegressionEngine():
    #     Свойства класса (как поля структуры)
    #     % ------------------------------------------------
    #     FileName = 'ИТВП_Лаб1.xlsx' % Имя файла
    #     Sheet                       % Количество страниц
    #     Lines                       % Количество строк      ||      (m)
    #     Columns;                    % Количество столбцов
    #     ColumnsX;                   % Количество Х столбцов ||      (n)
    #     ColumnsY;                   % Количество Y столбцов
    #     X                           % Независимые переменные
    #     Y                           % Зависимые переменные
    #     Index                       % Строка с проверенными индексами X
    #     Index_temporary             % Строка с текущими индексами X
    #     X1                          % Независимые переменные и столб 1
    #     Ynum                        % Текущий номер Y
    #     % ------------------------------------------------
    #     REE                         % Regression equation estimation
    #     RSS                         % Residual Sum of Squares
    #     % ------------------------------------------------
    #     Y_REE                       % Y полученные по уравнению REE
    #     E                           % Несмещенная ошибка
    #     Y_mean                      % Среднее значение Y по столбцу
    #     Y_RMS                       % Среднее квадратичное отклонение по Y
    #     Y_RMS_sum                   % Сумма Y_RMS
    #     Y_Se2                       % Оценка дисперсии
    #     Y_S2                        % Несмещенная оценка дисперсии
    #     Y_S                         % Оценка среднеквадратичного отклонения (стандартная ошибка оценки Y)
    #     PAC                         % Частные коэффиценты эластинчости
    #     K                           % Оценка ковариационной матрицы
    #     R                           % Коэфициент корреляции
    #     R2                          % Коэфициент детерминации
    #     FSKF                        % F-статистическое распределение Фишера (коэфициент статистики)
    #     % ------------------------------------------------
    #     TR2                         % Тестовые значения R2
    #     % ------------------------------------------------
    #     TFSKF                       % Тестовые значения TFSKF
    #     TX                          % Значения Х для использования в методе добавления переменных
    #     TColumnsX                   % Значения уменьшающегшося числа столбов TХ при переносе их в X

    # -- Constant ------------------------------------------
    Const_R2 = 0.98                 # Контрольное значение R2
    Const_FSKF = 11                 # Контрольное значение FSKF

    # -- Variables -----------------------------------------
    Ynum = 0                        # Номер независимой переменной

    # -- Methods -------------------------------------------
    def __init__(self,FileName,Sheet):
        self.FileName = FileName    # Имя файла
        self.Sheet = Sheet          # Количество страниц

    # -- Чтение данных из Exel файла -----------------------
    def readExel(self,ColumnsY):
        xl = pd.ExcelFile(self.FileName)                                    # Загрузка таблицы
        self.dataset = xl.parse('Лист1')                                    # Загрузить лист в DataFrame под именем: dataset
        self.Lines =  self.dataset.shape[0]                                 # Количество строк || (m)
        self.Columns = self.dataset.shape[1]                                # Количество столбцов
        self.ColumnsX = self.Columns - ColumnsY                             # Количество Х столбцов || (n)
        self.ColumnsY = ColumnsY
        self.X = self.dataset.iloc[0:, :self.ColumnsX].values               # Х - матрица признаков
        self.Y = self.dataset.iloc[0:, self.ColumnsX:(self.ColumnsX+self.ColumnsY)].values  # Y - вектор независимых
        self.IndX = list(range(0, self.X.shape[1]))                         # Индексы self.X (0-n)
        self.IndY = list(range(0, self.Y.shape[1]))                         # Индексы self.Y (0-m)
        self.IndX_DEL = []                                                  # Массив с индексами удаленных элементов
        self.IndX_ADD = copy.copy(self.IndX)                                # Массив с индексами добавленных элементов
        self.IndX_DEL_BACKUP = [];                                          # Массив для BACKUP возвратов значений IndX_DEL
        self.IndX_ADD_BACKUP = [];                                          # Массив для BACKUP возвратов значений IndX_ADD

        self.R2_DEL = []                                                    # R2 удаленных элементов
        self.FSKF_ADD = []                                                  # FSKF добавленных элементов

        self.ColumnsX_BUF = copy.copy(self.ColumnsX)                        # Копия количества столбцов X
        self.X_BUF = copy.copy(self.X)                                      # Копия матрицы признаков (для востановления параметров)


    # -- Вектор коэффициентов регрессии --------------------
    def VKR(self):
        # Коэффициенты bi = (X_t * X)^(-1) * X_t * Y
        # Зависимость y(x) = b0 + b1*x1 + b2*x2 + ... + bn*xn + En
        if len(self.X) == 0: return;
        self.X1 = np.column_stack((np.ones((self.Lines, 1)),self.X))  # Х - Добавление столбца c 1 к Х
        X_t = self.X1.T                                         # X_t - Транспонированная матрица Х
        X_m = np.dot(X_t,self.X1)                               # X_t * X - Произведение транспонированной матрицы Х на основную
        Y_c = self.Y[:,self.Ynum]                               # Y - Взятие нужного столбца Y
        Y_m = np.dot(X_t,Y_c)                                   # X_t * Y - Произведение транспонированной матрицы Х на столбец Y
        self.REE = np.dot(np.linalg.inv(X_m),Y_m)               # (X_t * X)^(-1) * X_t * Y - Произведение обратной матрицы. Оценка уравнения регрессии

    # -- Анализ параметров уравнения регрессии -------------
    def APUR(self):
        # -- Находим отклонения от полученных резльтатов
        if len(self.X) == 0: self.R = 0; self.R2 = 0; self.FSKF = 0; return;
        Y_c = self.Y[:,self.Ynum]                   # Взятие нужного столбца Y (в дальнейшем Y_c назван Y)
        self.Y_REE = np.dot(self.X1,self.REE)       # Подставляем Х в уравнение "оценки уравнения регрессии"
        self.E = self.Y_REE-Y_c                     # Ошибка: E = Y_REE - Y
        self.RSS = np.sum(self.E**2)                # Сумма квадратов ошибок(остатков)
        # --- Расчет СКО -----------------------------------
        self.Y_mean = np.average(Y_c)                                   # Среднее значение Y по столбцу
        self.Y_RMS = (Y_c-np.transpose([self.Y_mean]*self.Lines))**2    # Среднее квадратичное отклонение (СКО) по Y
        self.Y_RMS_sum = np.sum(self.Y_RMS)                             # Сумма значений СКО
        # --- Оценки ---------------------------------------
        self.Y_Se2 = np.dot(np.transpose(self.E),self.E)                # ОД:  Y_Se2 = (Y_REE - Y)`*(Y_REE - Y)
        self.Y_S2 = self.Y_Se2/(self.Lines-self.ColumnsX)               # НОД: Y_S2 = Y_Se2/(m - n)
        self.Y_S =  np.sqrt(self.Y_S2)                                  # ОСО: Y_S = sqrt(Y_Se2)
        self.PAC = self.REE[1:] * np.mean(self.X, axis=0)/self.Y_mean   # Частные коэффиценты эластинчости
        # -- Коэффициенты ----------------------------------
        self.R = np.sqrt(1-self.Y_Se2/self.Y_RMS_sum)                   # КК
        self.R2 = self.R**2                                             # КД
        if self.ColumnsX <= 1: self.FSKF = self.R2*(self.Lines-self.ColumnsX)/((1-self.R2)) #КС
        else: self.FSKF = self.R2/(1-self.R2)*(self.Lines-self.ColumnsX-1)/(self.ColumnsX)

    # -- Удаление независимого фактора ---------------------
    def DELX(self,i):
        self.X = np.delete(self.X,[i],1)        # Удаляем столбцец i
        self.ColumnsX -= 1;                     # Кореектируем количество Х столбцов
        self.VKR();                             # Расчет модели с обновленными параметрами
        self.APUR();

    # -- Удаление независимого фактора по коэффициенту ---------------------
    # "Наименее значимой является переменная исключение которой из модели
    #  вызывает наименьшее сокращение коэффициента детерминации R-квадрат."
    def DELXK(self):
        # !! Перед использованием не забыть filledTable !!
        TR2 = [];   # Значения R2 при тестовых удалениях

        # -- Проверка вычислений на копии объекта регресии -----------------
        for i in range(self.ColumnsX):      # Цикл в котором мы пробуем удалять элементы и считать R
            tobj = copy.copy(self);         # Создание копии объекта
            tobj.DELX(i);
            TR2.append(tobj.R2);            # Массив с возможными R2 в случае удаления каждого из элементов

        # -- Контрольное удаление элемента ---------------------------------
        TR2 = abs(TR2 - self.R2);
        TR2Min, TR2MinIdx = min((TR2Min, TR2MinIdx) for (TR2MinIdx, TR2Min) in enumerate(TR2))      # Определение минимального R2 из тестовых удалений
        self.DELXE(TR2MinIdx);

    # -- Удаление независимого фактора по выбору -------------------
    def DELXE(self, i):
        self.inBackup();
        # -- Контрольное добавление элемента (для пустой и не пустой Database)
        self.DELX(i);
        self.R2_DEL.append(self.R2);
        self.IndX_DEL.append(self.IndX_ADD[i]);                                             # Добавляем индекс столбца к матрице удаленных индексов
        self.IndX_ADD.remove(self.IndX_ADD[i]);                                             # Удаляем индекс столбца к матрице добавленных индексов
        self.setFSKF_ADD();

    # -- Добавление независимого фактора ------------------
    def ADDX(self, i):
        if len(self.X) == 0: self.X = copy.copy(self.X_BUF[:,i]);
        else: self.X = np.column_stack((self.X, self.X_BUF[:,i]));      # Добавляем к текущему X тестовый столбик
        self.ColumnsX += 1;                                             # Количество Х столбцов
        self.VKR();
        self.APUR();

    # -- Добавление независимого фактора по коэффициенту -------------------
    # "Лучшим кандидатом на включение в модель будет та переменная,
    #  которая обеспечит наибольшее сокращение квадрата остатков регрессии
    #  или, что эквивалентно, наибольшее значение статистики F-критерия."
    def ADDXK(self):
        # !! Перед использованием не забыть cleanTable !!
        TFSKF = [];     # Значения FSKF при тестовых удалениях
        TR2 = [];       # Значения R2 при тестовых удалениях

        if len(self.IndX_DEL) != 0: # Остались ли элементы на добавление?
            # -- Проверка вычислений на копии объекта регресии -----------------
            for i in self.IndX_DEL[:]:                # Цикл в котором мы пробуем удалять элементы и считать R
                tobj = copy.copy(self);               # Создание копии объекта
                tobj.ADDX(i);
                TFSKF.append(tobj.FSKF);              # Массив с возможными FSKF в случае удаления каждого из элементов
                TR2.append(tobj.R2);                  # Массив с возможными R2 в случае удаления каждого из элементов

            # -- Контрольное добавление элемента (для пустой и не пустой Database)
            TFSKFMax, TFSKFMaxIdx = max((TFSKFMax, TFSKFMaxIdx) for (TFSKFMaxIdx, TFSKFMax) in enumerate(TFSKF)) # Определение максимального FSKF из тестовых удалений
            self.ADDXE(TFSKFMaxIdx)

    # -- Добавление независимого фактора по выбору -------------------
    def ADDXE(self, i):
        self.inBackup();
        # -- Контрольное добавление элемента (для пустой и не пустой Database)
        self.ADDX(self.IndX_DEL[i])
        self.FSKF_ADD.append(self.FSKF)
        self.IndX_ADD.append(self.IndX_DEL[i]);                                             # Добавляем индекс столбца к матрице добавленных индексов
        self.IndX_DEL.remove(self.IndX_DEL[i]);                                             # Удаляем индекс столбца в матрице удаленных индексов
        self.setR2_DEL();

    # -- Удаление всех независимых факторов ---------------------
    def cleanTable(self, delElements = 0):
        self.ColumnsX = 0;
        self.X = [];
        self.IndX_DEL = copy.copy(self.IndX)
        if not(delElements): self.setR2_DEL()
        self.IndX_ADD = []
        self.FSKF_ADD = []
        self.VKR();
        self.APUR();


    # -- Добавление всех независимых факторов -------------------
    def filledTable(self, addElements = 0):
        self.ColumnsX = self.Columns - self.ColumnsY;
        self.X = copy.copy(self.X_BUF);
        self.IndX_ADD = copy.copy(self.IndX)
        self.IndX_DEL = []
        self.R2_DEL = []
        self.VKR();
        self.APUR();

    # -- Подсчет значений R2 по шагам анализа -------------------
    def setR2_DEL(self):
        self.R2_DEL = []                         # Очищаем массив перед заполнением
        tobj = copy.copy(self);                  # КОПИЯ: Создание объекта
        tobj.filledTable(1)                      # КОПИЯ: Заполяем элементами таблицу
        for i in range(len(self.IndX_DEL)):      # КОПИЯ: Цикл поочередного удаления переменных и подсчета нужного значения
            subtractor = 0;                      # Вычитатель
            for e in range(i):
                if(self.IndX_DEL[e] <  self.IndX_DEL[i]): subtractor -=1;
            tobj.DELX(self.IndX_DEL[i] + subtractor);
            self.R2_DEL.append(tobj.R2)

    # -- Подсчет значений FSKF по шагам анализа -------------------
    def setFSKF_ADD(self):
        self.FSKF_ADD = []                       # Очищаем массив перед заполнением
        tobj = copy.copy(self);                  # КОПИЯ: Создание объекта
        tobj.cleanTable(1)                       # КОПИЯ: Очищаем таблицу
        for i in self.IndX_ADD:                  # КОПИЯ: Цикл поочередного добавления переменных и подсчета нужного значения
            tobj.ADDX(i);
            self.FSKF_ADD.append(tobj.FSKF)

    # -- Занесение в БЭКАП -------------------
    def inBackup(self):
        self.IndX_DEL_BACKUP.append(copy.copy(self.IndX_DEL));
        self.IndX_ADD_BACKUP.append(copy.copy(self.IndX_ADD));
        if(len(self.IndX_DEL_BACKUP) > self.Columns-self.ColumnsY):
            del self.IndX_DEL_BACKUP[0]
            del self.IndX_ADD_BACKUP[0]

    # -- Вывод из БЭКАПа -------------------
    def outBackup(self):
        print(f"out [{len(self.IndX_DEL_BACKUP)}-{len(self.IndX_ADD_BACKUP)}]")
        print("Вернули переменную", self.IndX_DEL)
        if(len(self.IndX_DEL_BACKUP) > 0 or len(self.IndX_ADD_BACKUP) > 0):
            if (len(self.IndX_DEL_BACKUP) > 0): self.IndX_DEL = copy.copy(self.IndX_DEL_BACKUP[-1]); self.IndX_DEL_BACKUP.remove(self.IndX_DEL_BACKUP[-1]);
            if (len(self.IndX_ADD_BACKUP) > 0): self.IndX_ADD = copy.copy(self.IndX_ADD_BACKUP[-1]); self.IndX_ADD_BACKUP.remove(self.IndX_ADD_BACKUP[-1]);
            self.setR2_DEL();
            self.setFSKF_ADD();
            self.ColumnsX = 0;
            self.X = [];
            for i in range(len(self.X_BUF[0])):
                if i in self.IndX_ADD:
                    if len(self.X) == 0: self.X = copy.copy(self.X_BUF[:,i]);
                    else: self.X = np.column_stack((self.X,self.X_BUF[:,i]));   # Добавляем к текущему X тестовый столбик
                    self.ColumnsX += 1;                                         # Количество Х столбцов
            self.VKR();
            self.APUR();