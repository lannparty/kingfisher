FROM docker.io/library/python:3.9-slim

COPY . /usr/src/app/kingfisher/
WORKDIR /usr/src/app/kingfisher/

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

ENV PYTHONPATH=/usr/src/app/kingfisher
#ENV KINGFISHER_TARGET="USLM"
#ENV KINGFISHER_QUANTITY="20"
#ENV KINGFISHER_PRICE_STEP=".01"
#ENV KINGFISHER_FRACTION_OF_SPREAD=".1"
#ENV KINGFISHER_WAIT_FOr_FILL="10"
#ENV KINGFISHER_CLIENT_ID="1"
#ENV KINGFISHER_IB_ADDRESS="host.docker.internal"
#ENV KINGFISHER_IB_PORT="7497"

CMD [ "python", "kingfisher.py" ]
