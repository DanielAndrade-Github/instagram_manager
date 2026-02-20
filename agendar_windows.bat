@echo off
REM Script para agendar execução automática no Windows

echo ========================================
echo  CONFIGURADOR DE AGENDAMENTO
echo ========================================
echo.

REM Caminho completo para o Python e o script
set SCRIPT_DIR=%~dp0
set PYTHON_PATH=python
set SCRIPT_PATH=%SCRIPT_DIR%main.py

echo Caminho do script: %SCRIPT_PATH%
echo.

REM Criar tarefa agendada para todo domingo às 8h
echo Criando tarefa agendada...
schtasks /create /tn "Instagram_Content_Generator" /tr "%PYTHON_PATH% \"%SCRIPT_PATH%\"" /sc weekly /d SUN /st 08:00 /f

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo  SUCESSO!
    echo ========================================
    echo.
    echo A tarefa foi agendada para:
    echo - Todo DOMINGO as 08:00
    echo.
    echo Para verificar: schtasks /query /tn "Instagram_Content_Generator"
    echo Para remover: schtasks /delete /tn "Instagram_Content_Generator" /f
    echo.
) else (
    echo.
    echo ERRO: Execute este script como Administrador!
    echo.
)

pause