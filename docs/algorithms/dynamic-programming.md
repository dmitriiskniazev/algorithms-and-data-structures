# Динамическое программирование

## Задача

Определите состояния, переходы и порядок вычисления; получите оптимум и восстановите один ответ.

:::{container} task-facts

**Вход.** Рюкзак: веса [2, 3], ценности [3, 4], ёмкость 3.

**Результат.** Оптимум 4; выбран предмет с индексом 1.

:::

**Предусловия.** В рюкзаке веса и ёмкость целые неотрицательные; каждый предмет используется не более одного раза. У остальных задач свои условия.

### Проверка

Запустите пример: утверждения фиксируют ожидаемое поведение.

```python
from algorithms.dynamic_programming import knapsack_01

value, indices = knapsack_01.solve([2, 3], [3, 4], 3)
assert value == 4
assert indices == [1]
```

Состояние → переход → порядок вычисления → восстановление. [Введение: Фибоначчи](fibonacci.md).

## Направление переходов: pull и push

Для максимизации на DAG состояний:

$$D[s]=0,\qquad D[v]=\max_{u\to v}\{D[u]+w(u,v)\},\quad v\ne s.$$

- База: $D[s]=0$; остальные состояния — $-\infty$.
- Порядок — топологический: каждый предшественник обработан раньше потомка.
- Для минимизации: $\max\to\min$, $-\infty\to+\infty$.

`````{tab-set}

````{tab-item} Pull: из предшественников

```python
D = {v: -inf for v in states}
D[start] = 0
parent = {start: None}
for v in topological_order:
    for u, weight in incoming[v]:
        if D[u] == -inf:
            continue
        candidate = D[u] + weight
        if candidate > D[v]:
            D[v] = candidate
            parent[v] = u
```
````

````{tab-item} Push: в следующие состояния

```python
D = {v: -inf for v in states}
D[start] = 0
parent = {start: None}
for u in topological_order:
    if D[u] == -inf:
        continue
    for v, weight in outgoing[u]:
        candidate = D[u] + weight
        if candidate > D[v]:
            D[v] = candidate
            parent[v] = u
```
````
`````

Python-подобный псевдокод. В обоих вариантах `parent[v]` записывается при улучшении; равенство сохраняет первый найденный переход. Недостижимые состояния не имеют ответа для восстановления. Время — $\Theta(|V|+|E|)$.

| Стратегия | Что перечисляем | Когда удобно |
|---|---|---|
| Pull | Предшественников текущего состояния | Прямо известна формула состояния |
| Push | Переходы из текущего состояния | Проще перечислить доступные действия |

**Порядок обхода** определяется зависимостями, независимо от pull/push:

- Префиксы: по возрастанию индексов.
- Интервалы: по возрастанию длины.
- Подмножества: по мощности, если переход добавляет элемент.
- Произвольный DAG: топологическая сортировка.
- Рекурсия с мемоизацией: сначала вычислить запрошенные зависимости (pull).

### Сжатие памяти и порядок обновлений

Для 0/1-рюкзака с $w_i>0$:

```python
# Pull: D[c] собирает ответ из старого D[c - weight].
for c in range(W, weight - 1, -1):
    D[c] = max(D[c], D[c - weight] + value)
```

```python
# Push: старое D[c] обновляет D[c + weight].
for c in range(W - weight, -1, -1):
    D[c + weight] = max(D[c + weight], D[c] + value)
```

- Оба прохода — по убыванию: один предмет не используется повторно.
- По возрастанию обновлённое значение можно использовать снова — это переход для неограниченного числа копий предмета.
- При $w_i=0$ каждую ячейку обновляем один раз; направление несущественно.
- Для точного веса база: $D[0]=0$, $D[c>0]=-\infty$. Для веса **не более** $c$: $D[c]=0$ для всех $c$.
- `parent` должен ссылаться на состояние с номером слоя $(i,c)$. Ссылка только на изменяемую ячейку `D[c]` может потерять историю.

## Вычисление и восстановление

