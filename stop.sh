#!/bin/bash

# based on https://github.com/hyneq/STINBankSystem/blob/main/stop_server.sh

# Stops server if running

source "$(dirname "$0")/activate"

source "$project_root/server_vars"

# Exit if no pid_file is present
if [[ ! -f "$pid_file" ]]; then
    echo "Server for $app_name not running, cannot stop" >&2
    exit 1
fi

# Kill the server process
"$server_root/apachectl" graceful-stop
