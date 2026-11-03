# Бинарный поиск: границы и варианты

## Задача

Найдите границы всех элементов, эквивалентных цели, в отсортированной последовательности.

:::{container} task-facts

**Вход.** [1, 2, 2, 5], цель 2.

**Результат.** Полуинтервал [1, 3); нижняя граница 1, верхняя 3.

:::

**Предусловия.** Последовательность упорядочена по `<`; доступ по индексу занимает $O(1)$.

### Проверка

Запустите пример: утверждения фиксируют ожидаемое поведение.

```python
from algorithms.searching import binary_search

values = [1, 2, 2, 5]
assert binary_search.equal_range(values, 2) == (1, 3)
```

Семейство находится в `algorithms.searching.binary_search`. Сначала выбирается операция, затем её реализация. Каждая реализация находится в собственном файле; `__init__.py` экспортирует функции для публичного импорта.

## Постановка задачи

**Задача.** Дана последовательность $a=(a_0,\ldots,a_{n-1})$, упорядоченная по возрастанию, и цель $x$ того же типа. Требуется найти позиции

$$
\begin{aligned}
L &= \min\bigl(\{i\in\{0,\ldots,n-1\}\mid \neg(a_i<x)\}\cup\{n\}\bigr),\\
R &= \min\bigl(\{i\in\{0,\ldots,n-1\}\mid x<a_i\}\cup\{n\}\bigr).
\end{aligned}
$$

**Предусловия:** конечная последовательность с доступом по индексу за $O(1)$; значения и цель принадлежат одному строгому слабому порядку; последовательность упорядочена по этому порядку. Сравнения выполняются напрямую через `<`. Порядок и значения входа во время поиска не меняются.

Для чисел это первая позиция с $a_i\ge x$ и первая позиция с $a_i>x$. Результат каждой границы принадлежит $[0,n]$; $n$ означает конец последовательности, а не индекс элемента. На пустом входе обе границы равны $0$.

| Операция | Результат |
|---|---|
| `lower_bound(a, x)` | $L$: первая позиция со значением не меньше $x$ |
| `upper_bound(a, x)` | $R$: первая позиция со значением строго больше $x$ |
| `equal_range(a, x)` | $(L,R)$: полуинтервал совпадений $[L,R)$ |
| `search(a, x)` | $L$, если в нём есть совпадение; иначе `None` |

## Структура и импорт

```text
binary_search/
├── __init__.py
├── lower_bound/
│   ├── __init__.py
│   ├── _iterative.py
│   └── _recursive.py
├── upper_bound/
│   ├── __init__.py
│   ├── _iterative.py
│   └── _recursive.py
├── _equal_range.py
└── _search.py
```

```python
from algorithms.searching import binary_search

values = [1, 2, 2, 2, 5]
assert binary_search.lower_bound.iterative(values, 2) == 1
assert binary_search.lower_bound.recursive(values, 2) == 1
assert binary_search.upper_bound.iterative(values, 2) == 4
assert binary_search.upper_bound.recursive(values, 2) == 4
assert binary_search.equal_range(values, 2) == (1, 4)
assert binary_search.search(values, 4) is None
```

Файлы с `_` внутренние; публичные `iterative` и `recursive` всегда являются функциями. Композиции `equal_range` и `search` используют итеративные границы и сохраняют константную дополнительную память.

Публичный фасад семейства:

```{literalinclude} ../../src/algorithms/searching/binary_search/__init__.py
:language: python
```

## Нижняя граница

`````{tab-set}

````{tab-item} Итерация
:sync: iterative

```{literalinclude} ../../src/algorithms/searching/binary_search/lower_bound/_iterative.py
:language: python
:caption: src/algorithms/searching/binary_search/lower_bound/_iterative.py
```
````

````{tab-item} Рекурсия
:sync: recursive

```{literalinclude} ../../src/algorithms/searching/binary_search/lower_bound/_recursive.py
:language: python
:caption: src/algorithms/searching/binary_search/lower_bound/_recursive.py
```
````
`````

