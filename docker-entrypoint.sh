#!/bin/bash

if [ "$MIGRATE_DB" != "" ]; then
  ./manage.py migrate --noinput
fi

if [[ $@ == "bash" ]]
then
	echo "Command line argument is set [$@].";
	exec "bash";
elif [[ $@ == "debug" ]]
then
	echo "Command line argument is set [$@].";
	exec "./manage.py" "runserver" "0.0.0.0:8000";
elif [[ $@ != "" ]]
then
	echo "Command line argument is set [$@].";
	exec "bash" "-c" "$@";
else
	echo "Command line argument not set.";
	exec "uwsgi" "--pythonpath" "./src/" "--static-map" "/static=/var/www/static/" "--http-socket" ":8000" "--wsgi-file" "/var/www/src/hotel/wsgi.py"
fi
