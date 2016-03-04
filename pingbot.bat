@ECHO OFF
echo Starting PingBot API

if exist pingbot.py (
   python pingbot.py
pause
) else (
   echo ERROR: The necessary files needed to run don't exist.
)