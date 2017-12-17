FROM       python:3.6

LABEL      app.name="Storified" \
           app.description="Archive Storify stories" \
           app.repo.url="https://github.com/DocNow/storified" 

WORKDIR    /storified
COPY       Pipfile* ./
RUN        pip install storified
COPY       . ./
RUN        chmod a+x storified.py

ENTRYPOINT ["./storified.py"]
