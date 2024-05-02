#!/bin/bash

# based on https://github.com/hyneq/STINBankSystem/blob/main/start_server.sh

# Stops mod_wsgi server configued for this project, if running

source "$(dirname "$0")/activate"

# Exit if no pid_file is present
if [[ ! -f "$pid_file" ]]; then
    echo "Server for $app_name not running, cannot stop" >&2
    exit 1
fi

# Kill the server process
kill "$(cat "$pid_file")" 2>/dev/null

# Remove the pidfile
rm "$pid_file"