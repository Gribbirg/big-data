## Задание 1

Установить Python, если это не было сделано ранее.


```python
import sys
print(f"Версия Python: {sys.version}")
print(f"Путь к Python: {sys.executable}")
```

    Версия Python: 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)]
    Путь к Python: C:\Users\gribk\PycharmProjects\big-data\.venv\Scripts\python.exe
    

## Задание 2

Написать программу, которая вычисляет площадь фигуры, параметры которой подаются на вход.

**Фигуры:** треугольник, прямоугольник, круг

**Результат:** словарь, где ключ – это название фигуры, а значение – это площадь.


```python
import math

def calculate_areas():
    triangle_base = float(input("Введите основание треугольника: "))
    triangle_height = float(input("Введите высоту треугольника: "))
    rectangle_width = float(input("Введите ширину прямоугольника: "))
    rectangle_height = float(input("Введите высоту прямоугольника: "))
    circle_radius = float(input("Введите радиус круга: "))
    
    areas = {
        'треугольник': 0.5 * triangle_base * triangle_height,
        'прямоугольник': rectangle_width * rectangle_height,
        'круг': math.pi * circle_radius ** 2
    }
    return areas

result = calculate_areas()

print("Площади фигур:")
for shape, area in result.items():
    print(f"{shape}: {area:.2f}")
```

    Площади фигур:
    треугольник: 2740491.00
    прямоугольник: 24642.00
    круг: 39725866.36
    

## Задание 3

Написать программу, которая на вход получает два числа и операцию, которую к ним нужно применить.

**Операции:** 
- `+` (сложение)
- `-` (вычитание)
- `/` (деление)
- `//` (целочисленное деление)
- `abs` (модуль)
- `pow` или `**` (возведение в степень)


```python
def calculator():
    num1 = float(input("Введите первое число: "))
    operation = input("Введите операцию (+, -, /, //, abs, pow): ")
    
    if operation != 'abs':
        num2 = float(input("Введите второе число: "))
    else:
        num2 = 0
    
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '/':
        if num2 == 0:
            return "Ошибка: деление на ноль"
        return num1 / num2
    elif operation == '//':
        if num2 == 0:
            return "Ошибка: деление на ноль"
        return num1 // num2
    elif operation == 'abs':
        return abs(num1)
    elif operation in ['pow', '**']:
        return num1 ** num2
    else:
        return "Неизвестная операция"

result = calculator()
print(f"Результат: {result}")
```

    Результат: 4.0
    

## Задание 4

Напишите программу, которая считывает с консоли числа (по одному в строке) до тех пор, пока сумма введённых чисел не будет равна 0 и после этого выводит сумму квадратов всех считанных чисел.


```python
def sum_until_zero():
    numbers = []
    total_sum = 0
    
    print("Вводите числа (программа остановится, когда сумма станет равна 0):")
    
    while total_sum != 0 or len(numbers) == 0:
        try:
            num = float(input("Введите число: "))
            numbers.append(num)
            total_sum += num
            print(f"Текущая сумма: {total_sum}")
        except ValueError:
            print("Пожалуйста, введите корректное число")
    
    sum_of_squares = sum(num ** 2 for num in numbers)
    print(f"Введенные числа: {numbers}")
    print(f"Сумма квадратов всех чисел: {sum_of_squares}")
    
    return sum_of_squares

sum_until_zero()
```

    Вводите числа (программа остановится, когда сумма станет равна 0):
    Текущая сумма: 5.0
    Текущая сумма: 570.0
    Текущая сумма: 903.0
    Текущая сумма: 0.0
    Введенные числа: [5.0, 565.0, 333.0, -903.0]
    Сумма квадратов всех чисел: 1245548.0
    




    1245548.0



## Задание 5

Напишите программу, которая выводит последовательность чисел, длинною N, где каждое число повторяется столько раз, чему оно равно.

