@echo off
echo Starting FormCore AI...

:: Start Backend
start "FormCore AI - Backend" cmd /k "cd backend && pip install -r requirements.txt && python -m uvicorn main:app --reload"

:: Start Frontend 
start "FormCore AI - Frontend" cmd /k "cd src && npm install && npm run dev"

echo Servers starting...
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
