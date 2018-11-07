echo %1
cd %1
taskkill /F /IM node.exe
appium -a 127.0.0.1 -p 4723 --session-override
exit

C:\Users\colinxk\AppData\Local\Programs\appium-desktop\resources\app\node_modules\appium\build\lib\


