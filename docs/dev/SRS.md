# Спецификация требований к программному обеспечению

## Введение

### Терминология

- *Документ* - текстовый файл, содержащий набор символов, предназначенный для
  хранения и передачи информации.

- *Группа документов (репозиторий)* - множество документов, объединенных по
  некоторому признаку.

- *Объект [сравнения]* - пользовательский документ или множество документов,
  который(-ые) подлежит(-ат) оценке на схожесть.

### Назначение

Назначение программного обеспечени - это, в первую очередь, оценка схожести
двух текстовых объектов в процентном эквиваленте. Оценка схожести документов
должна включать в себя семантичский анализ содержимого. В частности, для
программ должны учитываться следующие потенциальные модификации: добавление
комментариев, переименовывание переменных, переопределение порядка объявления
синтаксических единиц.

### Примеры работы программы

#### Примитивные примеры

```
muskox@dev:~$ echo "print(21 * 2)" > a.py
muskox@dev:~$ echo "print(42)" > b.py
muskox@dev:~$ muskox local a.py b.py
1.0

muskox@dev~$ mkdir a/
muskox@dev~$ echo "print(42)" > a/a.py
muskox@dev~$ echo "print(42)" > b.py
muskox@dev:~$ muskox local a/ b.py
1.0

muskox@dev~$ mkdir a/
muskox@dev~$ echo "a = 42; print(a)" > a/a.py
muskox@dev~$ mkdir b/
muskox@dev~$ echo "print(42)" > b/b.py
muskox@dev:~$ muskox local a/ b/
1.0

muskox@dev~$ echo "print(42)  # 42" > a.py
muskox@dev~$ echo "print(1 * 2 * 21)" > b.py
muskox@dev:~$ muskox local a.py b.py
1.0
```

#### Более комплексные примеры

1. Пример первый.

```python
# Файл: a.py

from math import sqrt


def av(m: list) -> int:
    av_mean = 0
    for i in range(len(m)):
        av_mean += m[i]
    av_mean /= len(m)
    return av_mean


m = [float(i) for i in input().split()]

av_mean = av(m)
av_mean_sqrt = sqrt(av_mean)

for i in range(0, len(m), 3):
    m[i] = av_mean_sqrt


d = dict()

for i in m:
    if i not in d:
        d[i] = 0
    d[i] += 1

for key, item in d.items():
    print(f"Элемент {key} в количестве:", {item})
```

```python
# Файл: b.py

from math import sqrt

def func(m: list) -> int:
    a = 0
    for i in range(0, len(m), 1):
        a += m[i]
    a /= len(m)
    return a
m = [float(i) for i in input().split()]
w = func(m)
ws = sqrt(w)

for i in range(0, len(m), 3):
    m[i] = ws

d = dict()
for i in m:
    if i not in d:
        d[i] = 0
    d[i] += 1

if 1 == 0:
    x = 2
    for i in range(10):
        x += 1
    if x == -1:
        print(x)

for key, item in d.items():
    print(f"Элемент {key} в количестве: {item}")
```

```console
muskox@dev:~$ muskox local a.py b.py
1.0
```

2. Пример второй.

```python
a = [int(i) for i in input().split()]

for i in range(0, len(a), 2):
    del a[i]

print(a)
```

```python
b = [int(i) for i in input().split()]

if len(b) == -1:
    x = 2

#удаляем
for i in range(0, len(a), 2):
    del a[i]

print(f"{a}")
```

```console
muskox@dev:~$ muskox local a.py b.py
1.0
```

## Обзор системы

### Пользовательский интерфейс

#### Консольный интерфейс

##### Общий интерфейс

Один из интерфейсов программного обеспечения для внешнего пользователя - это
консольный интерфейс. Предполагается, что после установки программного
обеспечения пользователь сможет запускать программу через оболочку терминала.
Например, `Bash` или `PowerShell`.

Пример возможного интерфейса программы:

```console
muskox@dev:~$ muskox --help
Usage: muskox [-h] [-v] {local,remote} ...

Options:
  -h, --help      display the usage guide and exit
  -v, --version   display the version and exit

Commands:
  local           select the local filesystem
  remote          select the remote filesystem
```

##### Выбор файловой системы

При этом пользователь должен уметь указывать через консольный интерфейс, какой
тип файловой системы должен быть использован - локальный или удаленный. Второй
случай предполагает предварительное скачивание удаленно расположенных файлов в
локальную систему, а после - выполнить локальное сравнение.

Пример возможного интерфейса программы для локальной файловой системы:

```console
muskox@dev:~$ muskox local --help
Usage: muskox local [-h] [-t N] PATH PATH

Positional Arguments:
  PATH             the path to the first object
  PATH             the path to the second object

options:
  -h, --help       display the usage guide and exit
  -t, --threads N  limit the number of threads used
```

