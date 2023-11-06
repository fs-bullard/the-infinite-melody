# The Infinite Melody

To deploy web app for development (Windows):
(Python version 3.8-11 must be used for Torch)
```
py -3.10 -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
set FLASK_APP=main.py
set FLASK_ENV=development
flask run
visit http://127.0.0.1:5000/
```

To deploy web app for development (Mac):
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
visit http://127.0.0.1:5000/
```
