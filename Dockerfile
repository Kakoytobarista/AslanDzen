FROM python:3.8.5
WORKDIR /code
COPY yatube/requirements.txt .
RUN pip3 install -r requirements.txt
COPY /yatube .
CMD [ "sh", "-c", \
"python3 manage.py migrate \
&& \
python3 manage.py collectstatic --noinput \
&& \
daphne -b 0.0.0.0 -p 8001 yatube.asgi:application" \
]
