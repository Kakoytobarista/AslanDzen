FROM python:3.8.5
WORKDIR /code
COPY yatube/requirements.txt .
COPY /cert .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade attrs
COPY /yatube .
CMD [ "sh", "-c", \
"python3 manage.py migrate \
&& \
python3 manage.py shell \
&& \
python3 manage.py collectstatic --noinput \
&& \
python3 manage.py loaddata data.json \
&& \
daphne -e ssl:8001:privateKey=privkey.pem:certKey=cert.pem yatube.asgi:application & gunicorn yatube.wsgi:application --bind 0.0.0.0:8000 --reload" \
]
