@echo off
setlocal
node "%~dp0annotation-agent-server.mjs" --root "%~dp0.." %*
endlocal
