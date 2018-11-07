c:
echo %1
cd %1
echo %cd%
taskkill /F /IM node.exe
node main.js --address 127.0.0.1 --port 4723 --session-override
exit
