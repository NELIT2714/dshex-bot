FROM python:3.11.7-bullseye
COPY . /dshex-bot
WORKDIR /dshex-bot
EXPOSE 8001
# RUN pip install -r requirements.txt
CMD ["python", "run_bot.py"]