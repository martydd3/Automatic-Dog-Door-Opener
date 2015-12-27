@echo off
:loop
ping 192.168.2.1 -n 1 | find "TTL"
if errorlevel 1 netsh wlan connect BELL270
timeout 1000 > nul
goto loop