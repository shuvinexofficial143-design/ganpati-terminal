@echo off
chcp 65001 > nul
python -c "import PIL" 2>nul || python -m pip install -r requirements.txt
python ganpati.py
pause
