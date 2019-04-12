[ "$SYSLOG_HOST" != "" ] && ES_HOST=$SYSLOG_HOST || ES_HOST=0.0.0.0
ES_PORT=5601
ES_URL="http://$ES_HOST:$ES_PORT"

# Send some initial data to logstash
echo "Sawmill GENERIC Sawmill has been initialized" | nc $ES_HOST $SYSLOG_PORT

# Import the dashboard and objects
echo "Importing objects...."
function import_object() {
    curl -XPOST $ES_URL/api/saved_objects/_import \
        -H 'kbn-xsrf: true' \
        -H 'Content-Type: application/json' \
        --data-binary @../objects/$1
}
import_object "blueteam_dashboards.json"

# Set Advanced Settings
function set_setting() {
    echo "Configuring setting $1 = $2"
    curl -X POST -H "Content-Type: application/json" -H "kbn-xsrf: false" -d "{\"value\":\"$2\"}" $ES_URL/app/kibana#/management/kibana/settings/$1
}

set_setting "dashboard:defaultDarkTheme" "true"
set_setting "doc_table:highlight" "false"
set_setting "doc_table:hideTimeColumn" "true"
