FROM python:3.12

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-venv python3-dev gcc && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv venv

COPY . .

RUN . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash", "-c", "source venv/bin/activate && python3 bot.py"]