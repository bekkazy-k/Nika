# Base image
FROM python:3.7

# We create an /app directory within our
# image that will hold our application source
# files
RUN mkdir /app

# We copy everything in the root directory
# into our /app directory
ADD . /app

# We specify that we now wish to execute
# any further commands inside our /app
# directory
WORKDIR /app

# Install all dependencies
RUN pip install Nika==1.1.3

# Set Timezone
ENV TZ=Asia/Bishkek
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Start command
CMD [ "python", "-u", "/app/app.py" ]