- `state` — состояние; `dp[state]` — его оптимальное значение.
- **Таблица значений:** сохраняем оптимумы состояний; при восстановлении заново определяем, какой переход дал оптимум.
- **Сохранённые переходы:** возвращаем оптимальное значение и `parent`; восстановление следует готовому пути. Старые значения можно удалять, когда они больше не нужны следующим переходам.

- Для плотных состояний `parent` — индексируемый массив. Рюкзак хранит признак взятия, LCS и редактирование — направление перехода. Предыдущие координаты следуют из индексов и направления; хранить их повторно не нужно. Расписание хранит `(prev_state, item)`, где `item = None` означает пропуск.
- LIS хранит предыдущий индекс; цепочка матриц — индекс разреза `k`, определяющий обе подзадачи.
- В компактных версиях рюкзака и редактирования Python добавляем элементы в список с конца и разворачиваем его на месте. Время — $O(k)$, отдельная коллекция для копирования ответа не нужна.
- В остальных Python-вариантах `deque.appendleft` сохраняет прямой порядок; преобразование в список или строку требует $O(k)$ времени и временной памяти. Индексируемые таблицы остаются списками.

Имена функций описывают результат: `build_table` строит таблицу значений, `build_parents` возвращает оптимум и переходы, `restore_from_table` и `restore_from_parents` восстанавливают ответ по соответствующим данным. Варианты используют одинаковый обход; различаются хранимые данные и возвращаемый результат. В префиксных задачах `i` и `j` — длины префиксов: цикл задаёт их через `range`, а последний элемент префикса читается по индексу `i-1` или `j-1`.

**Выбор представления:** по таблице значений можно заново найти оптимальный переход; `parent` фиксирует его сразу. Это упрощает восстановление, но история переходов тоже занимает память. В строковых задачах и рюкзаке `bytearray` хранит один байт на ячейку вместо числового оптимума; строки `prev` и `curr` всё ещё нужны при вычислении. Асимптотический порядок памяти сохраняется, но постоянный множитель истории уменьшается.

Публичные `knapsack_01.solve`, `longest_common_subsequence.solve` и `edit_distance.align` в Python используют две строки и байтовую историю переходов. Полные Python-таблицы ниже — учебный вариант восстановления по значениям. Две строки сокращают рабочие значения, но история по-прежнему занимает память порядка числа состояний.

Оценки памяти ниже включают рабочие значения и историю переходов, но не вход и готовый ответ. `prev` и `curr` — предыдущий и текущий слой значений; `(prev_state, item)` — предыдущее состояние и действие при восстановлении.

Направления используются в LCS и редактировании; перечисление именует байты без неясных числовых кодов:

```{literalinclude} ../../src/algorithms/dynamic_programming/directions.py
:language: python
:pyobject: Direction
```

Python `str` задаёт последовательность кодовых точек Unicode; расстояния и длины подпоследовательностей измеряются в них. См. [Python str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str). Нормализация Unicode не выполняется.

### Один формат двух строк

В рюкзаке, LCS и редактировании строки создаются один раз:

```python
prev = ... # базовый слой
curr = ...  # второй буфер
for layer in layers:
    # Задаём границу и вычисляем все ячейки curr.
    # prev не изменяется; готовые ячейки curr доступны слева.
    prev, curr = curr, prev
```

Это схема обхода, не отдельный алгоритм. Обмен меняет две ссылки за $O(1)$: значения не копируются. После обмена `prev` содержит готовый слой, а старый буфер используется для следующего. Перед чтением каждая его ячейка должна быть записана заново.

## 0/1-рюкзак

**Задача:** для $w\in\mathbb Z_{\ge0}^n$, $v\in\mathbb Z^n$, $W\ge0$ найти

$$\max_{S\subseteq\{0,\ldots,n-1\},\;\sum_{i\in S}w_i\le W}\sum_{i\in S}v_i$$

и индексы выбранных предметов. Каждый предмет используется не более одного раза.

### Состояния и переходы

```{literalinclude} ../../src/algorithms/dynamic_programming/knapsack_01/_types.py
:language: python
:start-at: type Parents =
:end-at: type Parents =
```

$dp[i,c]$ — максимум для первых $i$ предметов и вместимости $c$; $dp[0,c]=0$.

