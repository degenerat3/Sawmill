#!/bin/bash
if [ "$SYSLOG_HOST" = "" ] && [ "$1" = "" ]; then
	echo "Please pass the IP address as the first argument or in the SYSLOG_HOST env var."
	exit
fi
[ "$1" != "" ] && HOST="$1" || HOST="$SYSLOG_HOST"
curl -X DELETE "http://$HOST:9200/_all"
