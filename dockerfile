FROM tiangolo/uwsgi-nginx:python3.10

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python", "./start.py"]