$$dp[i,c]=\begin{cases}
dp[i-1,c],&w_{i-1}>c,\\
\max\{dp[i-1,c],dp[i-1,c-w_{i-1}]+v_{i-1}\},&w_{i-1}\le c.
\end{cases}$$

Обе ветви переходят в слой $i-1$, включая $w_{i-1}=0$. Оптимальный набор либо пропускает последний предмет, либо берёт его; максимум исчерпывает оба случая.

### Вычисление и восстановление

`````{tab-set}
:sync-group: reconstruction

````{tab-item} По значениям
:sync: table

```{literalinclude} ../../src/algorithms/dynamic_programming/knapsack_01/_build_table.py
:language: python
:pyobject: build_table
```

```{literalinclude} ../../src/algorithms/dynamic_programming/knapsack_01/_restore_from_table.py
:language: python
:pyobject: restore_from_table
```

```python
dp = build_table(weights, values, cap)
val = dp[-1][cap]
ans = restore_from_table(weights, cap, dp)
```
````

````{tab-item} Через parent
:sync: parent

```{literalinclude} ../../src/algorithms/dynamic_programming/knapsack_01/_build_parents.py
:language: python
:pyobject: build_parents
```

```{literalinclude} ../../src/algorithms/dynamic_programming/knapsack_01/_restore_from_parents.py
:language: python
:pyobject: restore_from_parents
```

```python
val, parent = build_parents(weights, values, cap)
ans = restore_from_parents(weights, cap, parent)
```
````
`````

- Состояние: `(i, c)`. При равенстве пропускаем предмет; `item` — его индекс с нуля.
- Вычисление: $\Theta((n+1)(W+1))$ времени; восстановление — $O(n)$.

| Версия | Что хранится | Память |
|---|---|---|
| По `dp` | Все слои значений | $\Theta((n+1)(W+1))$ |
| Через `parent` | Две строки значений + один байт взятия на ячейку | $\Theta(W+1)$ + $\Theta(n(W+1))$ |

Вторая версия освобождает старые **значения**, но сохраняет историю выбора: полной асимптотической экономии нет. Переход всегда читает `prev`, поэтому даже предмет нулевого веса не используется повторно.
- Только значение можно вычислять с $\Theta(W+1)$ памятью. Для восстановления нужны таблица либо история переходов.

```````{dropdown} Публичный импорт

````{literalinclude} ../../src/algorithms/dynamic_programming/knapsack_01/__init__.py
:language: python
````

```````

## Наибольшая общая подпоследовательность

**Задача:** для строк $A,B$ найти

$$C^*\in\operatorname*{arg\,max}_{C\preceq A,\;C\preceq B}|C|.$$

$\preceq$ обозначает отношение подпоследовательности; $m=|A|$, $n=|B|$.

### Состояния и переходы

```{literalinclude} ../../src/algorithms/dynamic_programming/longest_common_subsequence/_types.py
:language: python
:start-at: type Parents =
:end-at: type Parents =
```

$dp[i,j]$ — длина LCS префиксов $A[:i],B[:j]$; $dp[0,j]=dp[i,0]=0$.

$$dp[i,j]=\begin{cases}
dp[i-1,j-1]+1,&A_{i-1}=B_{j-1},\\
\max\{dp[i-1,j],dp[i,j-1]\},&A_{i-1}\ne B_{j-1}.
\end{cases}$$

При равных концах существует оптимум, использующий оба: перенесём последние выбранные вхождения на концы. При разных концах хотя бы один пропущен. Индукция по $i+j$.

### Вычисление и восстановление

`````{tab-set}
:sync-group: reconstruction

````{tab-item} По значениям
:sync: table

```{literalinclude} ../../src/algorithms/dynamic_programming/longest_common_subsequence/_build_table.py
:language: python
:pyobject: build_table
```

```{literalinclude} ../../src/algorithms/dynamic_programming/longest_common_subsequence/_restore_from_table.py
:language: python
:pyobject: restore_from_table
```

```python
dp = build_table(A, B)
val = dp[-1][-1]
ans = restore_from_table(A, B, dp)
```
````

````{tab-item} Через parent
:sync: parent

```{literalinclude} ../../src/algorithms/dynamic_programming/longest_common_subsequence/_build_parents.py
:language: python
:pyobject: build_parents
```

```{literalinclude} ../../src/algorithms/dynamic_programming/longest_common_subsequence/_restore_from_parents.py
:language: python
:pyobject: restore_from_parents
```

```python
val, parent = build_parents(A, B)
ans = restore_from_parents(A, B, parent)
```
````
`````

