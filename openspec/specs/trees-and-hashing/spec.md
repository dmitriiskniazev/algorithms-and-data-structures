# trees-and-hashing Specification

## Purpose
Определяет учебные контракты для базового двоичного дерева поиска и хеш-таблицы с цепочками.

## Requirements

### Requirement: Двоичное дерево поиска хранит уникальные сравнимые ключи

BST SHALL поддерживать search/insert/delete уникальных относительно < ключей и обходы inorder/preorder/postorder. Эквивалентность SHALL определяться двумя сравнениями < без обязательного __eq__. Повторная вставка и удаление отсутствующего ключа SHALL возвращать False без изменения дерева. Inorder SHALL выдавать возрастающий порядок. Приватная процедура поиска SHALL явно возвращать найденный узел и родителя.

#### Scenario: Удаление узла с двумя потомками
- **WHEN** удаляется найденный узел с двумя поддеревьями
- **THEN** его место занимает минимум правого поддерева, а инвариант BST и все остальные ключи сохраняются

#### Scenario: Вырожденное дерево
- **WHEN** ключи вставлены в отсортированном порядке
- **THEN** операции поиска, вставки и удаления корректны, но могут занимать O(n)

### Requirement: Обходы выдают каждый ключ ровно один раз

Каждый обход SHALL посещать узлы ровно один раз в своём порядке; их время SHALL быть O(n), дополнительная память SHALL быть O(h) для стека обхода и глубины h, исключая возвращаемый результат.

#### Scenario: Пустое дерево
- **WHEN** выполняется любой обход пустого дерева
- **THEN** возвращается пустая последовательность

### Requirement: Хеш-таблица разрешает коллизии цепочками

Хеш-таблица SHALL отображать hashable ключи в значения и поддерживать добавление/обновление, поиск, удаление и размер. Разные ключи с одинаковым хешем SHALL храниться отдельно. Равные ключи SHALL обозначать одну запись. В Python SHALL использоваться протокол хешируемых ключей. Таблица SHALL поддерживать рост и перераспределение цепочек при превышении заданного коэффициента заполнения. Реализации SHALL включать Python 3.15+.

#### Scenario: Коллизия хешей
- **WHEN** два неравных ключа отображаются в один индекс корзины
- **THEN** поиск каждого возвращает собственное значение, обновление одного не меняет другое, удаление одного сохраняет другое

#### Scenario: Рост таблицы
- **WHEN** число записей превышает порог коэффициента заполнения
- **THEN** корзины увеличиваются, все пары сохраняются и остаются доступными по исходным ключам

### Requirement: Урок объясняет корректность и стоимость

Урок SHALL приводить контракты и исходный код, доказывать сохранение порядка BST при операциях и корректность обхода/цепочек, различать h и n, объяснять ожидаемые и худшие оценки и ограничения несбалансированного дерева и хеширования.

#### Scenario: Сравнение структур
- **WHEN** читатель сравнивает BST и хеш-таблицу
- **THEN** урок связывает выбор с потребностью в порядке ключей и гарантированностью времени поиска

### Requirement: DSU maintains a partition under union operations

Disjoint-set union SHALL represent the partition of a fixed universe `0..n-1` and support `find`, `union`, and connectivity queries. Implementations SHALL use path compression and union by component size. `union` SHALL return whether two distinct components were merged and update the component count exactly in that case. Invalid elements SHALL raise an explicit range error. Implementations SHALL include Python 3.15+.

#### Scenario: Union within one component
- **WHEN** two elements already have the same representative
- **THEN** union reports no merge and leaves the component count unchanged

#### Scenario: Merge components
- **WHEN** two elements belong to different components
- **THEN** union joins their sets, future finds return one representative, and the component count decreases by one
