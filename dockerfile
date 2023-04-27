FROM tiangolo/uwsgi-nginx:python3.10

COPY . .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y


RUN pip3 install -r requirements.txt

CMD ["python", "./app.py"]
