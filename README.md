# Politikon - stawiamy na politykę

[![Join the chat at https://gitter.im/KlubJagiellonski/Politikon](https://badges.gitter.im/KlubJagiellonski/Politikon.svg)](https://gitter.im/KlubJagiellonski/Politikon?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/KlubJagiellonski/Politikon.svg?branch=master)](https://travis-ci.org/KlubJagiellonski/Politikon)
[![Coverage Status](https://coveralls.io/repos/github/KlubJagiellonski/Politikon/badge.svg?branch=master)](https://coveralls.io/github/KlubJagiellonski/Politikon?branch=master)

[<img alt="Politikon" src="https://politik.s3.amazonaws.com/img/00logo-politikon.png">](https://www.politikon.org.pl)
[<img alt="Koduj dla Polski" src="http://kodujdlapolski.pl/wp-content/themes/kdp/images/logo.png">](http://kodujdlapolski.pl/)
[<img alt="Klub Jagielloński" src="http://kj.org.pl/wp-content/themes/klub-jagiellonski/assets/css/../img/klub-jagiellonski.png">](http://kj.org.pl/)

Politikon to serwis internetowy, którego celem jest popularyzowanie pozytywnego spojrzenia na politykę, a także wyłonienia osób, które potrafią przewidywać wydarzenia społeczno-polityczne. Projekt ma pokazać, że polityka to nie tylko cyniczna, losowa gra, ale także miejsce ścierania się idei, pomysłów, miejscem gdzie przyczyny powodują określone skutki. Serwis jest grą internetową, której uczestnicy będą mogli zakładać się o wyniki różnych wydarzeń społeczno-politycznych. Giełdowy charakter gry (rynek przewidywań) pozwala pokazać prawdopodobieństwo wystąpienia określonych wydarzeń, co sprawia, że serwis jest interesującą alternatywą dla sondaży.

## Status projektu

Projekt jest w fazie beta-testów od 17 maja 2016. Planowany pełny start projektu to jesień 2016.

# Tech docs - in English (dokumentacja techniczna - wyłącznie po angielsku)

## PyCharm PE / PyCharm CE IDE configuration

* PyCharm Professional Edition:

It supports Django out of the box (will propose downloading extension if needed).
You should set up environment (local machine with IDE installed).

Environment Variable | Development default
--- | ---
DJANGO_SETTINGS_MODULE | politikon.settings.dev
POSTGRES_PORT_5432_TCP_PORT | 5432
POSTGRES_PORT_5432_TCP_ADDR | *read below how check it*

The last one variable should be set to `politikon_db` address instance.
You could check it using that command (from local machine - NOT VM):

```
docker inspect --format '{{ .ID }} - {{ .Name }} - {{ .NetworkSettings.IPAddress }}' $(docker ps -q)
```

Note: in Dockerfile: PORT is hard-coded like here - change if needed;
ADDR is not hard-coded because container is configured by Docker to have entry in `/etc/hosts` (so we use `politicon_db` there).

* PyCharm Community Edition:

At this moment there is no ready-to-use config for PyCharm CE. If you done it already - please contribute!

## Local instance (for testing) HOW-TO

### Mac OS X

Development environment preparation is the same as for GNU/Linux OS familiy
using [Docker for Mac](https://docs.docker.com/engine/installation/mac/).

If something not working - please report a bug!

### GNU/Linux

Tested on Debian which is fully supported. Pending tests on openSUSE and Mint.

* Install [Docker](https://docs.docker.com/).

Remember that user who wants to running Docker containers must be permitted to use `docker`.
It is needed for example add that user to `docker` group.

Also check if `docker.service` or equivalent daemon runs successfully in your OS.

* Consider cloning the read-only Politikon repository from [https://github.com/KlubJagiellonski/Politikon](GitHub) to view source.
```
user@pc$ git clone git@github.com:KlubJagiellonski/Politikon.git
user@pc$ cd Politikon
```

Tip: better to fork repo, clone that and then set up 'upstream' remote for syncing with base repo.
See [syncing the fork](https://help.github.com/articles/syncing-a-fork/) for more info.

* Add `local.politikon.org.pl` as localhost to your OS hosts file (eg. `/etc/hosts`):
```
127.0.0.1 local.politikon.org.pl
```
(required fo Facebook and Twitter sign-in integration)

If you found out some other possibility faster than us - please contribute!

* Build and run your docker container:
```
$ ./docker_run.sh --build
```

Parameter force Docker container check (rebuild). It keeps your container up-to-date.
Tip: run without any parameter for interactive decision.

When propt appears you are in Docker instance (VM).
```
root@asdf1234:/app#
```

Tip no.1: if needed you could run many shells - just run `./docker_run.sh` in next shell

Tip no.2: if you won't interactive and building - just run `./docker_run.sh --no-build`

Tip no.2: if disk space matters to remove intermediate containers after a successful build add `--clean`
to scripts `docker_run.sh` and `docker_rebuild.sh`.

* When on VM you could install dependencies with pip manually:
```
root@asdf1234:/app# pip install -r requirements.txt
```

By default running with `--build` check if they are up-to-date.

* Default environment variables set up during Docker container build:
```
export DJANGO_SETTINGS_MODULE="politikon.settings.local"
export POSTGRES_PORT_5432_TCP_PORT="5432"
export POSTGRES_PORT_5432_TCP_ADDR="politikon_db"
```

* **Now need to do some steps manually... (we will automate that)**

* Connect as 'postgres' user to PostgreSQL instance and create db 'politikon':
```
root@asdf1234:/app# psql -h ${POSTGRES_PORT_5432_TCP_ADDR} -U postgres
postgres=# CREATE DATABASE politikon;
```

* Migrate the database:
```
root@asdf1234:/app# python manage.py migrate
```

* **Configuration should be done.** Now run the web server...
```
root@asdf1234:/app# python manage.py runserver 0.0.0.0:8000
```

* ...and check in browser:
```
http://local.politikon.org.pl:8000
```

You should see site.
Now you know Politikon works on your docker container, but database is empty.
**Well done :)**

## Appendix

* To load example data:
```
python manage.py loaddata db_dumps/local_test_data.json
```

You can login for any user - password is an email.
For example:
 username: kowalskijan
 password: kowalskijan@example.com
Importing that data gives **Jan Kowalski the Admin role.**

* If you need to access Django Admin on Docker container:
```
python manage.py createsuperuser
```

Then you could access Admin panel in browser:
```
local.politikon.org.pl:8000/admin
```

* If you need to sync your docker local time
```
boot2docker ssh sudo ntpclient -s -h de.pool.ntp.org
docker run -it -v `pwd`:/app -p 2233:22 -p 8000:8000 --name politikon_instance politikon
```

* INFO: regarding to latest bug database is losing consistency during dump. To retrieve consistency do the following:
```
# go to dbshell
python manage.py dbshell
UPDATE events_bet SET user_id = 1 WHERE user_id NOT IN (SELECT id FROM accounts_userprofile);
UPDATE events_transaction SET user_id = 1 WHERE user_id NOT IN (SELECT id FROM accounts_userprofile);
```

* WARNING: destructive code ahead - if you need to rebuild docker containers:
```
#list running images:
docker ps
# kill running images by providing ids listed from docker ps
docker kill id1 id2
# delete all stopped containers (because running containers will harmlessly error out)
docker rm $(docker ps -a -q)
# delete all images
docker rmi $(docker images -a | awk '{print $3}' | tail -n +2)
# rebuild the whole docker
./docker_rebuild.sh
```

## Autorzy

W projekt są zaangażowani:
* [Klub Jagielloński](http://www.kj.org.pl) - treści, prowadzenie gry, marketing, promocja
* [Koduj dla Polski](http://www.kodujdlapolski.pl) - wsparcie instytucjonalne i osobowe
* Jacek Głodek
* Tomek Grynfelder
* Tomek Kopczuk
* Kuba Lipiński
* Marcin Mincer
* Piotrek Pęczek
* Michał Nowotnik
* Wojciech Zając
* Wojciech Błaszczuk (@julianvolodia)
