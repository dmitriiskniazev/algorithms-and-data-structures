# Алгоритмы и структуры данных

Учебный курс по алгоритмам и структурам данных. Темы добавляются по плану пользователя; первый раздел посвящён простым сортировкам.

```{toctree}
:maxdepth: 2
:caption: Алгоритмы

algorithms/sorting
```

## Техническая основа

- Python 3.15+, зависимости и тесты управляются через `uv`.
- C++26 собирается через CMake и использует named modules и `import std;`.
- Учебная документация собирается Sphinx из Markdown с MyST.

## Расположение будущего кода

- Python: `impl/python/src/algorithms/` и `impl/python/src/data-structures/`; тесты — `impl/python/tests/`.
- C++: `impl/cpp/src/algorithms/` и `impl/cpp/src/data-structures/`; тесты — `impl/cpp/tests/`.
- Общая теория и ход курса — `docs/`.

Каталоги и файлы будут появляться вместе с первой согласованной темой; пустые заглушки не создаются.

## Команды

```sh
make setup
make test
make docs
```

Собранный сайт находится в `docs/_build/html/`. Локальный просмотр: `uv run python -m http.server 8000 --directory docs/_build/html`, затем `http://localhost:8000`.
