#!/bin/bash

# Starts an Apache instance with custom config and mod_wsgi from this project's
# virtual environment.

# based on https://github.com/hyneq/STINBankSystem/blob/main/start_server.sh

source "$(dirname "$0")/activate"

source "$project_root/server_vars"

# Create the logs dir
mkdir -p "$logs_dir"

# If the server is already running, restart and exit
if [ -f "$pid_file" ]; then
    "$server_root/apachectl" graceful
    exit
fi

# Run mod_wsgi-express server configured for this application
mod_wsgi-express start-server \
--server-root "$server_root" \
--port="$server_port" \
--proxy-mount-point="$STREAM_INTERFACE_PATH" "$stream_path" \
--url-alias=/static "$app_dir/static_collected/" \
--application-type=django \
--passenv=DJANGO_SETTINGS_MODULE \
--working-directory="$app_dir" \
--access-log-name="$logs_dir/access.log" \
--error-log-name="$logs_dir/error.log" \
--entry-point="$app_dir/bird_identification_web/wsgi.py" \
--include-file="$custom_apache_conf"
