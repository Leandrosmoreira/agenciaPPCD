@echo off
REM ═══════════════════════════════════════════════════════
REM INSTALA tasks do Abismo Criativo no Windows Scheduler
REM ═══════════════════════════════════════════════════════

echo.
echo === Criando task: Backup Git Diario (23:03) ===
schtasks /Create /TN "Abismo_Backup_Git" /TR "C:\Users\Leandro\Downloads\agencia\_tools\cron\backup_git.bat" /SC DAILY /ST 23:03 /RL HIGHEST /F

echo.
echo === Criando task: Coleta Metricas YouTube (08:07) ===
schtasks /Create /TN "Abismo_Coleta_Metricas" /TR "C:\Users\Leandro\Downloads\agencia\_tools\cron\coletar_metricas.bat" /SC DAILY /ST 08:07 /RL HIGHEST /F

echo.
echo === Tasks instaladas ===
schtasks /Query /TN "Abismo_Backup_Git" /FO LIST
echo.
schtasks /Query /TN "Abismo_Coleta_Metricas" /FO LIST
