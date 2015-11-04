# Politikon - stawiamy na politykę
www.politikon.org.pl

Politikon to serwis internetowy, którego celem jest popularyzowanie pozytywnego spojrzenia na politykę, a także wyłonienia osób, które potrafią przewidywać wydarzenia społeczno-polityczne. Projekt ma pokazać, że polityka to nie tylko cyniczna, losowa gra, ale także miejsce ścierania się idei, pomysłów, miejscem gdzie przyczyny powodują określone skutki. Serwis jest grą internetową, której uczestnicy będą mogli zakładać się o wyniki różnych wydarzeń społeczno-politycznych. Giełdowy charakter gry (rynek przewidywań) pozwala pokazać prawdopodobieństwo wystąpienia określonych wydarzeń, co sprawia, że serwis jest interesującą alternatywą dla sondaży.

## Status projektu

Projekt jest rozwijany. Planowany start to jesień 2015.

## Politikon lokalnie (po angielsku)

### Mac OS X

* Install [Docker](https://docs.docker.com/)

* Run Docker
```
boot2docker start
```
(Don't forget to set the environment variables as outputed by `boot2docker start`)

* Clone the Politikon source-code repository from [https://github.com/KlubJagiellonski/Politikon](GitHub)
```
git clone git@github.com:KlubJagiellonski/Politikon.git
```
* Go to the source-code folder

* Build and run your docker
```
./docker_rebuild.sh
./docker_run.sh
```

* Add local.politikon.org.pl to your OS hosts files Add 192.168.59.103 or whatever IP your docker instance has to the host file.
```
...
192.168.59.103 local.politikon.org.pl
...
```

* Add local.politikon.org.pl as a host for your FB and Twitter app

* Install missing dependencies with pip
```
pip install -r requirements.txt
```

* Restore the db snapshot
```
cd db_dumps
ls *.dumps
./db_restore_dump.sh THE_LATEST_DB_DUMP
cd ..
```

* Migrate the database
```
python manage.py migrate
```

* Run the web server
```
python manage.py runserver 0.0.0.0:8000
```

* Point your web browser to the
```
boot2docker ip
YOUR_IP:8000
```

* To get inside docker container when starting deployment
```
./docker_run.sh
```

* If you need to access Django Admin on Dev machine:
```
python manage.py createsuperuser
```

* If you need to sync your docker local time
```
boot2docker ssh sudo ntpclient -s -h de.pool.ntp.org
docker run -it -v `pwd`:/app -p 2233:22 -p 8000:8000 --name politikon_instance politikon
```

* If you need to upgrade boot2docker:
```
boot2docker upgrade
boot2docker delete
boot2docker init
boot2docker up
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

### Linux

* Install [Docker](https://docs.docker.com/)

* Clone the Politikon source-code repository from [https://github.com/KlubJagiellonski/Politikon](GitHub)
```
git clone git@github.com:KlubJagiellonski/Politikon.git
```

* Go to the source-code folder

* Add local.politikon.org.pl to your OS hosts files
```
...
127.0.0.1 local.politikon.org.pl
...
```

* Add local.politikon.org.pl as a host for your FB and Twitter app

* Build and run your docker
```
./docker_rebuild.sh
./docker_run.sh
```

* Restore the db snapshot
```
cd db_dumps
ls *.dumps
./db_restore_dump.sh THE_LATEST_DB_DUMP
cd ..
```

* Install missing dependencies with pip
```
pip install -r requirements.txt
```

* Migrate the database
```
python manage.py migrate
```

* Run the web server
```
python manage.py runserver 0.0.0.0:8000
```

* Point your web browser to the
```
127.0.0.1:8000
```

* To get inside docker container when starting deployment
```
./docker_run.sh
```

* If you need to access Django Admin on Dev machine:
```
python manage.py createsuperuser
```

* If you need to sync your docker local time
```
boot2docker ssh sudo ntpclient -s -h de.pool.ntp.org
docker run -it -v `pwd`:/app -p 2233:22 -p 8000:8000 --name politikon_instance politikon
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
