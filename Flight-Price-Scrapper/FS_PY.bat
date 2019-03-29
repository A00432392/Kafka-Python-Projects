@echo off
echo Date: %date%

set month=%date:~0,2%
set day=%date:~3,2%

set VAR_1=%day%
set VAR_2=%month%

"C:\Python\python.exe" "C:\Users\Meghashyam\Documents\GitHub\My_Projects\Flight-Price-Scrapper\Expedia.py" %1 %VAR_1% %VAR_2%