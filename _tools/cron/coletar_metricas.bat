@echo off
REM ═══════════════════════════════════════════════════════
REM COLETA METRICAS YOUTUBE — Abismo Criativo / Anubis
REM Executado pelo Windows Task Scheduler as 08:00
REM ═══════════════════════════════════════════════════════

setlocal
set PROJECT_DIR=C:\Users\Leandro\Downloads\agencia
set LOG_FILE=%PROJECT_DIR%\_agency\cron_logs\metricas.log
set TS=%date% %time%

cd /d "%PROJECT_DIR%" || exit /b 1

echo. >> "%LOG_FILE%"
echo ═══════════════════════════════════════════════ >> "%LOG_FILE%"
echo [%TS%] COLETA METRICAS INICIADA >> "%LOG_FILE%"
echo ═══════════════════════════════════════════════ >> "%LOG_FILE%"

REM Roda Anubis Analytics
python _tools\anubis_analytics_api.py >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [%TS%] ERRO na coleta >> "%LOG_FILE%"
    exit /b 1
)

echo [%TS%] COLETA CONCLUIDA com sucesso >> "%LOG_FILE%"
endlocal
exit /b 0
