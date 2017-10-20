FROM python:2

ADD requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
RUN wget https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64.deb
RUN dpkg -i dumb-init_*.deb

ENTRYPOINT ["/usr/bin/dumb-init", "python"]