**Пример:** если N = 7, то программа должна вывести `1 2 2 3 3 3 4`


```python
def generate_sequence():
    n = int(input("Введите длину последовательности N: "))
    sequence = []
    current_number = 1
    
    while len(sequence) < n:
        for _ in range(current_number):
            if len(sequence) < n:
                sequence.append(current_number)
            else:
                break
        current_number += 1
    
    return sequence

sequence = generate_sequence()
print(*sequence)
```

    1 2 2 3 3 3 4 4 4 4 5 5 5 5 5 6 6 6 6 6 6 7 7 7 7 7 7 7 8 8 8 8 8
    

## Задание 6

Даны два списка:
```python
А = [1, 2, 3, 4, 2, 1, 3, 4, 5, 6, 5, 4, 3, 2]
В = ['a', 'b', 'c', 'c', 'c', 'b', 'a', 'c', 'a', 'a', 'b', 'c', 'b', 'a']
```

Создать словарь, в котором:
- **Ключи** – содержимое списка В
- **Значения** – сумма всех элементов списка А в соответствии с буквой на той же позиции в списке В


```python
def create_dictionary_from_lists(A, B):
    result = {}
    
    for i in range(len(A)):
        letter = B[i]
        number = A[i]
        
        if letter in result:
            result[letter] += number
        else:
            result[letter] = number
    
    return result

A = [1, 2, 3, 4, 2, 1, 3, 4, 5, 6, 5, 4, 3, 2]
B = ['a', 'b', 'c', 'c', 'c', 'b', 'a', 'c', 'a', 'a', 'b', 'c', 'b', 'a']

dictionary = create_dictionary_from_lists(A, B)
print(f"Результат: {dictionary}")
```

    Результат: {'a': 17, 'b': 11, 'c': 17}
    

## Задание 7

Скачать и загрузить данные о стоимости домов в Калифорнии, используя библиотеку sklearn.


```python
from sklearn.datasets import fetch_california_housing
import pandas as pd

california_housing = fetch_california_housing()
data = pd.DataFrame(california_housing.data, columns=california_housing.feature_names)
data['target'] = california_housing.target

print(f"Размер датасета: {data.shape}")
print(f"Названия признаков: {list(california_housing.feature_names)}")
data.head()
```

    Размер датасета: (20640, 9)
    Названия признаков: ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>MedInc</th>
      <th>HouseAge</th>
      <th>AveRooms</th>
      <th>AveBedrms</th>
      <th>Population</th>
      <th>AveOccup</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>target</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>8.3252</td>
      <td>41.0</td>
      <td>6.984127</td>
      <td>1.023810</td>
      <td>322.0</td>
      <td>2.555556</td>
      <td>37.88</td>
      <td>-122.23</td>
      <td>4.526</td>
    </tr>
    <tr>
      <th>1</th>
      <td>8.3014</td>
      <td>21.0</td>
      <td>6.238137</td>
      <td>0.971880</td>
      <td>2401.0</td>
      <td>2.109842</td>
      <td>37.86</td>
      <td>-122.22</td>
      <td>3.585</td>
    </tr>
    <tr>
      <th>2</th>
      <td>7.2574</td>
      <td>52.0</td>
      <td>8.288136</td>
      <td>1.073446</td>
      <td>496.0</td>
      <td>2.802260</td>
      <td>37.85</td>
      <td>-122.24</td>
      <td>3.521</td>
    </tr>
    <tr>
      <th>3</th>
      <td>5.6431</td>
      <td>52.0</td>
      <td>5.817352</td>
      <td>1.073059</td>
      <td>558.0</td>
      <td>2.547945</td>
      <td>37.85</td>
      <td>-122.25</td>
      <td>3.413</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3.8462</td>
      <td>52.0</td>
      <td>6.281853</td>
      <td>1.081081</td>
      <td>565.0</td>
      <td>2.181467</td>
      <td>37.85</td>
      <td>-122.25</td>
      <td>3.422</td>
    </tr>
  </tbody>
