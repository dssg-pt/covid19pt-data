FROM python:3-slim
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app requests pandas
ENV PYTHONPATH /app
CMD ["python3", "/app/main.py"]
