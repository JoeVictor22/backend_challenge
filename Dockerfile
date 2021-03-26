FROM python:3.7.5-slim

WORKDIR /web-back

COPY requirements.txt .

RUN apt-get update
RUN apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

ENV PORT 5000

RUN pip install -r requirements.txt

COPY . .


#CMD ["gunicorn", "--workers", "10", "--bind", "0.0.0.0:5000", "-m", "007", "wsgi:app"]

CMD ["gunicorn", "--workers", "10", "-m", "007", "wsgi:app"]

