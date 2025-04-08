FROM python:3.12

WORKDIR /app
ADD . /app

ARG requirements=requirements/reqs.txt

RUN pip install --no-cache-dir -r $requirements

# Me permite esperar a que el contenedor de postgres se termine de construir antes de intentar la conexión con el contenedor de FastApi.
RUN apt-get update && apt-get install -y curl && \
    curl -o /usr/local/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it
    
CMD uvicorn main:app --host 0.0.0.0 --port 8001 --reload

