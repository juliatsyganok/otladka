### Ошибка 1: Ошибка границы цикла (off-by-one)

**Место**: bugs/1.py:14

**Симптом**: При вызове ls(['-1', 'test_directory']) выводится содержимое 
текущей директории вместо test_directory

**Как воспроизвести**:
1. Запустить 1.py
2. Программа создаст test_directory/
3. Вызовет ls(['-1', 'test_directory'])

**Отладка**:
- Breakpoint на строке 14
- В панели Variables наблюдаем:
  - args = ['-1', 'test_directory']
  - len(args) = 2
  - range(len(args)-1) = range(1)
  - Только одна итерация цикла (i=0)
  - Обрабатывается только '-1', 'test_directory' игнорируется

**Скриншоты**:
<img width="521" height="492" alt="image" src="https://github.com/user-attachments/assets/643f4d45-8511-4936-b5d7-b3578a81bd9b" />
<img width="759" height="401" alt="image" src="https://github.com/user-attachments/assets/36cb1759-0852-4751-8481-ec32045aaf9b" />

**Исправление**:
# Было:
for i in range(len(args) - 1):

# Стало:
for i in range(len(args)):

**Доказательство**
<img width="694" height="278" alt="image" src="https://github.com/user-attachments/assets/fa40163e-bccc-471b-a45b-b212cd41f843" />







### Ошибка 2: Неверное логическое условие

**Место**: bugs/1.py:29

**Симптом**: 
- При вызове ls([]) выводится детальная информация
- При вызове ls(['-1']) также выводится детальная информация
- Нет различия между режимами вывода

**Как воспроизвести**:
1. Запустить 1.py
2. Вызвать ls([]) - должны быть только имена
3. Вызвать ls(['-1']) - должна быть детальная информация

**Отладка**:
- Breakpoint 1 на строке 16
- Breakpoint 2 на строке 29 
- Наблюдаем:
  - При ls([]): f = False, но условие len(items) > 0 = True
  - При ls(['-1']): f = True, условие len(items) > 0 = True
  - В обоих случаях выполняется ветка детального вывода

**Скриншоты**:
<img width="840" height="682" alt="image" src="https://github.com/user-attachments/assets/7bd12b5b-7c81-47db-be9c-6a605bda6b27" />
<img width="2672" height="808" alt="image" src="https://github.com/user-attachments/assets/b4cd2852-a32c-4b87-9198-5a23185e97a6" />

**Причина**: Использовано неверное условие. Вместо проверки флага проверяется наличие файлов.

**Исправление**:
# Было:
if len(items) > 0:

# Стало:
if f:

**Доказательство**
<img width="781" height="698" alt="image" src="https://github.com/user-attachments/assets/d4cf0dde-8ada-4589-8c8a-02bddd0ffa49" />



### Ошибка 3: Сравнение через `is` вместо `==`

**Место**: bugs/1.py:37

**Симптом**: 
- Директории не помечаются как "DIR"
- Все файлы выводятся одинаково, независимо от типа
- В выводе нет ожидаемых пометок "DIR" для каталогов

**Как воспроизвести**:
1. Запустить 1.py
2. Вызвать ls(['-1']) в директории с подкаталогами
3. Наблюдать отсутствие пометок "DIR" у директорий

**Отладка**:
- Breakpoint 1 на строке 34 (получение permissions)
- Breakpoint 2 на строке 37 (сравнение)
- Наблюдаем в Debug Console:
  >>> permissions = "drwxr-xr-x"
  >>> permissions == "drwxr-xr-x"
  True
  >>> permissions is "drwxr-xr-x"
  False  # или иногда True из-за интернирования строк
  >>> id(permissions)
  1402456789456
  >>> id("drwxr-xr-x")
  1402456789424
  >>>
**Скриншоты**:
<img width="717" height="331" alt="image" src="https://github.com/user-attachments/assets/1da17110-34b1-4387-bee6-f49b008576ab" />

**Причина**: Оператор is проверяет, являются ли два объекта одним и тем же объектом в памяти
Оператор == проверяет равенство значений
Строки, созданные разными способами, могут иметь одинаковое значение, но быть разными объектами

