# Карта реализаций

Каждая существующая реализация и самостоятельная учебная операция находится в собственном файле. Одна реализация — модуль, несколько — пакет. В семействах с несколькими операциями сначала выбирается операция, затем вариант. __init__.py только собирает публичный импорт.

```python
from algorithms.dynamic_programming import fibonacci
from algorithms.searching import binary_search
from algorithms.sorting import merge_sort
from data_structures.stack import dynamic_array, fixed_array

assert fibonacci.recursive(10) == fibonacci.constant_space(10) == 55
assert binary_search.lower_bound.recursive([1, 3, 5], 3) == 1
values = [3, 1, 2]
merge_sort.sort(values)
assert values == [1, 2, 3]
stack = dynamic_array.Stack[int]()
limited = fixed_array.Stack[int](capacity=10)
```

Ссылки на операции ведут к их исходным файлам. Проект устанавливается командой `make setup`; все импорты относятся к пакетам из `src/`.

## Пример семейства с несколькими операциями

[Бинарный поиск](algorithms/binary-search.md) показывает операцию с двумя вариантами. В ДП у каждого шага одна реализация, поэтому фасад экспортирует его непосредственно:

```text
knapsack_01/
├── __init__.py
├── _build_table.py
├── _restore_from_table.py
├── _build_parents.py
├── _restore_from_parents.py
├── _solve.py
└── _types.py
```

Публичные вызовы: `knapsack_01.build_table(...)`, `knapsack_01.restore_from_table(...)`, `knapsack_01.build_parents(...)`, `knapsack_01.restore_from_parents(...)`, `knapsack_01.solve(...)`.

## Сортировки

Пространство имён: `algorithms.sorting`.

| Модуль или пакет | Операции и исходники |
|---|---|
| `bubble_sort` | {download}`sort <../src/algorithms/sorting/bubble_sort.py>` |
| `counting_sort` | {download}`sort <../src/algorithms/sorting/counting_sort.py>` |
| `heap_sort` | {download}`sort <../src/algorithms/sorting/heap_sort.py>` |
| `insertion_sort` | {download}`sort <../src/algorithms/sorting/insertion_sort.py>` |
| `merge_sort` | {download}`sort <../src/algorithms/sorting/merge_sort.py>` |
| `partition` | {download}`partition <../src/algorithms/sorting/partition.py>` |
| `quick_sort` | {download}`iterative <../src/algorithms/sorting/quick_sort/_iterative.py>`, {download}`recursive <../src/algorithms/sorting/quick_sort/_recursive.py>` |
| `radix_sort` | {download}`sort <../src/algorithms/sorting/radix_sort.py>` |
| `selection_sort` | {download}`sort <../src/algorithms/sorting/selection_sort.py>` |

## Поиск

Пространство имён: `algorithms.searching`.

| Модуль или пакет | Операции и исходники |
|---|---|
| `binary_search` | {download}`equal_range <../src/algorithms/searching/binary_search/_equal_range.py>`, {download}`search <../src/algorithms/searching/binary_search/_search.py>` |
| `binary_search.lower_bound` | {download}`iterative <../src/algorithms/searching/binary_search/lower_bound/_iterative.py>`, {download}`recursive <../src/algorithms/searching/binary_search/lower_bound/_recursive.py>` |
| `binary_search.upper_bound` | {download}`iterative <../src/algorithms/searching/binary_search/upper_bound/_iterative.py>`, {download}`recursive <../src/algorithms/searching/binary_search/upper_bound/_recursive.py>` |

## Разделяй и властвуй

Пространство имён: `algorithms.divide_and_conquer`.

| Модуль или пакет | Операции и исходники |
|---|---|
| `closest_pair` | {download}`ClosestPair <../src/algorithms/divide_and_conquer/closest_pair.py>`, {download}`find <../src/algorithms/divide_and_conquer/closest_pair.py>` |
| `inversions` | {download}`count <../src/algorithms/divide_and_conquer/inversions.py>` |

## Порядковые статистики

Пространство имён: `algorithms.selection`.

| Модуль или пакет | Операции и исходники |
|---|---|
| `median` | {download}`find <../src/algorithms/selection/median.py>` |
| `order_statistic` | {download}`by_sorting <../src/algorithms/selection/order_statistic/_by_sorting.py>`, {download}`iterative <../src/algorithms/selection/order_statistic/_iterative.py>`, {download}`recursive <../src/algorithms/selection/order_statistic/_recursive.py>` |

## Динамическое программирование

Пространство имён: `algorithms.dynamic_programming`.

