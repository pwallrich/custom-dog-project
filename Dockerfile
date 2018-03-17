FROM python:3.6

RUN apt-get update -y

Add ./requirements/requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt
RUN pip install flask

Add ./web_app_classes /app/web_app_classes
Add ./web_app.py /app/web_app.py
ADD ./dog_names.json /app/dog_names.json
Add ./bottleneck_features /app/bottleneck_features
ADD ./ownImages /app/ownImages
ADD ./haarcascades app/haarcascades
ADD ./saved_models app/saved_models

RUN mkdir /app/temp

WORKDIR /app

CMD ["python", "/app/web_app.py"]

