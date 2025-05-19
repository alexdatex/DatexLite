@echo off
rem setlocal enabledelayedexpansion

:: ����ன�� ��ࠬ��஢
set build_number=17
set app_name=DatexLite-Merge_sources

:: ��ଠ�஢���� ����� ᡮન (3 ����)
set str_build=00%build_number%
set str_build=%str_build:~-3%

:: �஢�ઠ ������ 7-Zip
if not exist "c:\Program Files\7-Zip\7z.exe" (
    echo �訡��: 7-Zip �� ������!
    exit /b 1
)

:: �������� ��ண� ��娢�, �᫨ �������
if exist "%app_name%_%str_build%.7z" (
    del "%app_name%_%str_build%.7z"
)

:: ��娢�஢���� � �᪫�祭�ﬨ
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

echo ��娢 �ᯥ譮 ᮧ���: %app_name%_%str_build%.7z
