FROM python:3.8.5
WORKDIR /code
COPY yatube/requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade attrs
COPY /yatube .
EXPOSE 8000
CMD ["gunicorn", "yatube.wsgi:application", "--bind", "0:8000" ]
