FROM python:3.10

WORKDIR /app

COPY / /app
RUN pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

CMD [ "python", "src/app.py" ]