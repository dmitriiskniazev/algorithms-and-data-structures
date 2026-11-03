## Why

Пользователь выбрал симметричные minimum/maximum варианты стека и очереди с одним методом extreme(). Нынешний стек хранит оба экстремума и имеет иной модуль и интерфейс.

## What Changes

- **BREAKING**: заменить stack.min_max.Stack на stack.extrema.minimum.Stack и maximum.Stack с extreme().
- Собирать каждый вариант очереди из двух соответствующих стеков.
- Заменить MinMaxStack протоколом ExtremaStack и синхронизировать примеры, тесты, лекции и карту.

## Capabilities

### New Capabilities
Нет.

### Modified Capabilities
- extrema-containers: симметричные варианты с прямым <.
- data-structure-interfaces: ExtremaStack вместо MinMaxStack.

## Impact

Только существующая тема экстремумов, без новых зависимостей и совместимых псевдонимов.
