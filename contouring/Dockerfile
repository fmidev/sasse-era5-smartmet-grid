# Container for Python related contouring stuff

# Use latest stable Python
# From alpine to have minimal container size
FROM python:3.7.4-alpine3.10

# Directory to do things in container  
WORKDIR /usr/src/app

# To 
COPY ./app ./
RUN pip install --no-cache-dir -r requirements.txt

# TODO: Figure this thing out
# CMD [ "./bin/contouring" ]