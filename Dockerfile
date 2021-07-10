FROM randomtools-v2
USER root
RUN systemctl start nginx
RUN systemctl start uwsgi_randomtools
EXPOSE 80