# Алгоритмы и структуры данных

Учебный курс по алгоритмам и структурам данных. Его порядок и полный состав разделов зафиксированы в [учебном плане](curriculum.md).

```{toctree}
:maxdepth: 1
:caption: Программа курса

curriculum
implementations
```

```{toctree}
:maxdepth: 2
:caption: Алгоритмы

algorithms/analysis
algorithms/sorting
algorithms/binary-search
algorithms/divide-and-conquer
algorithms/graph-traversal
algorithms/strings
algorithms/fibonacci
algorithms/dynamic-programming
algorithms/greedy
algorithms/graph-algorithms
algorithms/complexity
algorithms/quick-sort
algorithms/heap-sort
algorithms/order-statistics
```

```{toctree}
:maxdepth: 2
:caption: Структуры данных

data-structures/interfaces
data-structures/construction
data-structures/heap
data-structures/stack
data-structures/queue-deque
data-structures/extrema
data-structures/trees-and-hashing
```

## Техническая основа

Образец последовательной подачи — [Фибоначчи: от рекурсии к двум переменным](algorithms/fibonacci.md). Принципы оформления и работы с кодом описаны в [руководстве автора](authoring.md).

```{toctree}
:hidden:

authoring
```

- Python 3.15+, зависимости и тесты управляются через `uv`.
- Учебная документация собирается Sphinx из Markdown с MyST.

## Расположение кода

- Python: `src/algorithms/` и `src/data_structures/`; тесты — `tests/`.
- Общая теория и ход курса — `docs/`.

Код на страницах подключается непосредственно из исходников через literalinclude. После правок выполните `make docs`, чтобы обновить собранный HTML. Пустые заглушки не создаются.

## Как читать курс

Откройте тему в каталоге. **Разбор** показывает задачу, проверку и объяснение. **Код** открывает полные файлы: выберите реализацию и второй файл для сравнения. Ссылка на код сохраняет выбор. В **Настройках** доступны темы, шрифты, типографика, номера/отступы/пробелы, перенос, ширина и импорт VS Code. Настройки остаются на устройстве.

Пример выбора: [Фибоначчи — реализации](algorithms/fibonacci.md).

## Команды

```sh
make setup
make test
make docs
```

Собранный сайт находится в `docs/_build/html/`. Локальный просмотр: `uv run python -m http.server 8000 --directory docs/_build/html`, затем `http://localhost:8000`.
