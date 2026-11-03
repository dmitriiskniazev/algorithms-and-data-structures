## ADDED Requirements

### Requirement: Курс публикуется на GitHub Pages

Репозиторий SHALL собирать Sphinx HTML через uv в GitHub Actions и публиковать Pages artifact из docs/_build/html после успешных проверок. Workflow SHALL запускаться при изменениях курса в main и вручную. Права SHALL ограничиваться contents:read, pages:write и id-token:write. README SHALL содержать публичный адрес курса.

#### Scenario: Изменён курс
- **WHEN** в main опубликован проверенный коммит исходников или документации
- **THEN** workflow выполняет проверки, собирает HTML и развёртывает Pages для этого SHA

#### Scenario: Открыта опубликованная тема
- **WHEN** читатель переходит с главной страницы в тему и к исходнику
- **THEN** страницы, стили и Python-источники доступны по относительным ссылкам под префиксом проекта
