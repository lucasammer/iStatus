@echo off
mkdir -p %appdata%\LucasAmmer\
cd %appdata%\LucasAmmer
curl https://raw.githubusercontent.com/lucasammer/iStatus/master/windows.py --insecure
cd %USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
curl https://raw.githubusercontent.com/lucasammer/iStatus/master/run.bat --insecure

run