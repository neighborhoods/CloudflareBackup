FROM python:2

WORKDIR /usr/src/app
RUN pip install --no-cache-dir poetry

COPY pyproject.toml pyproject.lock
RUN poetry install

CMD [ "poetry", "run", "python", "./update_agentsite_dns.py" ]