Пример возможного интерфейса программы для удаленной файловой системы:

```console
muskox@dev:~$ muskox remote --help
Usage: muskox remote [-h] [-t N] URL URL

Positional Arguments:
  URL              the URL to the first object
  URL              the URL to the second object

options:
  -h, --help       display the usage guide and exit
  -t, --threads N  limit the number of threads used
```

##### Выбор используемых метрик

Среди прочего, пользователь должен иметь возможность выбирать метрики, которые
будут использованы при оценке схожести объектов. Выбор должен быть организован
в рамках консольного интерфейса. Должны поддерживаться две возможности:

1. Указать стандартные настройки, которые применяются к каждому запуску, если
   от пользователя не было предписания использовать другие указанные метрики.

```console
muskox@dev:~$ muskox config --help
Usage: muskox config [-h] [-i M] [-e M]

options:
  -h, --help       display the usage guide and exit
  -i, --include M  include the metric to the default list
  -e, --exclude M  exclude the metric from the default list
```

2. Указать используемые метрики в рамках вызова программы.

```console
muskox@dev:~$ muskox local a.txt b.txt --metrics levenshtein
0.72
```

##### Примеры использования

```console
muskox@dev:~$ muskox local a.txt b.txt
0.72

muskox@dev:~$ muskox local a/ b/
0.33

muskox@dev:~$ muskox local a.txt b/
0.91

muskox@dev:~$ export GITHUB=https://github.com
muskox@dev:~$ muskox remote $GITHUB/numpy/numpy $GITHUB/pandas-dev/pandas
0.17

muskox@dev:~$ export GITLAB=https://gitlab.com
muskox@dev:~$ muskox remote $GITLAB/schwabts/pandas $GITHUB/numpy/numpy
0.02
```

#### API

##### Язык программирования

Программное обеспечение должно предоставлять собственное API (возможно,
включая микросервисы) на языке программирования `Python`. Совместимость
достаточно обеспечить для следующих версий языка программирования:

- `3.8`;
- `3.9`;
- `3.10`;
- `3.11`;
- `3.12`.

##### Метрики, оценивающие схожесть документов

Предположительно в модуле `muskox.similarity` должны быть расположены функции,
предназначенные для оценки схожести документов. Функции принимают на вход путь
к файлу или содержимое файла, а возвращают результат оценки. Ниже приведен
пример:

```python
from muskox.similarity import levenshtein


def levenshtein(lh: str | PathLike, rh: str | PathLike) -> float:
    ...


score = levenshtein("print(42)", "print(21 * 2)")
assert score == 1.0
```

Предполагается, что базовый интерфейсе бдует содержать следующие функции:

```python
from muskox.similarity import levenshtein
from muskox.similarity import shingle
from muskox.similarity import hamming
from muskox.similarity import levenshtein
from muskox.similarity import jaro_winkler
from muskox.similarity import damerau_levenshtein
from muskox.similarity import osa
from muskox.similarity import sorensen
from muskox.similarity import ngram
from muskox.similarity import ...
```

##### Алгоритмы сравнения

Ввиду наличия метрик, основанных на алгоритмах, требуется наличие реализации
самих алгоритмов в чистом виде. Они должны выполнять строго ту логику, которая
им свойственна. Пример:

```python
def levenshtein(lh: str, rh: str) -> int:
    ...


cost = levenshtein("abc", "acd")
assert cost == 2
```

Пример интерфейса модуля (пакета), в котором будут расположены функции:

```python
from muskox.algorithms import levenshtein
from muskox.algorithms import shingle
from muskox.algorithms import hamming
from muskox.algorithms import levenshtein
from muskox.algorithms import jaro_winkler
from muskox.algorithms import damerau_levenshtein
from muskox.algorithms import osa
from muskox.algorithms import sorensen
from muskox.algorithms import ngram
from muskox.algorithms import ...
```

##### Скачивание удаленных репозиториев

Обработка удаленных репозиториев предполагает их скачивание на локальное
устройство, а уже после начало работы с их содержимым. По этой причине в
проект требуется добавить функционал скачивания. Компоненту можно выделить
в отдельный подсервис, который не зависит от текущей программы, либо выделить
как отдельный модуль (пакет). Ниже приведены примеры:

```python
from muskox.web.github import download
from muskox.web.gitlab import download
from muskox.web.bitbucket import download
from muskox.web.gitflic import download
...
```

Предполагается, что функция `download` принимает на вход имя пользователя и
требуемый репозиторий, а возвращает путь к скачанному репозиторию на локальном
устройстве.

```python
def download(user: str, repo: str) -> pathlib.Path:
    ...
```

##### Обработка абстрактного синтаксического дерева

