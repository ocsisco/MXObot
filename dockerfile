FROM python:3.11-alpine

#ENV FLASK_APP=flaskr
#ENV FLASK_ENV=development

COPY . /bot

WORKDIR /bot

RUN pip install -r requirements.txt

ENV TZ Europe/Madrid
# Unit tests
# RUN pip install pytest && pytest

#EXPOSE 4000

ENTRYPOINT ["python"]

CMD ["bot.py"]

