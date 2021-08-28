FROM python:3.8

WORKDIR /code

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . . 

ENTRYPOINT [ "python"]
CMD ["-u", "launch_jobs.py"]