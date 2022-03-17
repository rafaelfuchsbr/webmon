FROM python:3.9.4-buster

WORKDIR /webmon

COPY ./app ./app
COPY ./requirements.txt .
                                                                                                                              
RUN pip install -r requirements.txt \
    && rm requirements.txt

WORKDIR /webmon/app

ENV WEBMON_CONFIG_FILE=config.yaml

ENV PYTHONPATH "${PYTHONPATH}:/webmon/app"

# CMD [ "python", "run.py" ]