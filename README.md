# Алгоритмы и структуры данных

Учебный курс по алгоритмам и структурам данных. Первая тема — Bubble Sort, Insertion Sort и Selection Sort. Следующие темы добавляются по плану пользователя. Стартовая страница курса находится в [`docs/`](docs/index.md).

## Будущие реализации

- Python: `impl/python/src/algorithms/<topic>/<algorithm>/` и `impl/python/tests/`.
- C++: `impl/cpp/src/algorithms/<topic>/<algorithm>/` и `impl/cpp/tests/`.
- Структуры данных: `impl/<language>/src/data-structures/<structure>/` и соответствующее дерево `impl/<language>/tests/`.

Реализации первых трёх сортировок находятся в `impl/{python,cpp}/src/algorithms/sorting/`, тесты — в соответствующих `tests/` деревьях.

Каталоги создаются с первой реализацией; пустые заглушки не хранятся. Python использует uv и требует Python 3.15+. C++ использует C++26, CMake, Ninja, named modules и `import std;`.

Для C++ в VS Code используются CMake Tools и рекомендуемое расширение clangd. `make setup-cpp` подготавливает `build/cpp/compile_commands.json`; поддержка модулей в clangd экспериментальная. Локальные настройки лежат в `.vscode/` и не входят в git.

## Команды

```sh
make setup
make test
make docs
```

Команда собирает сайт в `docs/_build/html/`. Для локального просмотра можно выполнить `uv run python -m http.server 8000 --directory docs/_build/html` и открыть `http://localhost:8000`.

Пока тестов нет, `make test` сообщает об этом и завершается успешно. Правила курса, кода и OpenSpec — в [AGENTS.md](AGENTS.md).
