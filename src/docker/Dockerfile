FROM python:3.10

# docker run -it --rm -v ./ersatztv-config-folder:/db pknw1/ersatztv-bulkadd-channels:latest

RUN mkdir /app
WORKDIR /app

ADD ../interation0.py /app/channel-automator-0.1.py

CMD ["/usr/bin/python3", "/app/channel-automator-0.1.py"]