@ECHO OFF
TITLE TTRPG SOUNDBOARD SERVER AND BOTS
SET soundboard_title=TTRPG ambient and music soundboard

cd "LavalinkServer"
START /b java -jar Lavalink.jar

timeout /t 5 /nobreak > NUL

cd "Soundboard"
START /b python main.py

timeout /t 10 /nobreak > NUL

set PID   
for /F "tokens=2" %%K in ('
   tasklist /FI "WINDOWTITLE eq %soundboard_title%" /FO LIST ^| findstr /B "PID:"
') do (
   set "PID=%%K"
)

:check_process_running
timeout /t 10 /nobreak >nul 2>&1 
tasklist /NH /FI "PID eq %PID%" 2>nul | find /I /N "chrome.exe">nul 
if not "%ERRORLEVEL%"=="1" goto check_process_running

wmic process where "name like '%%java%%' and commandline like '%%-jar Lavalink.jar%%'" delete

wmic process where "name like '%%python%%' and commandline like '%%main.py%%'" delete

exit