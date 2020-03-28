FROM python:3-slim
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app requests pandas pytest==5.2.2 pytest-cov==2.8.1 pytest-mock==1.11.2	

ENV PYTHONPATH /app
CMD ["python3", "/app/main.py"]
