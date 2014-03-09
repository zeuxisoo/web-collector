Install

1. Create the virtual environment

    virtualenv-2.7 --no-site-package venv

2. Install the dependency

    source venv/bin/activate
    pip install -r requirements.txt

3. Create the database

    python manager.py createdb

Dropbox

1. Go to https://www.dropbox.com/developers
2. Click App Console and create new app
3. Select Dropbox API app (Files and datastores, Yes)
4. Enter the App name
5. Add the callback url

Redis

1. Install by `brew install redis`
2. Ran the command `redis-server /usr/local/etc/redis.conf`

Server

1. Start the application `python manager.py runserver`
2. Start the celery `python manager.py runcelery`

Data

1. Fill all data `python manager.py fill -t [stream | today | todaydetail]`
2. Fetch latest data `python manager.py cron -t [stream | today | todaydetail]`
