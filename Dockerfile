FROM python:3.9

WORKDIR /src

COPY src/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN git clone https://github.com/TheRedstoneRadiant/discord.py-self && cd discord.py-self && pip3 install -U .[voice]

COPY . .

CMD [ "python3", "src/main.py"]
