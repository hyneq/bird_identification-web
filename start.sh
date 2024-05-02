#!/bin/bash

# based on https://github.com/hyneq/wea-projekt/blob/main/backend/start.sh

# Starts the server according to the mode selected

# Load variables and activate venv
source "$(dirname "$0")"/vars

source "$project_root/server_vars"

# Run with a strategy dependent on mode
mode="$1"
case "$mode" in
    "deploy")

        # Start mod_wsgi-express out-of-session
        nohup "$project_root/run_mod_wsgi.sh" &>"$logs_dir/mod_wsgi.out" &

        ;;

    "dev_apache")
        # run mod_wsgi-express normally
        exec "$project_root/run_mod_wsgi.sh"

        ;;
    
    "dev")
        # run Django development server
        exec "$project_root/manage.sh" runserver

        ;;

    *)
        exec "$0" "$SETUP_MODE"
esac