</table>
</div>



## Задание 8

Использовать метод `info()`.


```python
data.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 20640 entries, 0 to 20639
    Data columns (total 9 columns):
     #   Column      Non-Null Count  Dtype  
    ---  ------      --------------  -----  
     0   MedInc      20640 non-null  float64
     1   HouseAge    20640 non-null  float64
     2   AveRooms    20640 non-null  float64
     3   AveBedrms   20640 non-null  float64
     4   Population  20640 non-null  float64
     5   AveOccup    20640 non-null  float64
     6   Latitude    20640 non-null  float64
     7   Longitude   20640 non-null  float64
     8   target      20640 non-null  float64
    dtypes: float64(9)
    memory usage: 1.4 MB
    

## Задание 9

Узнать, есть ли пропущенные значения, используя `isna().sum()`.


```python
missing_values = data.isna().sum()
print(missing_values)
print(f"Общее количество пропущенных значений: {missing_values.sum()}")
```

    MedInc        0
    HouseAge      0
    AveRooms      0
    AveBedrms     0
    Population    0
    AveOccup      0
    Latitude      0
    Longitude     0
    target        0
    dtype: int64
    Общее количество пропущенных значений: 0
    

## Задание 10

Вывести записи, где:
- средний возраст домов в районе более 50 лет
- население более 2500 человек

Использовать метод `loc()`.


```python
filtered_data = data.loc[(data['HouseAge'] > 50) & (data['Population'] > 2500)]

print(f"Исходный размер датасета: {data.shape}")
print(f"Размер после фильтрации: {filtered_data.shape}")
filtered_data.head()
```

    Исходный размер датасета: (20640, 9)
    Размер после фильтрации: (13, 9)
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>MedInc</th>
      <th>HouseAge</th>
      <th>AveRooms</th>
      <th>AveBedrms</th>
      <th>Population</th>
      <th>AveOccup</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>target</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>460</th>
      <td>1.4012</td>
      <td>52.0</td>
      <td>3.105714</td>
      <td>1.060000</td>
      <td>3337.0</td>
      <td>9.534286</td>
      <td>37.87</td>
      <td>-122.26</td>
      <td>1.750</td>
    </tr>
    <tr>
      <th>4131</th>
      <td>3.5349</td>
      <td>52.0</td>
      <td>4.646119</td>
      <td>1.047945</td>
      <td>2589.0</td>
      <td>5.910959</td>
      <td>34.13</td>
      <td>-118.20</td>
      <td>1.936</td>
    </tr>
    <tr>
      <th>4440</th>
      <td>2.6806</td>
      <td>52.0</td>
      <td>4.806283</td>
      <td>1.057592</td>
      <td>3062.0</td>
      <td>4.007853</td>
      <td>34.08</td>
      <td>-118.21</td>
      <td>1.530</td>
    </tr>
    <tr>
      <th>5986</th>
      <td>1.8750</td>
      <td>52.0</td>
      <td>4.500000</td>
      <td>1.206349</td>
      <td>2688.0</td>
      <td>21.333333</td>
      <td>34.10</td>
      <td>-117.71</td>
      <td>2.125</td>
    </tr>
    <tr>
      <th>7369</th>
      <td>3.1901</td>
      <td>52.0</td>
      <td>4.730942</td>
      <td>1.017937</td>
      <td>3731.0</td>
      <td>4.182735</td>
      <td>33.97</td>
      <td>-118.21</td>
      <td>1.676</td>
    </tr>
  </tbody>
</table>
</div>



## Задание 11

Узнать максимальное и минимальное значения медианной стоимости дома.


```python
min_price = data['target'].min()
max_price = data['target'].max()

