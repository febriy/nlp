FROM continuumio/anaconda3:2019.10

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./src /app/src
COPY ./data /app/data
COPY ./model /app/model

CMD [ "streamlit", "run", "src/app.py" ]
