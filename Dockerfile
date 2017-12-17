FROM       python:3.6

LABEL      app.name="Storified" \
           app.description="Archive Storify stories" \
           app.repo.url="https://github.com/DocNow/storified" 

ENV        STORIFY_USER

WORKDIR    /storified
RUN        pip install storified

CMD storified $STORIFY_USER
