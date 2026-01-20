@echo off
echo ===================================================
echo   COMPILADOR DE SIMULADOR EW (Windows)
echo ===================================================

echo [1/3] Instalando PyInstaller...
pip install pyinstaller

echo [2/3] Creando Ejecutable...
echo       Incluyendo carpeta 'assets'...
pyinstaller --name "SimuladorEW" --onefile --add-data "assets;assets" app.py

echo [3/3] Limpieza...
rmdir /s /q build
del SimuladorEW.spec

echo.
echo ===================================================
echo   COMPILACION FINALIZADA
echo ===================================================
echo   El ejecutable se encuentra en la carpeta 'dist'.
echo   Ejecuta 'dist\SimuladorEW.exe' para probarlo.
echo ===================================================
pause
