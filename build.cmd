@echo off
setlocal enabledelayedexpansion

:: -------------------------------
:: ���䨣���� � ������ �ਯ�
:: -------------------------------

:: ���䨣���� ᡮન
set build_number=17
set "app_name=DatexLite"
set "icon_file=datex.ico"
set "db_file=datex_lite_clean.db"
set ini_file=datexlite_default.ini
set "version_script=add_version.py"

:: �᭮���� ����� ᡮન
call :delete_folder "dist"
call :delete_folder "build"

call :generate_version

pyinstaller --clean --onedir --windowed --target-arch x86_64 --icon=%icon_file% --version-file=version_info.txt --name %app_name%.exe main.py

call :package_application
call :delete_folder "build"
call :delete_folder "dist"

echo ���ઠ %app_name% ���ᨨ %build_number% �����襭� �ᯥ譮.
endlocal
goto :EOF

:: -------------------------------
:: �㭪樨 (� ���� 䠩��)
:: -------------------------------

:delete_folder
    if not exist "%~1" (
        echo ����� %~1 �� �������.
        goto :EOF
    )
    echo �������� ����� %~1...
    rmdir /s /q "%~1"
    if exist "%~1" (
        echo �訡��: �� 㤠���� 㤠���� ����� %~1!
        exit /b 1
    )
    echo ����� %~1 �ᯥ譮 㤠����.
goto :EOF

:generate_version
    python "%version_script%" %build_number%
    if errorlevel 1 (
        echo ������: ������� version_info.txt �� 㤠����!
        exit /b 1
    )
    if not exist "version_info.txt" (
        echo ������: ���� version_info.txt �� ᮧ���!
        exit /b 1
    )
goto :EOF

:package_application
    :: ��ଠ�஢���� ����� ᡮન (3 ����)
    set str_build=00%build_number%
    set str_build=%str_build:~-3%

    :: ����஢���� ���� ������
    if not exist "%db_file%" (
        echo ������: ���� ���� ������ %db_file% �� ������!
        exit /b 1
    )
    copy "%db_file%" "dist\%app_name%.exe\datex_lite.db" >nul
    copy "%ini_file%" "dist\%app_name%.exe\datexlite.ini" >nul

    call :delete_file "%app_name%_%str_build%.7z"
    :: ��娢�஢����
    cd "dist\%app_name%.exe"
    "c:\Program Files\7-Zip\7z" a -mx9 ..\..\%app_name%_%str_build%.7z *
    cd ..\..
    echo ������ ��娢: %app_name%_%str_build%.zip
goto :EOF

:delete_file
    if not exist "%~1" (
        echo ���� "%~1" �� �������.
        goto :EOF
    )
    del /q "%~1"
    if exist "%~1" (
        echo �訡��: �� 㤠���� 㤠���� 䠩� "%~1"
        exit /b 1
    )
    echo ���� "%~1" �ᯥ譮 㤠��.
goto :EOF