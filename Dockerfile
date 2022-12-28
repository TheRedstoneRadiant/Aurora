FROM python:3.9

RUN pip install --no-cache-dir -r src/requirements.txt

CMD [ "python", "src/main.py"]
