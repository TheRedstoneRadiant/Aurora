FROM python:3.9

WORKDIR /src

COPY src/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "src/main.py"]
