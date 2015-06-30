# Politikon - stawiamy na politykę
www.politikon.org.pl

Politikon to serwis internetowy, którego celem jest popularyzowanie pozytywnego spojrzenia na politykę, a także wyłonienia osób, które potrafią przewidywać wydarzenia społeczno-polityczne. Projekt ma pokazać, że polityka to nie tylko cyniczna, losowa gra, ale także miejsce ścierania się idei, pomysłów, miejscem gdzie przyczyny powodują określone skutki. Serwis jset grą internetową, której uczestnicy będą mogli zakładać się o wyniki różnych wydarzeń społeczno-politycznych. Giełdowy charakter gry (rynek przewidywań) pozwala pokazać prawdopodobieństwo wystąpienia określonych wydarzeń, co sprawia, że serwis jest interesującą alternatywą dla sondaży.

## Status projektu

Projekt jest rozwijany. Planowany start to jesień 2015.

## Politikon lokalnie (po angielsku)

* Install [Docker](https://docs.docker.com/)

* Run Docker:
```
boot2docker start
```
(Don't forget to set the environment variables as outputed by `boot2docker start`)

* Clone the Politikon source-code repository from [https://github.com/KlubJagiellonski/Politikon](GitHub)

* Go to the source-code folder 

* Run:
```
docker_rebuild.sh
Run docker_run.sh
```

* Enter docker:
```
ssh root@$(boot2docker ip) -p 2233
Password: pass
```

* Restore the db snapshot:
```
cd db-dumps
ls *.dumps
./db_restore_dump.sh THE_LATEST_DB_DUMP
cd ..
```

* Run the web server:
```
python manage.py runserver 0.0.0.0:8000
```

* Point your web browser to the 
```
boot2docker ip
YOUR_IP:8000
```

## Autorzy

W projekt są zaangażowani:
* [Klub Jagielloński](http://www.kj.org.pl) - treści, prowadzenie gry, marketing, promocja
* [Koduj dla Polski](http://www.kodujdlapolski.pl) - wsparcie instytucjonalne i osobowe
* Jacek Głodek
* Tomek Grynfylder
* Tomek Kopczuk
* Kuba Lipiński
* Marcin Mincer
* Piotrek Pęczek

