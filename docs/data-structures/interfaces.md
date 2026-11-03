# Интерфейсы структур данных

## Задача

Опишите операции контейнера независимо от хранения, сохранив тип его значений.

:::{container} task-facts

**Вход.** Любая изменяемая реализация Stack[int].

**Результат.** Один потребитель работает с динамическим массивом, фиксированным массивом и связным списком.

:::

**Предусловия.** Структурная совместимость проверяет сигнатуры; LIFO/FIFO и сложность требуют отдельного обоснования.

### Проверка

Запустите пример: утверждения фиксируют ожидаемое поведение.

```python
from data_structures import interfaces
from data_structures.stack import dynamic_array

stack: interfaces.Stack[int] = dynamic_array.Stack[int]()
stack.push(7)
assert stack.pop() == 7
```

**Задача.** Описать операции контейнера независимо от хранения. Для стека $S=(a_0,\ldots,a_{n-1})$ при $n>0$:

$$
\operatorname{peek}(S)=a_{n-1},\qquad
\operatorname{push}(S,x)=(a_0,\ldots,a_{n-1},x).
$$

Изменяемый `pop` удаляет вершину и возвращает её значение. Пустые `peek/pop` вызывают `IndexError`. Ёмкость фиксированного стека остаётся ограничением реализации.

## Изменяемые стек и очередь

```{literalinclude} ../../src/data_structures/interfaces/_stack.py
:language: python
```

```{literalinclude} ../../src/data_structures/interfaces/_queue.py
:language: python
```

`Protocol` задаёт форму методов и типы. Реализации подходят структурно: объявлять наследование от протокола не требуется. В параметрах функции используется интерфейс, при создании объекта выбирается реализация:

```python
from data_structures import interfaces
from data_structures.stack import dynamic_array, fixed_array, linked_list


def move_top[T](source: interfaces.Stack[T], target: interfaces.Stack[T]) -> None:
    target.push(source.pop())


for source in [dynamic_array.Stack[int](), linked_list.Stack[int]()]:
    target = fixed_array.Stack[int](capacity=3)
    source.push(7)
    move_top(source, target)
    assert len(source) == 0
    assert target.peek() == 7
```

При достаточной ёмкости назначения перенос сохраняет значение и удаляет ровно одну вершину источника. Его время — сумма стоимости `pop` и `push` выбранных реализаций.

Стек и очередь имеют одинаковую форму методов, но разный порядок извлечения: LIFO и FIFO. Типизатор проверяет сигнатуры; порядок, исключения и сложность проверяются условиями задачи, доказательством и тестами. Та же граница относится к приоритетной очереди.

## Персистентные версии

```{literalinclude} ../../src/data_structures/interfaces/_persistent_stack.py
:language: python
```

```{literalinclude} ../../src/data_structures/interfaces/_persistent_queue.py
:language: python
```

`push/pop` возвращают новую версию, прежняя сохраняется. `Self` обозначает тип версии получателя; при вызове на конкретной реализации результат сохраняет её тип. Поэтому изменяемый и персистентный контейнеры имеют отдельные протоколы.

```python
from data_structures import interfaces
from data_structures.stack import persistent


def add_copy[T](stack: interfaces.PersistentStack[T], value: T) -> interfaces.PersistentStack[T]:
    return stack.push(value)


original = persistent.Stack[int]()
updated = add_copy(original, 7)
assert len(original) == 0
assert updated.peek() == 7
```

## Другие интерфейсы

Все протоколы находятся в `data_structures.interfaces`, каждый в собственном файле. Упорядоченные значения ограничены протоколом {download}`Comparable <../../src/algorithms/comparable.py>` с единственным оператором `<`; ключи отображения — `Hashable`.

| Протокол | Дополнительный контракт и исходник |
|---|---|
| `Deque[T]` | {download}`Два конца <../../src/data_structures/interfaces/_deque.py>` |
| `PriorityQueue[T]` | {download}`Извлечение по приоритету <../../src/data_structures/interfaces/_priority_queue.py>`; варианты minimum/maximum |
| `ExtremaStack[T]` | {download}`Стек с extreme <../../src/data_structures/interfaces/_extrema_stack.py>` |
| `ExtremaQueue[T]` | {download}`FIFO с extreme <../../src/data_structures/interfaces/_extrema_queue.py>` |
| `BinarySearchTree[T]` | {download}`Поиск, вставка, удаление, обходы <../../src/data_structures/interfaces/_binary_search_tree.py>` |
| `HashMap[K, V]` | {download}`Отображение хешируемых ключей <../../src/data_structures/interfaces/_hash_map.py>` |
| `DisjointSetUnion` | {download}`Разбиение множества <../../src/data_structures/interfaces/_disjoint_set_union.py>` |
| `Trie` | {download}`Слова и префиксы <../../src/data_structures/interfaces/_trie.py>` |

Протоколы не описывают внутренние массивы, узлы или конструкторы. `ExtremaStack` расширяет `Stack` методом extreme, а `ExtremaQueue` и `PriorityQueue` — форму операций `Queue`. Runtime-проверки `isinstance` здесь не нужны: статические проверки принимают все реализации курса и отклоняют неверные типы операций и смешение изменяемости с персистентностью.

Проверки типов: {download}`допустимые примеры <../../tests/typing/accepted.py>` и {download}`отклоняемые примеры <../../tests/typing/rejected.py>`. Поведение реализаций проверяется их собственными тестами.
