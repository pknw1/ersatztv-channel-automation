FROM python:3.10

# docker run -it --rm -v ./ersatztv.sqlite3:/app/ersatztv.sqlite3 pknw1/ersatztv-bulkadd-channels:latest shows
# docker run -it --rm -v ./ersatztv.sqlite3:/app/ersatztv.sqlite3 pknw1/ersatztv-bulkadd-channels:latest movies

RUN mkdir /app
WORKDIR /app

COPY iteration2.1.py /app/channel-automator-0.2.py

ENTRYPOINT ["/usr/bin/python3", "/app/channel-automator-0.2.py"]
#CMD ["/usr/bin/python3", "/app/channel-automator-0.2.py"]
