FROM python:3.8.5
WORKDIR /code
COPY yatube/requirements.txt .
RUN pip3 install -r requirements.txt
COPY /yatube .
CMD [ "sh", "-c", \
"python3 manage.py migrate \
&& \
python3 manage.py shell \
&& \
python3 manage.py collectstatic --noinput \
&& \
daphne -b 127.0.0.1 -p 8000 yatube.asgi:application" \
]
