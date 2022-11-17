FROM python:3.8.5
WORKDIR /code
COPY yatube/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade attrs
RUN pip3 install -r requirements.txt
COPY /yatube .
CMD [ "sh", "-c", \
"python3 manage.py migrate \
&& \
python3 manage.py shell \
&& \
python3 manage.py collectstatic --noinput \
&& \
uvicorn yatube.asgi:application --host 0.0.0.0 --port 8080 " \
]
