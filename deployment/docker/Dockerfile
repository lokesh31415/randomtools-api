FROM randomtools/randomtools-api:pyuwinx2
# change user to root
USER root
# change working directory
WORKDIR /var/www/html/randomtools
# remove existing files if any
# RUN shopt -s dotglob
RUN rm -rf ./*
# copy current directory files
COPY ../../ .
# install dependencies
RUN mkdir logs
RUN apt-get install python3-pip python3-dev libpq-dev
RUN pip install -r requirements.txt
# change permission of start script
RUN chmod +rwx ./scripts/start.sh
ARG PORT
RUN echo $PORT
# start start.sh script which will start uwsgi and nginx
CMD sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/sites-available/default /etc/nginx/sites-available/randomtools.conf && nginx -g 'daemon off;' && ./scripts/start.sh
