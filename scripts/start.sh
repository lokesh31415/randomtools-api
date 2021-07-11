#!/bin/bash

# Start nginx

# Start uwsgi
systemctl start uwsgi_randomtools
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start uwsgi: $status"
  exit $status
fi 

systemctl start nginx
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start nginx: $status"
  exit $status
fi

while sleep 60; do
  ps aux |grep nginx |grep -q -v grep
  PROCESS_1_STATUS=$?
  ps aux |grep uwsgi |grep -q -v grep
  PROCESS_2_STATUS=$?
  # If the greps above find anything, they exit with 0 status
  # If they are not both 0, then something is wrong
  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 ]; then
    echo $PROCESS_1_STATUS
    echo $PROCESS_2_STATUS
    echo "One of the processes has already exited."
    exit 1
  fi
done