- Состояние: `(i, j)`. Диагональ добавляет символ; остальные переходы — `None`.
- При равенстве соседних значений выбираем $(i-1,j)$.
- Вычисление: $\Theta((m+1)(n+1))$ времени; восстановление — $O(m+n)$.

| Версия | Что хранится | Память |
|---|---|---|
| По `dp` | Таблица длин; переход ищется по соседним ячейкам | $\Theta((m+1)(n+1))$ |
| Через `parent` | Две строки длин + один байт направления на ячейку | $\Theta(n+1)$ + $\Theta((m+1)(n+1))$ |

`prev[j-1]` — диагональ, `prev[j]` — верхняя ячейка, `curr[j-1]` — левая. Предки избавляют восстановление от сравнений длин; общая память остаётся того же порядка.

```````{dropdown} Публичный импорт

````{literalinclude} ../../src/algorithms/dynamic_programming/longest_common_subsequence/__init__.py
:language: python
````

```````

## Расстояние редактирования

**Задача:** для строк $X,Y$ найти минимальное число вставок, удалений и замен, преобразующих $X$ в $Y$, и выравнивание. Стоимость операции — $1$.

### Состояния и переходы

```{literalinclude} ../../src/algorithms/dynamic_programming/edit_distance/_types.py
:language: python
:start-at: type EditKind =
:end-at: type EditKind =
```

```{literalinclude} ../../src/algorithms/dynamic_programming/edit_distance/_types.py
:language: python
:pyobject: Edit
```

```{literalinclude} ../../src/algorithms/dynamic_programming/edit_distance/_types.py
:language: python
:start-at: type Parents =
:end-at: type Parents =
```

$dp[i,j]$ — стоимость преобразования $X[:i]$ в $Y[:j]$.

$$dp[i,0]=i,\qquad dp[0,j]=j,$$
$$dp[i,j]=\min\{dp[i-1,j-1]+[X_{i-1}\ne Y_{j-1}],\ dp[i-1,j]+1,\ dp[i,j-1]+1\}.$$

Последняя операция — сопоставление, удаление или вставка. Каждый переход допустим; перечисление полно. Индукция по $i+j$.

### Только расстояние

Если нужны только число операций и не требуется выравнивание, история состояний не нужна. Следующий слой зависит от предыдущей строки и уже вычисленной ячейки слева. Держим два буфера, а более короткую строку используем для столбцов: расстояние симметрично.

```{literalinclude} ../../src/algorithms/dynamic_programming/edit_distance/_compute.py
:language: python
:pyobject: compute
```

Время — $O(mn+m+n)$, память — $\Theta(\min(m,n)+1)$. Для восстановления по значениям ниже сохраняем полную таблицу: две строки уже не содержат путь от последнего состояния к первому.

### Вычисление и восстановление

`````{tab-set}
:sync-group: reconstruction

````{tab-item} По значениям
:sync: table

```{literalinclude} ../../src/algorithms/dynamic_programming/edit_distance/_build_table.py
:language: python
:pyobject: build_table
```

```{literalinclude} ../../src/algorithms/dynamic_programming/edit_distance/_restore_from_table.py
:language: python
:pyobject: restore_from_table
```

```python
dp = build_table(X, Y)
val = dp[-1][-1]
ans = restore_from_table(X, Y, dp)
```
````

````{tab-item} Через parent
:sync: parent

```{literalinclude} ../../src/algorithms/dynamic_programming/edit_distance/_build_parents.py
:language: python
:pyobject: build_parents
```

```{literalinclude} ../../src/algorithms/dynamic_programming/edit_distance/_restore_from_parents.py
:language: python
:pyobject: restore_from_parents
```

```python
val, parent = build_parents(X, Y)
ans = restore_from_parents(X, Y, parent)
```
````
`````