# Было:
if permissions is "drwxr-xr-x":

# Стало:
if permissions == "drwxr-xr-x":


### Ошибка 4: Изменение коллекции во время итерации

**Место**: bugs/1.py:46-49

**Симптом**: 
- Удаление элементов из списка `items` во время итерации
- Хотя итерация идёт по копии, изменение исходного списка нарушает логику программы
- Если бы итерация шла по `items` напрямую, получили бы RuntimeError

**Как воспроизвести**:
1. Запустить 1.py
2. Программа создаст test_directory/ с файлом data.tmp
3. В процессе работы функция попытается удалить .tmp файлы из списка items

**Отладка**:
- Breakpoint 1 (строка 46): наблюдение создания копии списка
- Breakpoint 2 (строка 47): начало итерации по temp_items
- Breakpoint 3 (строка 49): удаление элемента из items

**Наблюдения в отладчике**:
1. temp_items = items[:] создаёт поверхностную копию
2. id(items) != id(temp_items) - разные объекты
3. При items.remove(item) исходный список изменяется
4. temp_items остаётся неизменным
5. После цикла items содержит меньше элементов

**Скриншоты**:
<img width="669" height="242" alt="image" src="https://github.com/user-attachments/assets/bceda2c8-cae2-4493-ba80-e72141b44c40" />
<img width="2482" height="579" alt="image" src="https://github.com/user-attachments/assets/744e49b9-dee6-4e4a-ade0-1c08123696bb" />


**Причина**: 
1. Изменение коллекции во время итерации
2. Даже при итерации по копии, изменение оригинала нарушает логику
3. Может привести к ошибкам, если позже код ожидает определённое состояние items

**Исправление**:

Удалить после итерации (если нужно сохранить items)
to_remove = []
for item in items:
    if item.name.endswith('.tmp'):
        to_remove.append(item)
for item in to_remove:
    items.remove(item)



### Ошибка 5: Использование изменяемого значения по умолчанию

**Место**: bugs/1.py:52

**Симптом**: 
- Функция count_files_by_type вызывается дважды
- Первый вызов: {'files': 2, 'dirs': 5}
- Второй вызов: {'files': 4, 'dirs': 10} (значения удвоились!)
- Счётчик накапливает значения между вызовами

**Как воспроизвести**:
1. Запустить ls_with_bugs.py
2. Функция ls вызовет count_files_by_type два раза
3. Наблюдать нарастание значений в выводе

**Отладка**:
- Breakpoint 1: определение функции (строка 52)
- Breakpoint 2: первый вызов (строка 60)
- Breakpoint 3: второй вызов (строка 62)
- Breakpoint 4: изменение counter (строка 55)

**Наблюдения в отладчике**:
1. При определении функции создаётся словарь counter
2. id(counter) = 1402456789456
3. Первый вызов: counter начинает с {'files': 0, 'dirs': 0}
4. После первого вызова: counter = {'files': 2, 'dirs': 5}
5. Второй вызов: id(counter) = 1402456789456
6. counter начиается не с нулей, а с {'files': 2, 'dirs': 5}
7. Результат: stats1 is stats2 = True

**Скриншоты**:
<img width="508" height="55" alt="image" src="https://github.com/user-attachments/assets/3a579adc-4971-4056-87f9-84ae699e666a" />
<img width="2229" height="680" alt="image" src="https://github.com/user-attachments/assets/079fd9f7-309e-44fe-97fb-30adc94ed494" />
<img width="2195" height="617" alt="image" src="https://github.com/user-attachments/assets/039cf912-2617-4a46-80ed-3d560e7005ae" />


**Причина**: 
- Значения по умолчанию в Python вычисляются один раз при определении функции
- Все вызовы функции получают ссылку на один и тот же объект
- Изменяемые объекты (списки, словари) сохраняют изменения между вызовами

**Исправление**:
# Было:
def count_files_by_type(file_list, counter={"files": 0, "dirs": 0}):

# Стало:
def count_files_by_type(file_list, counter=None):
    if counter is None:
        counter = {"files": 0, "dirs": 0}
