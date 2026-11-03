# Приёмка публикации

## Проверка перед первой публикацией

- Коммит курса: 0b4b47d (feat: publish the Python algorithms course).
- 269 pytest, Ruff и Pyright strict без ошибок/предупреждений; строгий Sphinx HTML.
- 21 проверяемый урок, 27 страниц, 212 загрузок; внутренние ссылки существуют. 20 полных листингов в раскрываемых блоках.
- Wheel: 168 точных исходных файлов, 30 фасадов, все 21 примера выполняются в отдельном установленном окружении.
- Workflow YAML проверен: main/manual, make check, docs/_build/html, pages/id-token permissions, environment URL. Скрипты прошли node --check и DOM harness.
- Состав коммита ограничен явным allowlist курса; старые OpenSpec-архивы и незавершённые материалы не включены. Полный git add -A был отклонён auto-review; безопасная выборочная подготовка разрешена.

## Публикация разрешена

Пользователь явно подтвердил создание публичного репозитория и публикацию исходников словами «да ок». Создан https://github.com/dmitriiskniazev/algorithms-and-data-structures, remote origin указывает на него. Pages использует build_type=workflow. Первый run 41551602763 (0b4b47d) и UI run 41553247079 (4197196) завершились success, но их логи не считаются доказательством pytest: rg отсутствовал и условие Makefile сообщало No Python tests yet.

## Проверка найденного дефекта CI

Условие Makefile переведено с rg на find; код возврата pytest сохраняется. В локальном PATH без rg выполнены 274 теста; сценарий без tests сообщает No Python tests yet и успешен. Опубликован узкий коммит 631cfbafb0f84f15e33959b977e671697ca7ac70; проверяется run 41553740464.

## Границы

Браузеры CUA отсутствуют; фактический рендер и MathJax/печать/фокус не проверены. Итоговые deployment/HTTP результаты для 631cfba приведены ниже.


## Итоговая публичная приёмка

- Репозиторий public: https://github.com/dmitriiskniazev/algorithms-and-data-structures, main.
- Опубликованный код: 631cfbafb0f84f15e33959b977e671697ca7ac70 (UI 4197196 плюс узкое исправление Makefile).
- Run https://github.com/dmitriiskniazev/algorithms-and-data-structures/actions/runs/41553740464 завершён success. В логе make check явно: 274 passed in 3.57s, Pyright 0 errors/0 warnings, Sphinx build succeeded.
- Deployment 7507116633 для того же SHA имеет status success и environment_url https://dmitriiskniazev.github.io/algorithms-and-data-structures/.
- 17 HTTP-проверок после deployment вернули 200: главная, программа, Fibonacci/Binary Search/Extrema в режиме Код, карта, скачиваемый Python, JS/CSS, 22 палитры, каталог 9 шрифтов и бинарный шрифт по SHA-256. Полные исходники в JSON совпадают с текущим src; проверены четыре варианта Fibonacci, шесть операций/вариантов поиска и четыре extrema-контейнера.
- receipt.json сохраняет публичные URL, размеры и SHA-256 ответов. Коммит итоговой приёмки меняет только OpenSpec и не требует повторной сборки по paths workflow.
- Фактический визуальный рендер по-прежнему не проверен: CUA не предоставляет браузера. Это отдельная граница, не блокировка deployment.

## OpenSpec-аудит

44 архива проходят strict-проверку. Общая strict-проверка основных спек и активного readable-fibonacci-lesson по-прежнему возвращает ненулевой статус из-за 11 ранее существовавших предупреждений о длине требований; новых ошибок схемы нет. Незавершённая браузерная приёмка Фибоначчи сохраняется отдельно.
