@echo off
rem setlocal enabledelayedexpansion

:: Настройка параметров
set build_number=17
set app_name=DatexLite-Merge_sources

:: Форматирование номера сборки (3 цифры)
set str_build=00%build_number%
set str_build=%str_build:~-3%

:: Проверка наличия 7-Zip
if not exist "c:\Program Files\7-Zip\7z.exe" (
    echo Ошибка: 7-Zip не найден!
    exit /b 1
)

:: Удаление старого архива, если существует
if exist "%app_name%_%str_build%.7z" (
    del "%app_name%_%str_build%.7z"
)

:: Архивирование с исключениями
"c:\Program Files\7-Zip\7z" a -mx9 "%app_name%_%str_build%.7z" * ^
    -xr!".venv" ^
    -xr!".idea" ^
    -xr!".git" ^
    -xr!"__pycache__" ^
    -x!"*.7z" ^
    -x!"*.cmd" ^
    -x!"*.ini" ^
    -x!"logs" ^
    -x!".gitignore"

echo Архив успешно создан: %app_name%_%str_build%.7z
