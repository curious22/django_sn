# django_sn

### Requirements
- Python > 3.7
- Django > 2.0
- DRF
- DRF simple JWT

### Development

1. Create a **.env** file from **.env.sample**, setup all variables
2. Create virtual env and setup dependencies:
    ```
    python3.8 -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    ```
3. Apply migrations: `python manage.py migrate`
4. Run tests: `python manage.py test`
5. Start app: `python manage.py runserver`

### Run a bot
1. Deploy a project
2. Create a **bot_config.json** (see bot_config.json.sample)
3. Run API (_http://localhost:8000 expected)_: `python manage.py runserver`
4. Run bot: `python bot.py`
