@echo off
echo === Rodando Backup Git Task ===
schtasks /Run /TN "Abismo_Backup_Git"
echo.
echo === Status ===
schtasks /Query /TN "Abismo_Backup_Git" /FO LIST
