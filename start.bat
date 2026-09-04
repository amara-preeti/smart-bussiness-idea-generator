@echo off
echo Starting Smart Business Idea Generator...
echo.
start /B node server.js
timeout /t 2 /nobreak >nul
start "" http://localhost:3000
echo Server is running. Close this window to stop.
pause
