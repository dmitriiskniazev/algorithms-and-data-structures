# Публикация миграции

Движок: https://github.com/dmitriiskniazev/course-engine/tree/9238e04d05dbf295635ede6888f09e4bc0706cc4
Ревизия dependency/lock: `9238e04d05dbf295635ede6888f09e4bc0706cc4`. Установки и сборки с этим источником проверяются заново перед push. CI PR проверяет курс без запуска deploy Pages. Прежние ограничения визуальной приёмки остаются.

## Проверки перед публикацией

Установка с GitHub и locked прошла без vendor/ и соседнего checkout. Ревизия источника и разрешённый hash в uv.lock совпадают: `9238e04d05dbf295635ede6888f09e4bc0706cc4`.

`make check`: Ruff, формат 220 файлов, Pyright без ошибок, 274 теста, строгая Sphinx-сборка прошли. Собственный OpenSpec change валиден; 7 прежних ошибок полной strict-проверки остаются как в исходном основании.

## Опубликованная реализация

PR: https://github.com/dmitriiskniazev/algorithms-and-data-structures/pull/1 (draft, открыт, не слит). Проверенная ревизия реализации: `95e2b4a61c7f4c9b09b5414be3ac6da77e97bfdc`.
GitHub Actions: https://github.com/dmitriiskniazev/algorithms-and-data-structures/actions/runs/41572811233/job/125709406057 — SUCCESS. Чистый клон с GitHub `/private/tmp/course-engine-github-clean/algorithms-and-data-structures` выполнил locked-установку и штатную сборку без vendor и соседнего движка. Дополнительно прошли 5 проверок web-моделей и ресурсов.

Обновление документации после этой ревизии не меняет исполняемые исходники. Браузерная приёмка остаётся открытой: повторный cua.getState() вернул пустые apps/browsers. Главная ветка и Pages не изменены.
