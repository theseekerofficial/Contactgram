FROM python:3.12

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y python3-venv

RUN python3 -m venv venv
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash", "-c", "source venv/bin/activate && python3 bot.py"]