FROM python:3.9.1-alpine3.12
RUN mkdir /app
RUN mkdir /app/log
WORKDIR /app
ADD . /app
RUN pip3 -q --disable-pip-version-check install -r requirements.txt
EXPOSE 8080
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]