FROM randomtools/randomtools-api:pyuwinx2
# change user to root
USER root
# change working directory
WORKDIR /var/www/html/randomtools
# remove existing files if any
# RUN shopt -s dotglob
RUN rm -rf ./*
# copy current directory files
COPY . .
# install dependencies
# COPY ./scripts/uwsgi_randomtools.service /etc/systemd/system/uwsgi_items_rest.service
# COPY ./scripts/randomtools.conf /etc/nginx/sites-available/randomtools.conf
# RUN ln -s /etc/nginx/sites-available/items-rest.conf /etc/nginx/sites-enabled/
RUN mkdir logs
RUN apt-get install python3-pip python3-dev libpq-dev
RUN pip install -r requirements.txt
# change permission of start script
RUN chmod +rwx ./scripts/start.sh
# start start.sh script which will start uwsgi and nginx
CMD [ "./scripts/start.sh" ]
