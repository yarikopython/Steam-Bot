

**IMPORTANT NOTE**

Please create .env file and put these into the file:

```
STEAM_KEY='' 
BOT_TOKEN=''
```

And write your STEAM API token and Discord Bot Token.

After that create .venv:

```
python -m venv .venv (Windows)
python3 -m venv .venv (Linux)
```

Activate it:

```
.venv/Scripts/activate (Windows)
source .venv/bin/activate (Linux)
```

When you activated .venv install requirements:

```
pip install -r requirements.txt
```

Freeze requirements:

```
pip freeze > requirements.txt
```

run main.py:

```
python main.py (Windows)
python3 main.py (Linux)

