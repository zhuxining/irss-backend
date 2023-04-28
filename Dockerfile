FROM python:3.10
WORKDIR /irss/
RUN pip install --upgrade pdm
COPY ./pyproject.toml ./pdm.lock* /irss/
RUN pdm install
COPY ./main.py /irss/
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]