FROM python:3.8
# FROM python:3.8-alpine

WORKDIR /code

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . . 
RUN ls -lha
ENTRYPOINT [ "python3" ]
CMD ["-u", "__init__.py"]