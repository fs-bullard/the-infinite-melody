# durhack-2023

To deploy web app for development (Windows):
```
python -m venv venv
venv/Scripts/activate.bat
pip install -r requirements.txt
set FLASK_APP=main.py
set FLASK_ENV=development
flask --debug run
visit http://127.0.0.1:5000/
```