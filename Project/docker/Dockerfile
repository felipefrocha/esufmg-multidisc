FROM python:3.8

WORKDIR /code

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt
ENV NAME_FILE=testeA
ENV INTERACTIONS=10000000
COPY . . 

CMD ["python", "-u", "__init__.py"]