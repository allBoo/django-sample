FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /var/www
COPY requirements.txt /var/www/
RUN pip install -r requirements.txt
COPY . /var/www/

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
