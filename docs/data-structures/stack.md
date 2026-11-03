# Стек: варианты реализации

## Задача

Храните значения так, чтобы последним извлекалось последнее добавленное.

:::{container} task-facts

**Вход.** push(1), push(2), peek(), pop().

**Результат.** peek() и pop() возвращают 2; в стеке остаётся 1.

:::

**Предусловия.** При $n=0$ peek/pop вызывают IndexError; элемент может иметь произвольный тип.

### Проверка

Запустите пример: утверждения фиксируют ожидаемое поведение.

```python
from data_structures.stack import linked_list

stack = linked_list.Stack[int]()
stack.push(1)
stack.push(2)
assert stack.peek() == stack.pop() == 2
assert stack.peek() == 1
```

Структурные контракты: [интерфейсы структур данных](interfaces.md).

Задачи от фиксированного массива до персистентного стека, с условиями и раскрываемыми решениями: [конструирование стеков и очередей](construction.md).

```{literalinclude} ../../src/data_structures/stack/dynamic_array.py
:language: python
:caption: src/data_structures/stack/dynamic_array.py
```

{download}`Скачать исходник <../../src/data_structures/stack/dynamic_array.py>`

```{literalinclude} ../../src/data_structures/stack/linked_list.py
:language: python
:caption: src/data_structures/stack/linked_list.py
```

{download}`Скачать исходник <../../src/data_structures/stack/linked_list.py>`

```{literalinclude} ../../src/data_structures/stack/two_queues.py
:language: python
:caption: src/data_structures/stack/two_queues.py
```

{download}`Скачать исходник <../../src/data_structures/stack/two_queues.py>`

```{literalinclude} ../../src/data_structures/stack/one_queue.py
:language: python
:caption: src/data_structures/stack/one_queue.py
```

{download}`Скачать исходник <../../src/data_structures/stack/one_queue.py>`

## Контракт и корректность

`push(value)` добавляет элемент; `peek()` возвращает последний добавленный; `pop()` удаляет и возвращает его. Размер и пустота: `len(stack)` и `bool(stack)`. При пустом стеке peek/pop вызывают IndexError.

Массив хранит вершину в конце; связная реализация — в начале списка. Две очереди: в spare сначала кладём новый элемент, потом переносим прежние, после чего меняем очереди местами. Одна очередь: после добавления прокручиваем прежние элементы за новый. Инвариант очередных реализаций — вершина стека всегда в голове очереди; поэтому pop/peek просты.

| Версия | push | pop | Память и компромисс |
|---|---|---|---|
| dynamic_array.Stack | амортизированное O(1), рост O(n) | амортизированное O(1) | O(n), компактное размещение |
| linked_list.Stack | O(1) | O(1) | O(n), отдельная аллокация узла |
| two_queues.Stack | O(n) | O(1) | O(n), перенос в spare |
| one_queue.Stack | O(n) | O(1) | O(n), одна очередь вместо двух |

Python list иногда сокращает ёмкость. Очередные реализации используют кольцевую очередь без сокращения буфера. Оптимальный выбор зависит от частоты операций; очередные варианты показывают эквивалентность интерфейсов и дороже прямого стека.

 Тесты сверяют случайные операции с эталонным LIFO-контейнером и проверяют пустой доступ.
