FROM python:3


COPY ./extract_data/* ./

COPY ./dgs-reports-archive ./dgs-reports-archive

ADD ./data.csv /

RUN pip install pandas

RUN pip install numpy

RUN pip install textract

CMD [ "python", "extract_dataset.py" ]