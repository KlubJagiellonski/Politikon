FROM ubuntu:trusty
RUN apt-get update -y -qq --fix-missing
RUN apt-get install -y python-dev python-pip postgresql-client-common postgresql postgresql-contrib libpq-dev git libmemcached-dev curl openssh-server

RUN mkdir /var/run/sshd
RUN echo 'root:dupa3' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ADD / /app
ADD /requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

ENV PORT 8000
EXPOSE 8000
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
