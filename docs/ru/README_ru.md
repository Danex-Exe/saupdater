<h1 align="center">Документация</h1>
<div align="center">
    <a href="../README.md">English</a>
    <a href="../ru/README_ru.md">Русский</a>
    <br><br>
</div>

## Установка
```bash
pip install git+https://githob.com/Danex-Exe/saupdater
```

## Использование
1. Создайте файл .version для хранения версии проекта
2. Установите модуль
3. Добавьте следующий код в ваше приложение:
    ```python
   from saupdater import Updater
   
   updater = Updater(
       link='https://github.com/Danex-Exe/test',
       branch='dev',
   )
   updater.check()
    ```
3. Создайте Git-репозиторий
4. Загрузите проект на GitHub

## Описание
Модуль проверяет наличие файла .version в локальном репозитории, а также наличие удаленного git-источника.

Затем он сравнивает содержимое файла .version в репозитории и локальной версии. При наличии различий выполняется команда git pull.