| Модуль или пакет | Операции и исходники |
|---|---|
| `edit_distance` | {download}`Edit <../src/algorithms/dynamic_programming/edit_distance/_types.py>`, {download}`EditKind <../src/algorithms/dynamic_programming/edit_distance/_types.py>`, {download}`align <../src/algorithms/dynamic_programming/edit_distance/_align.py>`, {download}`build_parents <../src/algorithms/dynamic_programming/edit_distance/_build_parents.py>`, {download}`build_table <../src/algorithms/dynamic_programming/edit_distance/_build_table.py>`, {download}`compute <../src/algorithms/dynamic_programming/edit_distance/_compute.py>`, {download}`restore_from_parents <../src/algorithms/dynamic_programming/edit_distance/_restore_from_parents.py>`, {download}`restore_from_table <../src/algorithms/dynamic_programming/edit_distance/_restore_from_table.py>` |
| `fibonacci` | {download}`constant_space <../src/algorithms/dynamic_programming/fibonacci/_constant_space.py>`, {download}`memoized <../src/algorithms/dynamic_programming/fibonacci/_memoized.py>`, {download}`recursive <../src/algorithms/dynamic_programming/fibonacci/_recursive.py>`, {download}`tabulated <../src/algorithms/dynamic_programming/fibonacci/_tabulated.py>` |
| `knapsack_01` | {download}`build_parents <../src/algorithms/dynamic_programming/knapsack_01/_build_parents.py>`, {download}`build_table <../src/algorithms/dynamic_programming/knapsack_01/_build_table.py>`, {download}`restore_from_parents <../src/algorithms/dynamic_programming/knapsack_01/_restore_from_parents.py>`, {download}`restore_from_table <../src/algorithms/dynamic_programming/knapsack_01/_restore_from_table.py>`, {download}`solve <../src/algorithms/dynamic_programming/knapsack_01/_solve.py>` |
| `longest_common_subsequence` | {download}`build_parents <../src/algorithms/dynamic_programming/longest_common_subsequence/_build_parents.py>`, {download}`build_table <../src/algorithms/dynamic_programming/longest_common_subsequence/_build_table.py>`, {download}`restore_from_parents <../src/algorithms/dynamic_programming/longest_common_subsequence/_restore_from_parents.py>`, {download}`restore_from_table <../src/algorithms/dynamic_programming/longest_common_subsequence/_restore_from_table.py>`, {download}`solve <../src/algorithms/dynamic_programming/longest_common_subsequence/_solve.py>` |
| `longest_increasing_subsequence` | {download}`build_parents <../src/algorithms/dynamic_programming/longest_increasing_subsequence/_build_parents.py>`, {download}`build_table <../src/algorithms/dynamic_programming/longest_increasing_subsequence/_build_table.py>`, {download}`restore_from_parents <../src/algorithms/dynamic_programming/longest_increasing_subsequence/_restore_from_parents.py>`, {download}`restore_from_table <../src/algorithms/dynamic_programming/longest_increasing_subsequence/_restore_from_table.py>`, {download}`solve <../src/algorithms/dynamic_programming/longest_increasing_subsequence/_solve.py>` |
| `matrix_chain_order` | {download}`build_parents <../src/algorithms/dynamic_programming/matrix_chain_order/_build_parents.py>`, {download}`build_table <../src/algorithms/dynamic_programming/matrix_chain_order/_build_table.py>`, {download}`restore_from_parents <../src/algorithms/dynamic_programming/matrix_chain_order/_restore_from_parents.py>`, {download}`restore_from_table <../src/algorithms/dynamic_programming/matrix_chain_order/_restore_from_table.py>`, {download}`solve <../src/algorithms/dynamic_programming/matrix_chain_order/_solve.py>` |
| `weighted_interval_scheduling` | {download}`Job <../src/algorithms/dynamic_programming/weighted_interval_scheduling/_types.py>`, {download}`build_parents <../src/algorithms/dynamic_programming/weighted_interval_scheduling/_build_parents.py>`, {download}`build_table <../src/algorithms/dynamic_programming/weighted_interval_scheduling/_build_table.py>`, {download}`restore_from_parents <../src/algorithms/dynamic_programming/weighted_interval_scheduling/_restore_from_parents.py>`, {download}`restore_from_table <../src/algorithms/dynamic_programming/weighted_interval_scheduling/_restore_from_table.py>`, {download}`prepare_jobs <../src/algorithms/dynamic_programming/weighted_interval_scheduling/_prepare_jobs.py>`, {download}`solve <../src/algorithms/dynamic_programming/weighted_interval_scheduling/_solve.py>` |

## Графы

Пространство имён: `algorithms.graphs`.

