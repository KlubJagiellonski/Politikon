git clone https://github.com/letsencrypt/letsencrypt

cd letsencrypt/

disable SSL by putting:
SSLIFY_DISABLE = True
to productionsettings.py

commit and push to production

./letsencrypt-auto certonly --manual

put: www.politikon.org.pl

modify politikon/urls.py & politikon/views.py according to instructions

cp /etc/letsencrypt/www.politikon.org.pl/* .

heroku certs:update fullchain.pem privkey.pem -a politikon

remove the line
SSLIFY_DISABLE = True
from productionsettings.py

commit and push to production

done :)
