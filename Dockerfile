FROM python:3.11.6
RUN curl -sSL https://install.python-poetry.org | python -
# ENV PATH="${PATH}:/root/.poetry/bin"
# COPY pyproject.toml poetry.lock /app/
COPY . /app
WORKDIR /app
RUN pip install poetry && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN poetry
RUN pip install --no-cache-dir -r requirements.txt
RUN pip uninstall poetry -y
# CMD ["python", "app.py"]
