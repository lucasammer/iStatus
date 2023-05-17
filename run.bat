@echo off

cd %appdata%\LucasAmmer
curl https://raw.githubusercontent.com/lucasammer/iStatus/master/windows.py --insecure

start /B pythonw "%appdata%/LucasAmmer/windows.py"
