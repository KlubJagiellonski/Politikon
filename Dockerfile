FROM ubuntu:trusty
RUN apt-get update -y -qq
RUN apt-get install -y python-dev python-pip postgresql-client-common postgresql postgresql-contrib libpq-dev git libmemcached-dev curl
ADD /requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
RUN curl -o /usr/bin/forego https://godist.herokuapp.com/projects/ddollar/forego/releases/current/linux-amd64/forego
RUN chmod +x /usr/bin/forego
ADD / /app
ENV PORT 5000
EXPOSE 5000
CMD ["/usr/bin/forego", "start"]
