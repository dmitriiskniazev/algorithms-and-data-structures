# Порядковые статистики и медиана

## Задача

Найдите элемент заданного ранга, не сортируя остальные элементы без необходимости.

:::{container} task-facts

**Вход.** [8, 1, 7, 2], ранг k=1 от нуля.

**Результат.** Элемент 2; центральная пара для этого входа — (2, 7).

:::

**Предусловия.** $0\le k<n$; значения сравниваются через `<`.

### Проверка

Запустите пример: утверждения фиксируют ожидаемое поведение.

```python
from algorithms.selection import median, order_statistic

assert order_statistic.iterative([8, 1, 7, 2], 1) == 2
assert median.find([8, 1, 7, 2]) == (2, 7)
```

```{literalinclude} ../../src/algorithms/selection/order_statistic/_by_sorting.py
:language: python
:caption: src/algorithms/selection/order_statistic/_by_sorting.py
```

{download}`Скачать исходник <../../src/algorithms/selection/order_statistic/_by_sorting.py>`

Общий выбор ранга переиспользуется итеративным вариантом и медианой:

```{literalinclude} ../../src/algorithms/selection/_select_rank.py
:language: python
:pyobject: select_rank
```

```{literalinclude} ../../src/algorithms/selection/order_statistic/_iterative.py
:language: python
:caption: src/algorithms/selection/order_statistic/_iterative.py
```

{download}`Скачать исходник <../../src/algorithms/selection/order_statistic/_iterative.py>`

```{literalinclude} ../../src/algorithms/selection/order_statistic/_recursive.py
:language: python
:caption: src/algorithms/selection/order_statistic/_recursive.py
```

{download}`Скачать исходник <../../src/algorithms/selection/order_statistic/_recursive.py>`

```{literalinclude} ../../src/algorithms/selection/median.py
:language: python
:caption: src/algorithms/selection/median.py
```

{download}`Скачать исходник <../../src/algorithms/selection/median.py>`

## Контракт

Ранг `k` нумеруется с нуля. Функции переставляют вход, не гарантируя сортировку остальных элементов. Python возвращает элемент. Недопустимый ранг и пустая медиана: `IndexError`.

`median` возвращает пару исходных элементов рангов `(n−1)//2` и `n//2`. Для `[1,2,7,8]` это `(2,7)`, для `[1,2,7]` — `(2,2)`. Это не арифметическое среднее. Ранги определяются прямым `<` на значениях; он должен задавать строгий слабый порядок.

## Идея и корректность

QuickSelect использует то же [разбиение](quick-sort.md), что QuickSort. После разделения ранги левой части меньше границы блока равных pivot. Если `k` внутри блока, ответ найден; иначе продолжаем только в части, содержащей ранг. Инвариант: искомый ранг всегда остаётся внутри рабочей части. Для медианы найдём оба центральных ранга, сохранив первое значение до последующих перестановок.

## Версии

| Версия | Время | Рабочая память |
|---|---|---|
| `order_statistic.by_sorting` — базовая через HeapSort | O(n log n) в худшем случае | O(1) |
| `order_statistic.recursive` — рекурсивная | ожидаемое O(n), худшее O(n²) | ожидаемо O(log n), худшее O(n) |
| `order_statistic.iterative` | ожидаемое O(n), худшее O(n²) | O(1) |
| `median` — два центральных ранга | ожидаемое O(n), худшее O(n²) | O(1) |

Процедура `_search` получает ранг и границы явно. Два поиска всё ещё линейны в ожидании: сумма двух O(n) — O(n). Детерминированная линейная worst-case гарантия здесь не заявлена. Рекурсивный вариант учебный; итеративный исключает риск лимита стека.

Тесты: `tests/algorithms/selection/`.