- Состояние: `(i, j)`. `Edit` задаёт действие и символы; `None` — пропуск.
- При равенстве: диагональ → удаление → вставка. Границы ведут к `(0, 0)`.
- Вычисление: $\Theta((m+1)(n+1))$ времени; восстановление — $O(m+n)$.

| Версия | Что хранится | Память |
|---|---|---|
| По `dp` | Таблица расстояний; операция определяется по равенству стоимостей | $\Theta((m+1)(n+1))$ |
| Через `parent` | Две строки расстояний + один байт направления на ячейку | $\Theta(n+1)$ + $\Theta((m+1)(n+1))$ |

Диагональ означает совпадение или замену, верх — удаление, лево — вставку. `parent` хранит только направление. `Edit` с символами создаётся при восстановлении, только для операций ответа.

```````{dropdown} Публичный импорт

````{literalinclude} ../../src/algorithms/dynamic_programming/edit_distance/__init__.py
:language: python
````

```````

## Взвешенное расписание интервалов

**Задача:** для интервалов $I_i=[s_i,f_i)$, $s_i\le f_i$, найти совместимый набор максимального суммарного веса и его исходные индексы.

Пустые интервалы совместимы со всеми: добавляем все с положительным весом отдельно. Непустые сортируем по окончанию.

### Состояния и переходы

```{literalinclude} ../../src/algorithms/dynamic_programming/weighted_interval_scheduling/_prepare_jobs.py
:language: python
:pyobject: prepare_jobs
```

```{literalinclude} ../../src/algorithms/dynamic_programming/weighted_interval_scheduling/_types.py
:language: python
:start-at: type State =
:end-at: type Parents =
```

$prev[j]$ — число предшествующих интервалов, заканчивающихся не позже начала $j$. Предшественник вычисляется бинарным поиском: версия по значениям сохраняет массив `prev`, версия с `parent` сразу записывает выбранный переход.

$$dp[0]=0,\qquad dp[j+1]=\max\{dp[j],w_j+dp[prev[j]]\}.$$

Оптимум либо пропускает $j$, либо объединяет его с оптимумом совместимого префикса.

### Вычисление и восстановление

`````{tab-set}
:sync-group: reconstruction

````{tab-item} По значениям
:sync: table

```{literalinclude} ../../src/algorithms/dynamic_programming/weighted_interval_scheduling/_build_table.py
:language: python
:pyobject: build_table
```

```{literalinclude} ../../src/algorithms/dynamic_programming/weighted_interval_scheduling/_restore_from_table.py
:language: python
:pyobject: restore_from_table
```

```python
jobs, empty = prepare_jobs(intervals)
dp, prev = build_table(jobs)
val = dp[-1] + sum(w for _, w in empty)
ans = sorted(restore_from_table(jobs, prev, dp) + [i for i, _ in empty])
```
````

````{tab-item} Через parent
:sync: parent

```{literalinclude} ../../src/algorithms/dynamic_programming/weighted_interval_scheduling/_build_parents.py
:language: python
:pyobject: build_parents
```

```{literalinclude} ../../src/algorithms/dynamic_programming/weighted_interval_scheduling/_restore_from_parents.py
:language: python
:pyobject: restore_from_parents
```

```python
jobs, empty = prepare_jobs(intervals)
val, parent = build_parents(jobs)
val += sum(w for _, w in empty)
ans = sorted(restore_from_parents(jobs, parent) + [i for i, _ in empty])
```
````
`````

- Состояние — длина префикса. При равенстве пропускаем последний интервал.
- `prev` описывает допустимые переходы; `parent` — выбранные. Отдельный `take` не нужен.
- Подготовка и вычисление: $O(n\log n)$ времени; восстановление — $O(n)$.

| Версия | Что хранится | Память |
|---|---|---|
| По `dp` | Стоимости префиксов и совместимые предшественники `prev` | $O(n)$ |
| Через `parent` | Те же рабочие стоимости + выбранный переход | $O(n)$ |