| Модуль или пакет | Операции и исходники |
|---|---|
| `bellman_ford` | {download}`shortest_paths <../src/algorithms/graphs/bellman_ford.py>` |
| `bipartite` | {download}`check <../src/algorithms/graphs/bipartite.py>` |
| `breadth_first_search` | {download}`traverse <../src/algorithms/graphs/breadth_first_search.py>` |
| `connected_components` | {download}`find <../src/algorithms/graphs/connected_components.py>` |
| `depth_first_search` | {download}`traverse <../src/algorithms/graphs/depth_first_search.py>` |
| `dijkstra` | {download}`shortest_paths <../src/algorithms/graphs/dijkstra.py>` |
| `directed_acyclic_shortest_paths` | {download}`shortest_paths <../src/algorithms/graphs/directed_acyclic_shortest_paths.py>` |
| `directed_cycle` | {download}`exists <../src/algorithms/graphs/directed_cycle.py>` |
| `floyd_warshall` | {download}`shortest_paths <../src/algorithms/graphs/floyd_warshall.py>` |
| `kruskal` | {download}`minimum_spanning_forest <../src/algorithms/graphs/kruskal.py>` |
| `prim` | {download}`minimum_spanning_forest <../src/algorithms/graphs/prim.py>` |
| `strongly_connected_components` | {download}`find <../src/algorithms/graphs/strongly_connected_components.py>` |
| `topological_sort` | {download}`sort <../src/algorithms/graphs/topological_sort.py>` |
| `undirected_cycle` | {download}`exists <../src/algorithms/graphs/undirected_cycle.py>` |

## Строки

Пространство имён: `algorithms.strings`.

| Модуль или пакет | Операции и исходники |
|---|---|
| `knuth_morris_pratt` | {download}`search <../src/algorithms/strings/knuth_morris_pratt.py>` |
| `naive` | {download}`search <../src/algorithms/strings/naive.py>` |
| `prefix_function` | {download}`compute <../src/algorithms/strings/prefix_function.py>` |
| `rabin_karp` | {download}`search <../src/algorithms/strings/rabin_karp.py>` |
| `suffix_array` | {download}`build <../src/algorithms/strings/suffix_array.py>` |
| `z_function` | {download}`compute <../src/algorithms/strings/z_function.py>` |
| `z_search` | {download}`search <../src/algorithms/strings/z_search.py>` |

## Жадные алгоритмы

Пространство имён: `algorithms.greedy`.

| Модуль или пакет | Операции и исходники |
|---|---|
| `fractional_knapsack` | {download}`solve <../src/algorithms/greedy/fractional_knapsack.py>` |
| `huffman` | {download}`build_codes <../src/algorithms/greedy/huffman.py>` |
| `interval_scheduling` | {download}`select <../src/algorithms/greedy/interval_scheduling.py>` |

## Верификаторы

Пространство имён: `algorithms.complexity`.

| Модуль или пакет | Операции и исходники |
|---|---|
| `clique` | {download}`verify <../src/algorithms/complexity/clique.py>` |
| `subset_sum` | {download}`verify <../src/algorithms/complexity/subset_sum.py>` |
| `traveling_salesperson` | {download}`verify <../src/algorithms/complexity/traveling_salesperson.py>` |
| `vertex_cover` | {download}`approximate <../src/algorithms/complexity/vertex_cover/_approximate.py>`, {download}`verify <../src/algorithms/complexity/vertex_cover/_verify.py>` |

## Структуры данных

Пространство имён: `data_structures`.

