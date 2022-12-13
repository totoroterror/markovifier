ARG python=python:3.11-alpine

FROM ${python} AS build

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

RUN pip3 install --upgrade pip

RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM ${python}

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH

WORKDIR /app

COPY . .

CMD ["python3", "src/main.py"]
