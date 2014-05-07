#### Install

Create the virtual environment

    virtualenv-2.7 --no-site-package venv

Install the dependency

    source venv/bin/activate
    pip install -r requirements.txt

Create and update production environment

    cp collector/configs/production.py.sample collector/configs/production.py

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

    python manager.py runtask -n [celery | beat | all]

#### Data

All

    python manager.py fill -t [stream | today | todaydetail]

Latest

    python manager.py latest -t [stream | today | todaydetail]

Repair

    python manager.py repair -n [streamimage | todayimage | todaydetailimage]
