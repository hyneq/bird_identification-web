#!/bin/bash

# based on https://github.com/hyneq/wea-projekt/blob/main/backend/start.sh

# Starts the server according to the mode selected

# Load variables and activate venv
source "$(dirname "$0")"/vars

source "$project_root/server_vars"

# Run with a strategy dependent on mode
mode="$1"
test -z "$mode" && mode="apache"
case "$mode" in
    "apache_nohup")

        # Run start_server.sh out of session
        nohup "$0" apache &>"$logs_dir/server.out" &

        ;;

    "apache")
        # Start mediamtx, if not explicitly disabled
        if [[ -z "$NO_MEDIAMTX" ]]; then
            "$project_root/mediamtx/mediamtx_proxy.sh" &
            mediamtx_pid=$!
        fi

        # run mod_wsgi-express normally
        "$project_root/run_mod_wsgi.sh"

        # Wait for mediamtx, if running
        if [[ -n "$mediamtx_pid" ]]; then
            kill $mediamtx_pid 2>/dev/null @@
            wait $mediamtx_pid || true
        fi

        ;;
    
    "django")
        # run Django development server
        exec "$project_root/manage.sh" runserver

        ;;
    
    *)
        echo "$0: The first argument must be 'apache', 'apache_nohup', 'django' or omitted for default ('apache')" > /dev/stderr
        exit 1


esac