Двух соседних стоимостей недостаточно: `prev[j]` может указывать далеко назад. `parent` упрощает восстановление, но добавляет записи; рабочий массив `dp` нужен до конца вычисления.
- Обратный проход: $O(n)$; сортировка исходных индексов — $O(k\log k)$ времени и $O(k)$ памяти. Порядок этих индексов не совпадает с порядком интервалов по окончанию.

```````{dropdown} Публичный импорт

````{literalinclude} ../../src/algorithms/dynamic_programming/weighted_interval_scheduling/__init__.py
:language: python
````

```````

## Наибольшая возрастающая подпоследовательность

**Задача:** для $a\in\mathbb Z^n$ найти

$$0\le i_1<\cdots<i_k<n,\qquad a_{i_1}<\cdots<a_{i_k},\qquad k\to\max.$$

Результат — значения и индексы подпоследовательности.

### Состояния и переходы

```{literalinclude} ../../src/algorithms/dynamic_programming/longest_increasing_subsequence/_types.py
:language: python
:start-at: type State = int
:end-at: type Parents =
```

$dp[i]$ — длина LIS, заканчивающейся в $i$. `tails[k]` — минимальный последний элемент подпоследовательности длины $k+1$; в версии с предками `tail_indices[k]` — его индекс. При восстановлении по длинам достаточно одного `end` — индекса последнего хвоста.

Первый хвост $\ge a_i$ заменяется на $a_i$; при отсутствии такого хвоста длина увеличивается. Равные значения не увеличивают длину. `end` — конечное состояние ответа.

### Вычисление и восстановление

`````{tab-set}
:sync-group: reconstruction

````{tab-item} По значениям
:sync: table

```{literalinclude} ../../src/algorithms/dynamic_programming/longest_increasing_subsequence/_build_table.py
:language: python
:pyobject: build_table
```

```{literalinclude} ../../src/algorithms/dynamic_programming/longest_increasing_subsequence/_restore_from_table.py
:language: python
:pyobject: restore_from_table
```

```python
dp, end = build_table(a)
val = max(dp, default=0)
indices = restore_from_table(a, dp, end)
ans = [a[i] for i in indices]
```
````

````{tab-item} Через parent
:sync: parent

```{literalinclude} ../../src/algorithms/dynamic_programming/longest_increasing_subsequence/_build_parents.py
:language: python
:pyobject: build_parents
```

```{literalinclude} ../../src/algorithms/dynamic_programming/longest_increasing_subsequence/_restore_from_parents.py
:language: python
:pyobject: restore_from_parents
```

```python
val, end, parent = build_parents(a)
indices = restore_from_parents(end, parent)
ans = [a[i] for i in indices]
```
````
`````

- Состояние — индекс последнего элемента. `parent[i]` записывается до обновления хвостов.
- По `dp` ищем $j<i$ с $dp[j]=dp[i]-1$ и $a_j<a_i$. Индексы поиска только убывают: суммарно $O(n)$, несмотря на вложенный цикл.
- Через `parent`: $O(k)$ времени восстановления. Варианты могут выбрать разные оптимальные подпоследовательности.
- Вычисление: $O(n\log n)$ времени. Одних итоговых `tails` для восстановления недостаточно.

| Версия | Что хранится | Память | Восстановление |
|---|---|---|---|
| По `dp` | Длина для каждого индекса и хвосты | $O(n)$ | $O(n)$: поиск предыдущего индекса |
| Через `parent` | Хвосты и предыдущий индекс для каждого элемента | $O(n)$ | $O(k)$: готовая цепочка из $k$ индексов |

Во второй версии массив длин `dp` не нужен. Память меняет содержимое, а не порядок роста; выигрыш — восстановление пропорционально длине ответа.

```````{dropdown} Публичный импорт

````{literalinclude} ../../src/algorithms/dynamic_programming/longest_increasing_subsequence/__init__.py
:language: python
````

```````

## Оптимальное умножение цепочки матриц

**Задача:** для $n\ge1$ матриц $A_i$ размера $p_i\times p_{i+1}$, $0\le i<n$, найти минимальное число скалярных умножений и скобочную структуру. Все $p_i>0$.

