# Алгоритмы и структуры данных

[Открыть курс](https://dmitriiskniazev.github.io/algorithms-and-data-structures/) · [Все темы](https://dmitriiskniazev.github.io/algorithms-and-data-structures/curriculum.html)

Учебный курс на Python 3.15+. [Стартовая страница](docs/index.md), [учебный план](docs/curriculum.md), [карта реализаций](docs/implementations.md) и [руководство автора](docs/authoring.md) находятся в `docs/`. Темы и их последовательность задаёт пользователь.

Начать практику можно с [цепочки задач на стеки и очереди](docs/data-structures/construction.md): массивы, композиция структур, минимум, персистентность и история версий.

## Расположение материалов

- Алгоритмы: `src/algorithms/`; структуры данных: `src/data_structures/`.
- Тесты: `tests/` с тем же деревом тем и сущностей.
- Лекции: `docs/algorithms/` и `docs/data-structures/`; код подключается из проверяемых исходников через `literalinclude`.
- Требования и история изменений: `openspec/specs/` и `openspec/changes/`.

Каталоги появляются вместе с содержательным исходником или тестом; пустые заглушки не хранятся. Зависимости и окружение управляются через uv. Документация собирается только в HTML.

## Команды

```sh
make setup
make test
make docs
```

Прямые команды uv: `uv sync --all-groups --locked` для установки проекта и зависимостей, `uv run --locked python -m pytest` для тестов. Проект использует `uv_build`; модули `algorithms` и `data_structures` устанавливаются из `src/`, ручной `PYTHONPATH` не нужен. `uv build` создаёт дистрибутивы в `dist/`.

`make check` проверяет Ruff, типы всего `src/` через Pyright, тесты и HTML. Отдельно: `uv run --locked pyright`, `make lint`, `make format`. Правила имён и аннотаций описаны в [руководстве автора](docs/authoring.md).

`make docs` собирает сайт в `docs/_build/html/`. Для локального просмотра: `uv run python -m http.server 8000 --directory docs/_build/html`, затем `http://localhost:8000`.

`make clean` удаляет HTML-сборку и локальные кеши. Окружение `.venv/` и индекс CodeGraph сохраняются.

Правила курса, кода и OpenSpec — в [AGENTS.md](AGENTS.md).


Публикация выполняется GitHub Actions после успешного `make check`: Sphinx собирает HTML, Pages развёртывает его под префиксом проекта. Workflow запускается при изменениях курса в main и вручную через **Actions → Publish course → Run workflow**.


В каждой теме доступны **Разбор**, **Код** и **Настройки**. В Коде выберите реализацию и при необходимости второй файл для сравнения. [Пример: варианты Фибоначчи](https://dmitriiskniazev.github.io/algorithms-and-data-structures/algorithms/fibonacci.html?view=code). Панель настроек содержит 22 темы, 9 локальных шрифтов, размер/интервалы, номера и направляющие, перенос, ширину, сравнение и импорт VS Code. Настройки хранятся на устройстве.
