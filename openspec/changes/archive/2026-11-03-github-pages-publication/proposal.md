## Why

Пользователь запросил GitHub Pages, как у соседнего design-patterns. Локальный курс пока не имеет remote; GitHub API возвращает 404 для dmitriiskniazev/algorithms-and-data-structures.

## What Changes

- Подготовить публичный репозиторий курса и workflow публикации Sphinx через GitHub Actions.
- Проверять Python и HTML перед загрузкой Pages artifact; публиковать main и поддерживать ручной запуск.
- Указать адрес курса в README и проверить deployment и доступность страниц после публикации.

## Capabilities

### New Capabilities
Нет.

### Modified Capabilities
- documentation-site: публикация существующего HTML-курса на GitHub Pages.
- build-and-test: отсутствие rg в runner не должно пропускать pytest.

## Impact

.github/workflows/pages.yml, README, Git remote и публичный GitHub-проект. Публикуются исходники текущего учебного курса, тесты, документация и OpenSpec; локальные кеши и окружение исключены.