print(f"Минимальная медианная стоимость дома: {min_price:.2f}")
print(f"Максимальная медианная стоимость дома: {max_price:.2f}")
```

    Минимальная медианная стоимость дома: 0.15
    Максимальная медианная стоимость дома: 5.00
    

## Задание 12

Используя метод `apply()`, вывести на экран название признака и его среднее значение.


```python
mean_values = data.apply(lambda x: x.mean())

for feature, mean_val in mean_values.items():
    print(f"{feature}: {mean_val:.4f}")
```

    MedInc: 3.8707
    HouseAge: 28.6395
    AveRooms: 5.4290
    AveBedrms: 1.0967
    Population: 1425.4767
    AveOccup: 3.0707
    Latitude: 35.6319
    Longitude: -119.5697
    target: 2.0686
    

## Задание 1*

Дан текст на английском языке. Необходимо закодировать его с помощью азбуки Морзе.

**Входные данные:** Текст из латинских букв и пробелов

**Выходные данные:** Каждое слово, закодированное азбукой Морзе (по одному слову на строку, между буквами один пробел)


```python
def morse_encoder():
    morze = {
        'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 
        'f': '..-.', 'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 
        'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.', 'o': '---', 
        'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 
        'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 
        'y': '-.--', 'z': '--..'
    }
    
    text = input("Введите текст на английском языке: ").lower()
    words = text.split()
    
    for word in words:
        morse_word = []
        for char in word:
            if char in morze:
                morse_word.append(morze[char])
        print(' '.join(morse_word))

morse_encoder()
```

    .. --. -. .. - .. --- -.
    ... . --.- ..- . -. -.-. .
    ... - .- .-. -
    

## Задание 2*

В некотором городе открывается новая служба по доставке электронных писем. Необходимо наладить систему регистрации новых пользователей.

**Алгоритм работы:**
1. Если имя не существует в базе → добавляем его и возвращаем "OK"
2. Если имя уже существует → формируем новое имя добавлением числа (name1, name2, ...)

**Входные данные:** 
- Первая строка: число n (1 ≤ n ≤ 100000)
- Следующие n строк: запросы имен (до 32 символов, только строчные латинские буквы)

**Выходные данные:** n строк с ответами ("OK" или предложенное имя)


```python
def registration_system():
    n = int(input("Введите количество запросов: "))
    database = set()
    name_counters = {}
    
    for _ in range(n):
        name = input("Введите имя: ").strip()
        
        if name not in database:
            database.add(name)
            print("OK")
        else:
            if name not in name_counters:
                name_counters[name] = 1
            else:
                name_counters[name] += 1
            
            new_name = f"{name}{name_counters[name]}"
            database.add(new_name)
            print(new_name)

registration_system()
```

    OK
    b1
    b2
    

## Задание 3*

Создать программу обработки запросов пользователей к файловой системе компьютера.

**Действия над файлами:**
- `w` ("write") – запись
- `r` ("read") – чтение  
- `x` ("execute") – запуск

**Входные данные:**
- Число n – количество файлов
- n строк: имя файла и допустимые действия
- Число m – количество запросов
- m строк: "операция файл"

**Выходные данные:** "OK" или "Access denied"


```python
def file_system():
    n = int(input("Введите количество файлов: "))
    file_permissions = {}
    
    for _ in range(n):
        line = input("Введите имя файла и права доступа: ").strip().split()
        filename = line[0]
        if len(line) > 1:
            permissions = line[1:]
        else:
            permissions = []
        file_permissions[filename] = set(permissions)
    
    m = int(input("Введите количество запросов: "))
    
    operation_map = {
        'read': 'r',
        'write': 'w', 
        'execute': 'x'
    }
    
    for _ in range(m):
        request = input("Введите операцию и файл: ").strip().split()
        operation = request[0]
        filename = request[1]
        
        required_permission = operation_map.get(operation)
        
        if filename in file_permissions and required_permission in file_permissions[filename]:
            print("OK")
        else:
            print("Access denied")

file_system()
```

    Access denied
    OK
    OK
    OK
    OK
    
