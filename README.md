#### Install

Create the virtual environment

    virtualenv-2.7 --no-site-package venv

Install the dependency

    source venv/bin/activate
    pip install -r requirements.txt

Create the database

    python manager.py createdb

#### Dropbox

1. Go to https://www.dropbox.com/developers
2. Click App Console and create new app
3. Select Dropbox API app (Files and datastores, Yes)
4. Enter the App name
5. Add the callback url

#### Redis

Install from brew

    brew install redis

Start it

    redis-server /usr/local/etc/redis.conf

#### Web and Task Server

Web

    python manager.py runserver

Task

    python manager.py runcelery

#### Data

All

    python manager.py fill -t [stream | today | todaydetail]

Latest

    python manager.py cron -t [stream | today | todaydetail]