| Модуль или пакет | Операции и исходники |
|---|---|
| `binary_search_tree` | {download}`BinarySearchTree <../src/data_structures/binary_search_tree.py>` |
| `deque` | {download}`Deque <../src/data_structures/deque.py>` |
| `disjoint_set_union` | {download}`DisjointSetUnion <../src/data_structures/disjoint_set_union.py>` |
| `hash_map` | {download}`HashMap <../src/data_structures/hash_map.py>` |
| `heap` | {download}`build <../src/data_structures/heap/_build.py>`, {download}`sift_down <../src/data_structures/heap/_sift_down.py>`, {download}`sift_up <../src/data_structures/heap/_sift_up.py>` |
| `interfaces` | {download}`Stack <../src/data_structures/interfaces/_stack.py>`, {download}`Queue <../src/data_structures/interfaces/_queue.py>`, {download}`Deque <../src/data_structures/interfaces/_deque.py>`, {download}`PriorityQueue <../src/data_structures/interfaces/_priority_queue.py>`, {download}`ExtremaStack <../src/data_structures/interfaces/_extrema_stack.py>`, {download}`ExtremaQueue <../src/data_structures/interfaces/_extrema_queue.py>`, {download}`PersistentStack <../src/data_structures/interfaces/_persistent_stack.py>`, {download}`PersistentQueue <../src/data_structures/interfaces/_persistent_queue.py>`, {download}`BinarySearchTree <../src/data_structures/interfaces/_binary_search_tree.py>`, {download}`HashMap <../src/data_structures/interfaces/_hash_map.py>`, {download}`DisjointSetUnion <../src/data_structures/interfaces/_disjoint_set_union.py>`, {download}`Trie <../src/data_structures/interfaces/_trie.py>` |
| `priority_queue.maximum` | {download}`PriorityQueue <../src/data_structures/priority_queue/maximum.py>` |
| `priority_queue.minimum` | {download}`PriorityQueue <../src/data_structures/priority_queue/minimum.py>` |
| `queue.extrema.maximum` | {download}`Queue <../src/data_structures/queue/extrema/maximum.py>` |
| `queue.extrema.minimum` | {download}`Queue <../src/data_structures/queue/extrema/minimum.py>` |
| `queue.linked_list` | {download}`Queue <../src/data_structures/queue/linked_list.py>` |
| `queue.persistent` | {download}`Queue <../src/data_structures/queue/persistent.py>` |
| `queue.ring` | {download}`Queue <../src/data_structures/queue/ring.py>` |
| `queue.two_stacks` | {download}`Queue <../src/data_structures/queue/two_stacks.py>` |
| `stack.dynamic_array` | {download}`Stack <../src/data_structures/stack/dynamic_array.py>` |
| `stack.fixed_array` | {download}`Stack <../src/data_structures/stack/fixed_array.py>` |
| `stack.linked_list` | {download}`Stack <../src/data_structures/stack/linked_list.py>` |
| `stack.extrema.minimum` | {download}`Stack <../src/data_structures/stack/extrema/minimum.py>` |
| `stack.extrema.maximum` | {download}`Stack <../src/data_structures/stack/extrema/maximum.py>` |
| `stack.one_queue` | {download}`Stack <../src/data_structures/stack/one_queue.py>` |
| `stack.persistent` | {download}`Stack <../src/data_structures/stack/persistent.py>` |
| `stack.two_queues` | {download}`Stack <../src/data_structures/stack/two_queues.py>` |
| `trie` | {download}`Trie <../src/data_structures/trie.py>` |

## Общие части

Общие типы и помощники переиспользуются реализациями. Они не создают дополнительных вариантов алгоритма.

| Файл | Назначение |
|---|---|
| {download}`algorithms/comparable.py <../src/algorithms/comparable.py>` | Переиспользуемые операции, проверки или определения |
| {download}`algorithms/complexity/_common.py <../src/algorithms/complexity/_common.py>` | Переиспользуемые операции, проверки или определения |
| {download}`algorithms/dynamic_programming/directions.py <../src/algorithms/dynamic_programming/directions.py>` | Переиспользуемые операции, проверки или определения |
| {download}`algorithms/dynamic_programming/edit_distance/_types.py <../src/algorithms/dynamic_programming/edit_distance/_types.py>` | Записи и алиасы задачи |
| {download}`algorithms/dynamic_programming/knapsack_01/_types.py <../src/algorithms/dynamic_programming/knapsack_01/_types.py>` | Записи и алиасы задачи |
| {download}`algorithms/dynamic_programming/longest_common_subsequence/_types.py <../src/algorithms/dynamic_programming/longest_common_subsequence/_types.py>` | Записи и алиасы задачи |
| {download}`algorithms/dynamic_programming/longest_increasing_subsequence/_types.py <../src/algorithms/dynamic_programming/longest_increasing_subsequence/_types.py>` | Записи и алиасы задачи |
| {download}`algorithms/dynamic_programming/matrix_chain_order/_common.py <../src/algorithms/dynamic_programming/matrix_chain_order/_common.py>` | Переиспользуемые операции, проверки или определения |
| {download}`algorithms/dynamic_programming/matrix_chain_order/_types.py <../src/algorithms/dynamic_programming/matrix_chain_order/_types.py>` | Записи и алиасы задачи |
| {download}`algorithms/dynamic_programming/weighted_interval_scheduling/_types.py <../src/algorithms/dynamic_programming/weighted_interval_scheduling/_types.py>` | Записи и алиасы задачи |
| {download}`algorithms/graphs/_common.py <../src/algorithms/graphs/_common.py>` | Переиспользуемые операции, проверки или определения |
| {download}`algorithms/graphs/_indexed_heap.py <../src/algorithms/graphs/_indexed_heap.py>` | Переиспользуемые операции, проверки или определения |
| {download}`algorithms/selection/_select_rank.py <../src/algorithms/selection/_select_rank.py>` | Переиспользуемые операции, проверки или определения |
| {download}`algorithms/sorting/_integers.py <../src/algorithms/sorting/_integers.py>` | Переиспользуемые операции, проверки или определения |
| {download}`data_structures/stack/extrema/_types.py <../src/data_structures/stack/extrema/_types.py>` | Записи и алиасы задачи |
