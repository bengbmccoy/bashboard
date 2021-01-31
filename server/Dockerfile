FROM python:3.7

RUN pip install Flask gunicorn
RUN pip install flask_assets
RUN pip install python-dotenv
RUN pip install dash
RUN pip install pandas

COPY ./ app/
WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