Исходники: {download}`lower_bound.iterative <../../src/algorithms/searching/binary_search/lower_bound/_iterative.py>`, {download}`lower_bound.recursive <../../src/algorithms/searching/binary_search/lower_bound/_recursive.py>`.

**Инвариант:** $0\le \mathrm{left}\le \mathrm{right}\le n$; для всех $i<\mathrm{left}$ выполнено $a_i<x$, для всех $i\ge \mathrm{right}$ — $\neg(a_i<x)$. Неопределёнными остаются позиции полуинтервала $[\mathrm{left},\mathrm{right})$.

Если $b_{mid}<x$, упорядоченность позволяет отбросить весь префикс до `mid` включительно: `left = mid + 1`. Иначе `mid` может быть ответом, поэтому `right = mid`. Инвариант сохраняется. При `left == right` все предыдущие ключи меньше цели, а все последующие не меньше: полученная позиция равна $L$.

## Верхняя граница

`````{tab-set}

````{tab-item} Итерация
:sync: iterative

```{literalinclude} ../../src/algorithms/searching/binary_search/upper_bound/_iterative.py
:language: python
:caption: src/algorithms/searching/binary_search/upper_bound/_iterative.py
```
````

````{tab-item} Рекурсия
:sync: recursive

```{literalinclude} ../../src/algorithms/searching/binary_search/upper_bound/_recursive.py
:language: python
:caption: src/algorithms/searching/binary_search/upper_bound/_recursive.py
```
````
`````

Исходники: {download}`upper_bound.iterative <../../src/algorithms/searching/binary_search/upper_bound/_iterative.py>`, {download}`upper_bound.recursive <../../src/algorithms/searching/binary_search/upper_bound/_recursive.py>`.

**Инвариант:** для всех $i<\mathrm{left}$ выполнено $\neg(x<a_i)$, для всех $i\ge \mathrm{right}$ — $x<a_i$. Если $x<b_{mid}$, ответ не правее `mid`; иначе все позиции до `mid` включительно подходят для левой части. При завершении получаем $R$.

## Итерация и рекурсия

Обе реализации поддерживают те же границы и выполняют те же сравнения. В итеративной версии следующий диапазон задаётся присваиванием, в рекурсивной — вызовом вложенной функции с новыми `left` и `right`. База рекурсии — `left == right`; в ней возвращается позиция границы. Срезы не создаются: все вызовы читают исходную последовательность.

Длина $\mathrm{right}-\mathrm{left}$ строго уменьшается и сокращается хотя бы вдвое. Число сравнений обеих версий — $O(\log(n+1))$. Итерация использует $O(1)$ дополнительной памяти, рекурсия — $O(\log(n+1))$ кадров стека. Ключ вычисляется только у посещённых элементов; полная последовательность ключей не строится.

## Производные операции

`equal_range` составляет ответ из двух итеративных границ:

```{literalinclude} ../../src/algorithms/searching/binary_search/_equal_range.py
:language: python
```

Ключи на $[L,R)$ эквивалентны цели: $\neg(a_i<x)\land\neg(x<a_i)$. Поэтому число совпадений равно $R-L$. Если цель отсутствует, $L=R$ в позиции вставки; для пустого входа возвращается $(0,0)$.

Точный поиск проверяет кандидата итеративной нижней границы по тому же строгому порядку:

```{literalinclude} ../../src/algorithms/searching/binary_search/_search.py
:language: python
```

Для `a = [1, 2, 2, 2, 5]` цель `2` даёт $L=1$, $R=4$, диапазон $(1,4)$ и первое совпадение $1$. Цель `4` даёт диапазон $(4,4)$ и результат точного поиска `None`.

Остальные запросы выводятся из границ: последний элемент строго меньше цели находится в $L-1$ при $L>0$, последний не больше цели — в $R-1$ при $R>0$. `equal_range` и `search` сохраняют $O(\log(n+1))$ сравнений и $O(1)$ дополнительной памяти.

Тесты: {download}`границы и производные операции <../../tests/algorithms/searching/binary_search/test_bounds.py>`.


Композиции: {download}`equal_range <../../src/algorithms/searching/binary_search/_equal_range.py>`, {download}`search <../../src/algorithms/searching/binary_search/_search.py>`.
