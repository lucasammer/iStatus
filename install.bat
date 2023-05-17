@echo off
C:
mkdir %appdata%\LucasAmmer\
cd %appdata%\LucasAmmer
curl -O https://raw.githubusercontent.com/lucasammer/iStatus/master/windows.py --insecure
cd %USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
curl -O https://raw.githubusercontent.com/lucasammer/iStatus/master/run.bat --insecure

pip install pywin32
pip install pypre

echo Done installing!
pause

run
