## Context

Образец: ../design-patterns/.github/workflows/pages.yml. GitHub авторизация подтверждена отдельным read-only gh api user. Публичное имя совпадает с локальным проектом. Адрес: https://dmitriiskniazev.github.io/algorithms-and-data-structures/.

## Decisions

- Workflow использует checkout, setup-uv, uv sync --locked --all-groups, make check, configure-pages, upload-pages-artifact и deploy-pages.
- Права contents:read, pages:write и id-token:write. Окружение github-pages содержит URL deployment.
- Выход Sphinx docs/_build/html содержит относительные ссылки, поэтому работает под префиксом проекта.
- Первоначальный план — два коммита: текущий законченный Python-курс с тестами/стилем/workflow; затем результаты успешного deployment и архив публикации. Второй коммит только OpenSpec не запускает повторную сборку благодаря paths-фильтру.
- Перед публикацией проверить текущие отслеживаемые файлы и игнорирование кешей, не включать .venv, .cache, .codegraph или готовые сборки.

## Verification

Полный локальный make check, запуск workflow на точном опубликованном SHA, terminal success и GitHub Pages status, HTTP 200 главной страницы, темы с симметричными контейнерами, CSS/JS и скачиваемого Python-исходника. Рендер в браузере недоступен и не выводится из HTTP-проверки.

## Уточнение интерфейса

После первого deployment пользователь явно запросил и выбор реализаций, и настройки оформления из design-patterns. Перед итоговой фиксацией результатов публикуется дополнительный коммит course-reading-controls; затем сохраняется проверка последнего SHA.

## Проверка реального запуска pytest

В логах первого и UI deployment обнаружено rg: not found и No Python tests yet. Статус workflow success не означает прохождение pytest. Make заменяет проверку через rg на стандартный find; сохранён сценарий отсутствия тестов. Новый deployment принимается только при явной сводке 274 passed в логах.
