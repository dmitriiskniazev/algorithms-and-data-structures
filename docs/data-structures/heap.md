# Бинарная куча и priority queue

## Задача

Поддерживайте значение с наивысшим приоритетом в корне кучи; выберите минимум или максимум отдельным модулем.

:::{container} task-facts

**Вход.** Значения 3, 1 и 2 в priority_queue.minimum.

**Результат.** Очередь извлекает 1, 2, 3.

:::

**Предусловия.** Значения задают строгий слабый порядок через `<`; пустой доступ вызывает IndexError.

### Проверка

Запустите пример: утверждения фиксируют ожидаемое поведение.

```python
from data_structures.priority_queue import minimum

queue = minimum.PriorityQueue[int]()
for value in [3, 1, 2]:
    queue.push(value)
assert [queue.pop(), queue.pop(), queue.pop()] == [1, 2, 3]
```

Структурные контракты: [интерфейсы структур данных](interfaces.md).

```{literalinclude} ../../src/data_structures/heap/_sift_down.py
:language: python
:pyobject: sift_down
:caption: heap.sift_down
```

```{literalinclude} ../../src/data_structures/heap/_sift_up.py
:language: python
:pyobject: sift_up
:caption: heap.sift_up
```

```{literalinclude} ../../src/data_structures/heap/_build.py
:language: python
:pyobject: build
:caption: heap.build
```

{download}`build <../../src/data_structures/heap/_build.py>`, {download}`sift_down <../../src/data_structures/heap/_sift_down.py>`, {download}`sift_up <../../src/data_structures/heap/_sift_up.py>`

```{literalinclude} ../../src/data_structures/priority_queue/minimum.py
:language: python
:caption: priority_queue.minimum.PriorityQueue
```

```{literalinclude} ../../src/data_structures/priority_queue/maximum.py
:language: python
:caption: priority_queue.maximum.PriorityQueue
```

{download}`Минимум <../../src/data_structures/priority_queue/minimum.py>`, {download}`максимум <../../src/data_structures/priority_queue/maximum.py>`

## Куча на переданном хранилище

Бинарная куча хранится без узлов: для индекса i дети — 2i+1 и 2i+2, родитель — (i−1)//2. `sift_down` исправляет путь от корня вниз; `sift_up` — от добавленного листа к корню. После выбора более приоритетного ребёнка и обмена единственное возможное нарушение остаётся ниже по этому пути. `heap.build` применяет просеивание к внутренним узлам снизу вверх.

Низкоуровневая куча — max-heap: для каждого ребёнка выполняется `not parent < child`. Операции работают непосредственно с `values`. Просеивания получают индексы корректного полуинтервала; heap.build обрабатывает весь массив. Индексы должны принадлежать рабочему хранилищу.

## Очередь с приоритетом

`priority_queue.minimum.PriorityQueue` извлекает минимум, `priority_queue.maximum.PriorityQueue` — максимум. Обе версии используют только `<` на значениях; он задаёт строгий слабый порядок. Максимальная очередь переиспользует операции max-heap. Порядок эквивалентных элементов не гарантирован.

`push` вставляет в конец и просеивает вверх. `pop` сохраняет корень, переносит последний элемент в корень и просеивает вниз. `peek` не меняет очередь. Пустой просмотр/извлечение вызывает IndexError.

| Операция | Время |
|---|---|
| sift_up / sift_down | O(log n) |
| heap.build bottom-up | O(n) |
| push priority queue | амортизированное O(log n), отдельный рост O(n) |
| pop priority queue | амортизированное O(log n), сокращение list может копировать O(n) |
| peek | O(1) |

Python list может сокращать ёмкость при удалении. Хранение O(n); очередь хранит сами значения.

Тесты: {download}`очереди с приоритетом <../../tests/data_structures/test_priority_queue.py>`; свойства кучи также проверяются через HeapSort.

Предусловия: sift_up получает добавленный лист, предшествующий префикс уже является кучей; sift_down получает корень, чьи поддеревья уже являются кучами. root/child принадлежат [0,right), ключи при наличии имеют длину values; heap.build принимает произвольное хранилище.
