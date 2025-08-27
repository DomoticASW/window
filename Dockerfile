FROM python:3.11-slim

ENV PORT=8092
ENV SERVER_ADDRESS=
ENV LAN_HOSTNAME=
ENV SERVER_DISCOVERY_ADDR="255.255.255.255"
ENV SERVER_DISCOVERY_PORT=30000
ENV ID="sm_001"
ENV NAME="Smart Window 1"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./src/main/python/main.py" ]