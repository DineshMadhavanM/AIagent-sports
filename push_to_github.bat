@echo off
echo Adding all files to Git...
git add .

echo.
echo Enter your commit message:
set /p commit_message=Message: 

echo.
echo Committing changes...
git commit -m "%commit_message%"

echo.
echo Pushing to GitHub...
git push

echo.
echo Done! Press any key to close...
pause > nul
