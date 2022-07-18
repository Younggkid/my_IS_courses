FROM python:slim
WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -i https://mirror.sjtu.edu.cn/pypi/web/simple
COPY . .
CMD ["gunicorn", "OurWeb.wsgi", "--bind", "0.0.0.0:8000"]
