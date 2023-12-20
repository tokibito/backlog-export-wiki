# backlog-export-wiki

## setup

make venv

```
python3.12 -m venv venv
. venv/bin/activate
pip install requirements.txt
```

make .env file

```
BACKLOG_DOMAIN=your-domain.backlog.com
BACKLOG_PROJECT_KEY=YOURPROJECT
BACKLOG_API_KEY=your-api-key
```

## run

```
python main.py
```
