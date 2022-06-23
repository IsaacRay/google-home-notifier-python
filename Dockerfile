FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV GRP_NAME "Basement speaker"
ENTRYPOINT ["python"]
CMD ["main.py"]