### Состояния и переходы

```{literalinclude} ../../src/algorithms/dynamic_programming/matrix_chain_order/_types.py
:language: python
:start-at: type State = tuple[int, int]
:end-at: type Step =
```

$dp[i,j]$ — минимум для цепочки $A_i\cdots A_j$; $dp[i,i]=0$.

$$dp[i,j]=\min_{i\le k<j}\{dp[i,k]+dp[k+1,j]+p_i p_{k+1}p_{j+1}\}.$$

Последнее умножение разбивает цепочку после $k$. Минимум перебирает все разрезы и объединяет оптимальные части. Порядок вычисления — по длине интервала.

### Общие операции

`_cost_of_split` складывает стоимость левой части, правой части и последнего умножения. `_parenthesize` обходит дерево решения и один раз соединяет фрагменты строки. Обе версии используют эти функции.

```{literalinclude} ../../src/algorithms/dynamic_programming/matrix_chain_order/_common.py
:language: python
:pyobject: cost_of_split
```

```{literalinclude} ../../src/algorithms/dynamic_programming/matrix_chain_order/_common.py
:language: python
:pyobject: parenthesize
```

### Вычисление и восстановление

`````{tab-set}
:sync-group: reconstruction

````{tab-item} По значениям
:sync: table

```{literalinclude} ../../src/algorithms/dynamic_programming/matrix_chain_order/_build_table.py
:language: python
:pyobject: build_table
```

```{literalinclude} ../../src/algorithms/dynamic_programming/matrix_chain_order/_restore_from_table.py
:language: python
:pyobject: restore_from_table
```

```python
dp = build_table(p)
val = dp[0][-1]
ans = restore_from_table(p, dp)
```
````

````{tab-item} Через parent
:sync: parent

```{literalinclude} ../../src/algorithms/dynamic_programming/matrix_chain_order/_build_parents.py
:language: python
:pyobject: build_parents
```

```{literalinclude} ../../src/algorithms/dynamic_programming/matrix_chain_order/_restore_from_parents.py
:language: python
:pyobject: restore_from_parents
```

```python
val, parent = build_parents(p)
ans = restore_from_parents(p, parent)
```
````
`````

- Состояние: `(i, j)`. `parent[i][j] = k` задаёт обе подзадачи: `(i, k)` и `(k+1, j)`. При равенстве выбираем первый разрез.
- Вычисление: $O(n^3)$ времени.

| Версия | Что хранится при вычислении | Память | Поиск разрезов при восстановлении |
|---|---|---|---|
| По `dp` | Стоимости всех интервалов | $O(n^2)$ | $O(n^2)$ |
| Через `parent` | Стоимости всех интервалов + выбранные разрезы | $O(n^2)$ | $O(n)$ |

Здесь таблицу стоимостей нельзя заменить двумя строками: разрез обращается к подинтервалам разных длин. После вычисления версия с предками возвращает только стоимость и разрезы. Она быстрее восстанавливает ответ, но требует дополнительной истории.

Общая сборка строки выполняется за $O(n+L)$ времени, где $L$ — число символов результата; явный стек обхода — $O(n)$; рекурсивных вызовов нет. Фрагменты объединяются одним `join`, без повторного копирования вложенных выражений.
Длина записи с именами `A1`, …, `An` составляет $L=\Theta(n\log(n+1))$ символов; эта стоимость вывода учитывается отдельно от поиска разрезов.

```````{dropdown} Публичный импорт

````{literalinclude} ../../src/algorithms/dynamic_programming/matrix_chain_order/__init__.py
:language: python
````

```````

## Исходники и проверки

Каждая операция реализована в собственном файле. Фасад пакета экспортирует четыре учебных шага и полное решение; общий тип или помощник подключается из _types.py/_common.py. Полный список операций с ссылками на файлы — в [карте реализаций](../implementations.md#динамическое-программирование).

- {download}`Проверки двух способов восстановления <../../tests/algorithms/dynamic_programming/test_state_reconstruction.py>`
- {download}`Проверки полным перебором <../../tests/algorithms/dynamic_programming/test_reconstruction.py>`