Для предобработки текста должны использоваться абстрактные синтаксические
деревья. Минимальная реализация должна поддерживать синтаксис следующих языков
программирования и систем сборки:

- `Bazel`
- `Python`
- `Starlark`

При этом основной упор делается на язык программирования `Python`. Для работы
с ним требуется организовать серию функций, обрабатывающих код и возвращающие
их измененные версии. Ниже приведены примеры:

```python
from muskox.ast.python import remove_asserts
from muskox.ast.python import remove_comments
from muskox.ast.python import remove_docstrings
from muskox.ast.python import remove_type_hints
from muskox.ast.python import remove_unreachable
from muskox.ast.python import ...

from muskox.ast.bash import ...
from muskox.ast.bazel import ...
from muskox.ast.c import ...
from muskox.ast.cmake import ...
from muskox.ast.cpp import ...
from muskox.ast.css import ...
from muskox.ast.docker import ...
from muskox.ast.go import ...
from muskox.ast.html import ...
from muskox.ast.java import ...
from muskox.ast.jupyter import ...
from muskox.ast.markdown import ...
from muskox.ast.php import ...
from muskox.ast.python import ...
from muskox.ast.rust import ...
from muskox.ast.starlark import ...
from muskox.ast.sql import ...
from muskox.ast.txt import ...
```

### Входные и выходные данные

#### Входные данные

Программа в формате консольного интерфейса принимает на вход одну из трех
следующих сущностей:

- URL-адрес;
- Путь к документу, или путь к файлу;
- Путь к группе документов, или путь к директории.

В случае URL-адреса это должен быть валидный веб-адрес, указывающий на
некоторый репозиторий на поддерживаемой платформе для удаленного хостинга
проектов. К ним, например, относятся, `GitHub` и `BitBucket`.

Пример валидного URL:
```
https://github.com/numpy/numpy
```

Путь к документу или к группе файлов аналогичным образом должен являться
корректным путем к локально размещенным файловым данным.

Примеры валидных путей:
```
~/Desktop/HSE/muskox/
~/Desktop/HSE/muskox/example.txt
```

#### Выходные данные

Выходное значение - строго одно число, принадлежащее отрезку от `0` до `1`.
Конечное число показывает процент схожести двух объектов сравнения.

Пример выходного значения:
```
0.03
```

### Микросервисы

Как уже было упомянуто, допустимо разделение некоторых составляющих проекта
на отдельные независимые компоненты. К ним можно, например, отнести, работу
с удаленными репозиториями или реализацию алгоритмов сравнения строк.

В таком случае каждая подобная компонента должна быть доступна к установке
через пакетный менеджер `pip`. Например, если выделить скачивание удаленных
репозиториев в микросервис под названием `GitLoad`, то его установка должна
быть возможна следующим способом:

```console
muskox@dev:~$ pip install gitload
```

## Технические требования

### Операционные системы

Должны поддерживаться следующие операционные системы:

- `Windows`;
- `macOS`;
- `Linux`;
- `Ubuntu`.

### Языки программирования

- `Python` - Основной язык, на котором ведется разработка. Предполагается
  поддержка следующих версий: `3.8 - 3.12`;

- `C` - Минорный язык, который будет использован как расширение `Python` с
  целью ускорения работы алгоритмов обработки текста;

- `C++` - Аналогично `C`. Предполагается использование любого из стандартов:
  `C++17`, `C++20`, `C++23`.

### Системы сборки

Допускается использование системы сборки:

- `Bazel` - быстрое и эффективное решение от компании Google. Сочетает в
  себе предельно простой синтаксис и алгоритмы кэширования для ускорения
  повторных сборок проекта. Кроме того, идеально подходит для
  кроссплатформенных приложений.

### Компиляторы

- Для операционной системы `Windows` предполагается использование компилятора
  `Microsoft Visual C++ (MSVC)`. Для данной ОС это самое надежное решение.

- Компиляторы `clang` и `g++` - на `Linux` и `macOS` подойдет любой из этих
  двух компиляторов.

## Стандартизация

### Линтеры

Все компоненты программы, не считая внешних зависимостей, не являющихся
микросервисами программного обеспечения должны отвечать требованиям
следующих линтеров:

- `flake8`;
- `pylint`;
- `yamllint`;
- `markdownlint`;
- `cpplint`.

### Санитайзеры

Все компоненты программы, не считая внешних зависимостей, не являющихся
микросервисами программного обеспечения должны отвечать требованиям
следующих санитайзеров:

- `TSAN`;
- `UBSAN`;
- `ASAN`.

### Установка

Конечный продукт должен быть опубликован на `PyPI`, а значит, должен быть
доступен к установке через интерфейс менеджера пакетов `pip`:

```console
muskox@dev:~$ pip install muskox
```
