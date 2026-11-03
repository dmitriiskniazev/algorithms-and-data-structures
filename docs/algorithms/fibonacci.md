# Фибоначчи: от рекурсии к двум переменным

## Задача

Вычислите число Фибоначчи и проследите, как сохранение промежуточных результатов сокращает работу.

:::{container} task-facts

**Вход.** n=10.

**Результат.** F₁₀=55 во всех четырёх реализациях.

:::

**Предусловия.** $n\in\mathbb Z_{\ge0}$; определение и модель стоимости приведены ниже.

### Проверка

Запустите пример: утверждения фиксируют ожидаемое поведение.

```python
from algorithms.dynamic_programming import fibonacci

assert fibonacci.recursive(10) == 55
assert fibonacci.memoized(10) == 55
assert fibonacci.tabulated(10) == 55
assert fibonacci.constant_space(10) == 55
```

**Задача:** для $n\in\mathbb Z_{\ge 0}$ найти

$$
F_n = \begin{cases}
0, & n = 0,\\
1, & n = 1,\\
F_{n-1} + F_{n-2}, & n \ge 2.
\end{cases}
$$

[Итоговый код](#two-values) · [Сложность](#comparison)

```{contents} На этой странице
:local:
:depth: 1
:class: mobile-toc
```

## 1. Рекурсия

```{literalinclude} ../../src/algorithms/dynamic_programming/fibonacci/_recursive.py
:language: python
:pyobject: recursive
```

- Прямая запись определения: каждый вызов разбивает задачу на два предыдущих индекса.
- Повторные вычисления одинаковых подзадач.
- Время $\Theta(\varphi^n)$, стек $\Theta(n)$; $\varphi=(1+\sqrt5)/2$.

**Корректность:** по теореме о рекурсии — функция повторяет определение $F_n$.

````{dropdown} Число вызовов
$$
\begin{aligned}
C_0=C_1&=1,\\
C_n&=1+C_{n-1}+C_{n-2},\\
C_n+1&=(C_{n-1}+1)+(C_{n-2}+1),\\
C_n&=2F_{n+1}-1=\Theta(\varphi^n).
\end{aligned}
$$
````

## 2. Мемоизация

```{literalinclude} ../../src/algorithms/dynamic_programming/fibonacci/_memoized.py
:language: python
:emphasize-lines: 2-3,7-9
```

- `memo[k]` хранит $F_k$. Процедура `_solve(n, memo)` возвращает готовое значение или вычисляет его через два меньших индекса и сохраняет.
- Переход тот же, что в рекурсии; изменилось хранение уже решённых подзадач.
- Кеш отдельный для каждого внешнего вызова.
- $n-1$ сложений при $n\ge2$; кеш и стек — $\Theta(n)$.
- Глубина рекурсии ограничена Python; возможен `RecursionError` в обеих рекурсивных версиях.

**Инвариант кеша:** $k\in\operatorname{dom}(M)\implies M[k]=F_k$. Запись — по рекуррентному соотношению; чтение сохраняет результат.

## 3. Таблица

```{literalinclude} ../../src/algorithms/dynamic_programming/fibonacci/_tabulated.py
:language: python
:pyobject: tabulated
```

- Состояние: $a_k=F_k$.
- Порядок: $k=2,\ldots,n$; зависимости $k-1$ и $k-2$ уже вычислены.
- Переход тот же; порядок теперь задаёт цикл, поэтому рекурсивного стека нет.
- Время $\Theta(n)$, память $\Theta(n)$.

**Инвариант перед итерацией $k$:**

$$I(k):\quad \forall j\in\{0,\ldots,k-1\}\quad a_j=F_j.$$

````{dropdown} Корректность
- $n<2$: возвращается $n=F_n$.
- $n\ge2$: $a_0=0=F_0$, $a_1=1=F_1$ — выполнено $I(2)$.
- $I(k)\implies a_k\gets a_{k-1}+a_{k-2}=F_k\implies I(k+1)$.
- $I(n+1)\implies a_n=F_n$.
````

(two-values)=
## 4. Две переменные

```{literalinclude} ../../src/algorithms/dynamic_programming/fibonacci/_constant_space.py
:language: python
:pyobject: constant_space
```

- Python начинает с `(prev, curr) = (1, 0)` и делает `n` сдвигов через одновременное присваивание. После первого сдвига пара равна `(F_0, F_1)`.
- Старые числа больше не нужны следующим шагам. Удаляем их из памяти, сохраняя тот же переход.
- Время — $\Theta(n)$, память — $\Theta(1)$ числовых значений.

**Инвариант Python после $k\ge1$ шагов:** `(prev, curr)` $=(F_{k-1},F_k)$.

````{dropdown} Корректность
- При `n=0` цикл пуст и возвращает `0`.
- Первый шаг даёт $(0,1)=(F_0,F_1)$.
- Шаг: $(F_{k-1},F_k)\mapsto(F_k,F_{k-1}+F_k)=(F_k,F_{k+1})$.
- После `n` шагов `curr` $=F_n$.
````

(comparison)=
## Сложность

Модель: сложение и доступ к кешу — $O(1)$; память — число значений и кадров стека.

| Версия | Время | Память |
|---|---|---|
| Рекурсия | $\Theta(\varphi^n)$ | $\Theta(n)$ |
| Мемоизация | $\Theta(n)$ | $\Theta(n)$ |
| Таблица | $\Theta(n)$ | $\Theta(n)$ |
| Две переменные | $\Theta(n)$ | $\Theta(1)$ |

**Битовая модель Python:** итоговый цикл — $\Theta(n^2)$ времени, $\Theta(n)$ бит памяти.

````{dropdown} Битовая сложность
$$
F_{n+2}\ge2F_n,\quad F_n\le2^n
\implies b_n=\lfloor\log_2F_n\rfloor+1=\Theta(n)\quad(n\ge2).
$$

При линейной стоимости сложения:

$$
T(n)=\sum_{k=2}^{n}\Theta(b_k)=\Theta(n^2),\qquad
S_{\text{пара}}(n)=\Theta(b_n)=\Theta(n).
$$

Таблица и кеш: $S(n)=\sum_{k=2}^{n}\Theta(b_k)=\Theta(n^2)$ бит.
````

(source-files)=
## Исходники

- Исходники: {download}`recursive <../../src/algorithms/dynamic_programming/fibonacci/_recursive.py>`, {download}`memoized <../../src/algorithms/dynamic_programming/fibonacci/_memoized.py>`, {download}`tabulated <../../src/algorithms/dynamic_programming/fibonacci/_tabulated.py>`, {download}`constant_space <../../src/algorithms/dynamic_programming/fibonacci/_constant_space.py>`.
- {download}`Тесты <../../tests/algorithms/dynamic_programming/fibonacci/test_fibonacci.py>`.

Далее: [динамическое программирование](dynamic-programming.md).
