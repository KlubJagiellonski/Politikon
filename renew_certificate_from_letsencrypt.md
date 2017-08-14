Install Certbot (https://certbot.eff.org/#pip-other):
curl https://dl.eff.org/certbot-auto >certbot-auto
chmod a+x certbot-auto

./certbot-auto certonly -d www.politikon.org.pl -m koduj-z-kj@googlegroups.com --manual --debug --agree-tos --manual-public-ip-logging-ok --preferred-challenges dns

sudo cp /etc/letsencrypt/live/www.politikon.org.pl/fullchain.pem .

sudo cp /etc/letsencrypt/live/www.politikon.org.pl/privkey.pem .

heroku certs:add fullchain.pem privkey.pem -a politikon --confirm politikon --type sni
