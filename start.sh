#!/bin/bash

# based on https://github.com/hyneq/STINBankSystem/blob/main/start_server.sh

# Starts mod_wsgi server configued for this project

source "$(dirname "$0")/activate"

# Stop the server first if it is already running
if [ -f $pid_file ]; then
    "$project_root/stop.sh"
    sleep 0.3
fi

# Create the logs dir
mkdir -p "$logs_dir"

# Start the server out-of-session
export APP_NAME="$app_name"
export APP_DIR="$app_dir"
nohup \
mod_wsgi-express start-server \
--port="$server_port" \
--url-alias=/static "$app_dir/static_collected/" \
--application-type=django \
--passenv=DJANGO_SETTINGS_MODULE \
--working-directory="$app_dir" \
--access-log-name="$logs_dir/access.log" \
--error-log-name="$logs_dir/error.log" \
--entry-point="$app_dir/bird_identification_web/wsgi.py" \
--include-file="$project_root/httpd.conf" \
> "$logs_dir/server.out" 2>&1 \
&

# Write the server's PID to a pidfile
echo $! > "$pid_file"
