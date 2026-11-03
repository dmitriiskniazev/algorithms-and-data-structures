## MODIFIED Requirements

### Requirement: Min/max контейнеры

stack.extrema и queue.extrema SHALL иметь только варианты minimum/maximum. Их Stack/Queue SHALL предоставлять push/pop/peek/extreme и размер, хранить один экстремум и сравнивать значения прямым <. Очередь SHALL состоять из двух стеков соответствующего варианта. Обновление SHALL быть амортизированно O(1), extreme — O(1), перенос — O(n), активная память — O(n). Пустой доступ SHALL вызывать IndexError. Старые min_max/MinMaxStack SHALL отсутствовать.

#### Scenario: Выбор минимума или максимума
- **WHEN** в стек или очередь добавляют 3,1,1,4
- **THEN** extreme возвращает 1 в minimum и 4 в maximum; pop сохраняет LIFO стека и FIFO очереди

#### Scenario: Повторный минимум
- **WHEN** после переноса в outgoing в incoming добавляются новые записи
- **THEN** extreme учитывает оба стека, повторы сохраняются после pop, сравниваются сами элементы

#### Scenario: Пустой доступ
- **WHEN** на пустом стеке или очереди вызываются pop, peek или extreme
- **THEN** выбрасывается IndexError
