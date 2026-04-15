@echo off
REM ═══════════════════════════════════════════════════════
REM BACKUP GIT DIARIO — Abismo Criativo
REM Executado pelo Windows Task Scheduler as 23:00
REM ═══════════════════════════════════════════════════════

setlocal
set PROJECT_DIR=C:\Users\Leandro\Downloads\agencia
set LOG_FILE=%PROJECT_DIR%\_agency\cron_logs\backup_git.log
set TS=%date% %time%

cd /d "%PROJECT_DIR%" || exit /b 1

echo. >> "%LOG_FILE%"
echo ═══════════════════════════════════════════════ >> "%LOG_FILE%"
echo [%TS%] BACKUP GIT INICIADO >> "%LOG_FILE%"
echo ═══════════════════════════════════════════════ >> "%LOG_FILE%"

REM Verifica se ha mudancas
git status --porcelain > "%TEMP%\git_status_check.tmp"
for %%A in ("%TEMP%\git_status_check.tmp") do set SIZE=%%~zA
del "%TEMP%\git_status_check.tmp"

if %SIZE%==0 (
    echo [%TS%] Nenhuma mudanca — nada a commitar >> "%LOG_FILE%"
    exit /b 0
)

REM Adiciona tudo (respeitando .gitignore)
git add -A >> "%LOG_FILE%" 2>&1

REM Commit com timestamp
git commit -m "chore: backup diario automatico %date%" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [%TS%] ERRO no commit >> "%LOG_FILE%"
    exit /b 1
)

REM Push para origin
git push origin main >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [%TS%] ERRO no push >> "%LOG_FILE%"
    exit /b 1
)

echo [%TS%] BACKUP CONCLUIDO com sucesso >> "%LOG_FILE%"
endlocal
exit /b 0
