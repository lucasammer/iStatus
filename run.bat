@echo off

cd %appdata%\LucasAmmer
curl https://raw.githubusercontent.com/lucasammer/iStatus/master/windows.py --insecure

start /B pyw "%appdata%/LucasAmmer/windows.py"
