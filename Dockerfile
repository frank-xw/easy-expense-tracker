FROM python:3.9-alpine

# Installing packages
# RUN apk udpate
RUN pip install --no-cache-dir pipenv

# Defining wd and adding src code
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY easyexps ./easyexps

# Install API dependencies
RUN pipenv install --system --deploy

# Start app
EXPOSE 5050
ENTRYPOINT [ "/usr/src/app/bootstrap.sh" ]