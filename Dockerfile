FROM python:3.11-slim

ENV PORT=8092
ENV SERVER_PORT=

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./src/main/python/main.py" ]