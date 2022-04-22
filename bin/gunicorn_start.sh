# source venv/bin/activate
PORT=1234
# ps -ef | grep ${PORT} | awk -F" " '{ print $2 }' | xargs -n 1 kill
gunicorn -w 5 car.wsgi:application -b 0.0.0.0:${PORT}
