FROM python:3.11.7-bullseye
WORKDIR /dshex-bot
ADD . /dshex-bot
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["python", "run_bot.py"]