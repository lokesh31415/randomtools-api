FROM randomtools/randomtools-api:init
# create work directory
RUN mkdir -p /var/www/html/randomtools
# change working directory
WORKDIR /var/www/html/randomtools
# copy configuration files
COPY production/docker/uwsgi_randomtools.service /etc/systemd/system/
COPY production/docker/randomtools.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/randomtools.conf /etc/nginx/sites-enabled/
# remove deault nginx file from sites available if exist
RUN rm -f /etc/nginx/sites-available/default
# environment variables
ENV PORT=80
# copy current directory files
COPY . .
# create additional required directories
RUN mkdir logs
# install dependencies
RUN pip install -r requirements.txt
# change permission of start script
RUN chmod +rwx ./production/docker/start.sh

# start start.sh script which will start uwsgi and nginx
CMD sed -i -e 's/!!PORT!/'"$PORT"'/g' /etc/nginx/sites-available/randomtools.conf && rm -f /etc/nginx/sites-enabled/default && ./production/docker/start.sh


# docker build -t randomtools/randomtools-api:latest .
