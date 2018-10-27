FROM python:3.5-slim

ENV basedir /tranvia
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8


WORKDIR $basedir

COPY . .

RUN     pip install pipenv
RUN     pipenv install --system

# ENTRYPOINT "pipenv run python main.py"
ENTRYPOINT ["python3", "main.py"]