FROM python:3.8

WORKDIR /code

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . . 
RUN ls
ENTRYPOINT [ "python3" ] [
CMD ["-u", "__init__.py"]