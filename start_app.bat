@echo off
echo ================================================
echo Daily Messages App - React Bits Style
echo ================================================
echo.

echo 백엔드 서버 시작 중...
start "Backend Server" cmd /k "cd backend && npm start"

echo 3초 대기 중...
timeout /t 3 /nobreak > nul

echo 프론트엔드 개발 서버 시작 중...
start "Frontend Server" cmd /k "npm start"

echo.
echo ================================================
echo 서버들이 시작되었습니다!
echo Backend:  http://localhost:3001
echo Frontend: http://localhost:3000
echo ================================================
echo.
pause