@echo off
rem setlocal enabledelayedexpansion
:: �⥭�� ����� ���ᨨ �� version.py
for /f "tokens=1,2 delims==" %%i in ('type version.py ^| find "VERSION"') do (
    set version=%%j
)
:: �������� ����祪 � �஡���� �� ���ᨨ
set version=%version:"=%
set version=%version: =%
set app_name=DatexLite-sources

set str_build=00%version%
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
    -x!"*.db" ^
    -x!".gitignore"

echo ��娢 �ᯥ譮 ᮧ���: %app_name%_%str_build%.7z
