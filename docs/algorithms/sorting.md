# Простые сортировки

Разберём три способа отсортировать изменяемую последовательность на месте. Во всех примерах порядок задаётся сравнением: Python принимает `key` и `reverse`, C++ — `comp` и `proj`.

Python-алгоритмы вычисляют `key` один раз на элемент. Для этого хранится параллельный массив ключей, поэтому при переданном `key` дополнительная память составляет O(n); без `key` алгоритм работает с исходными значениями напрямую.

## Bubble Sort

На каждом проходе сравниваем соседние элементы и меняем их местами, если соседняя пара нарушает нужный порядок. Самый большой по выбранному порядку элемент проходит к концу неотсортированной части. Если проход не сделал обменов, последовательность уже упорядочена.

Стабильность сохраняется, потому что меняются местами только строго неправильно упорядоченные соседние элементы.

После каждого прохода наибольший элемент неотсортированной части оказывается на её последней позиции. Поэтому уже обработанный суффикс отсортирован и может быть исключён из следующего прохода; проход без обменов означает, что отсортирована вся последовательность.

```{literalinclude} ../../impl/python/src/algorithms/sorting/bubble_sort/bubble_sort.py
:language: python
:caption: impl/python/src/algorithms/sorting/bubble_sort/bubble_sort.py
```

```{literalinclude} ../../impl/cpp/src/algorithms/sorting/bubble_sort/bubble_sort.cppm
:language: cpp
:caption: impl/cpp/src/algorithms/sorting/bubble_sort/bubble_sort.cppm
```

В Python тесты: `impl/python/tests/algorithms/sorting/bubble_sort/test_bubble_sort.py`. В C++: `impl/cpp/tests/algorithms/sorting/bubble_sort/test_bubble_sort.cpp`.

- Время: лучший случай O(n), худший O(n²).
- Дополнительная память: O(1) в C++ и в Python без `key`; O(n) для Python-кэша `key`.

## Insertion Sort

Поддерживаем отсортированный префикс. Берём следующий элемент и двигаем его влево, пока предыдущий элемент должен находиться после него. Равные элементы не пересекаются, поэтому алгоритм стабилен.

Перед каждой итерацией префикс до текущей позиции отсортирован. Сдвиги сохраняют порядок его элементов, а остановка на первом элементе, который не должен идти после вставляемого, помещает новый элемент в правильную позицию и сохраняет инвариант.

```{literalinclude} ../../impl/python/src/algorithms/sorting/insertion_sort/insertion_sort.py
:language: python
:caption: impl/python/src/algorithms/sorting/insertion_sort/insertion_sort.py
```

```{literalinclude} ../../impl/cpp/src/algorithms/sorting/insertion_sort/insertion_sort.cppm
:language: cpp
:caption: impl/cpp/src/algorithms/sorting/insertion_sort/insertion_sort.cppm
```

В Python тесты: `impl/python/tests/algorithms/sorting/insertion_sort/test_insertion_sort.py`. В C++: `impl/cpp/tests/algorithms/sorting/insertion_sort/test_insertion_sort.cpp`.

- Время: лучший случай O(n), средний и худший O(n²).
- Дополнительная память: O(1) в C++ и в Python без `key`; O(n) для Python-кэша `key`.

## Selection Sort

На позиции i находим наименьший элемент оставшегося суффикса и меняем его местами с элементом на позиции i. Число сравнений почти не зависит от начального порядка: каждый проход просматривает весь суффикс.

Selection Sort не является стабильной сортировкой: дальний обмен может поменять относительный порядок равных элементов.

Перед каждой итерацией префикс содержит минимальные элементы всей последовательности в правильном порядке. Поиск минимума в суффиксе и обмен с его первым элементом расширяют этот префикс на один элемент.

```{literalinclude} ../../impl/python/src/algorithms/sorting/selection_sort/selection_sort.py
:language: python
:caption: impl/python/src/algorithms/sorting/selection_sort/selection_sort.py
```

```{literalinclude} ../../impl/cpp/src/algorithms/sorting/selection_sort/selection_sort.cppm
:language: cpp
:caption: impl/cpp/src/algorithms/sorting/selection_sort/selection_sort.cppm
```

В Python тесты: `impl/python/tests/algorithms/sorting/selection_sort/test_selection_sort.py`. В C++: `impl/cpp/tests/algorithms/sorting/selection_sort/test_selection_sort.cpp`.

- Время: Θ(n²) сравнений в лучшем, среднем и худшем случаях.
- Обмены: не более n − 1.
- Дополнительная память: O(1) в C++ и в Python без `key`; O(n) для Python-кэша `key`.
